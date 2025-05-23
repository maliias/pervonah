from telethon import events
from telethon.tl.functions.messages import GetDiscussionMessageRequest
import logging
import config
from openai import OpenAI

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


@events.register(events.NewMessage(chats=config.channels_pn))
async def pervonah_default(event):
    client = event.client
    try:
        # Получаем сообщение в связанной группе
        discussion = await client(GetDiscussionMessageRequest(
            peer=event.chat_id,
            msg_id=event.message.id
        ))

        discussion_msg = discussion.messages[0]  # это сообщение в группе
        # Отправляем комментарий (ответ)
        await client.send_message(
            entity=discussion_msg.to_id,
            message=config.text_pn,
            reply_to=discussion_msg.id
        )
        logging.info(f"Комментарий в канал успешно написан")
        
    except Exception as e:
        logging.warning("Ошибка при отправке комментария:", e)
        
        
@events.register(events.NewMessage(chats=config.channels_pn))
async def pervonah_gpt(event):
    client = event.client
    gpt_client = OpenAI(api_key=config.gpt_api_key)
    try:
        original_text = event.raw_text
        print(original_text)
        # Получаем сообщение в связанной группе
        discussion = await client(GetDiscussionMessageRequest(
            peer=event.chat_id,
            msg_id=event.message.id
        ))

        discussion_msg = discussion.messages[0]
        
        

        
        response = gpt_client.responses.create(
            model="gpt-4.1",
            input=config.zapros_gpt + f"{original_text}"
        )
        # Отправляем комментарий (ответ)
        await client.send_message(
            entity=discussion_msg.to_id,
            message=response.output_text,
            reply_to=discussion_msg.id
        )
        logging.info(f"Комментарий в канал успешно написан")

    except Exception as e:
        logging.warning(f"Ошибка при отправке комментария: {e}")