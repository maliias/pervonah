import random
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
import logging
import config
import handlers.pervonah

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

api_id = config.api_id
api_hash = config.api_hash                                    

threads_count = input("Введите количество потоков: ")
sessions = [i for i in range(1, int(threads_count)+1)]

async def start_client(session_name, get_mode, pervonah_mode=None):
    async with TelegramClient(session_name, system_version="4.16.30-vxCUSTOM", device_model="Pixel 4", lang_code="en", api_id=api_id, api_hash=api_hash) as client:
        logging.info(f"{session_name}: Запуск приложения")
        
        for c in config.channels_pn:
            try:
                await client(JoinChannelRequest(c))
                logging.info(f"{session_name}: Успешно вступил в канал {c}")
            except Exception as e:
                logging.warning(f"{session_name}: Ошибка при вступлении в канал {c}: {e}")
        
        if get_mode == 1:
            if pervonah_mode == 1:
                client.add_event_handler(handlers.pervonah.pervonah_default)
                logging.info(f"{session_name}: Включен обычный первонах")
            elif pervonah_mode == 2:
                client.add_event_handler(handlers.pervonah.pervonah_gpt)
                logging.info(f"{session_name}: Включен GPT первонах")
                
        elif get_mode == 2:
            try:
                file = await client.upload_file(config.avatar)
                await client(UploadProfilePhotoRequest(file=file))
                await client(UpdateProfileRequest(
                    first_name=config.first_name, 
                    last_name=config.second_name, 
                    about=config.bio
                ))
                logging.info(f"{session_name}: Профиль успешно обновлен")
            except Exception as e:
                logging.error(f"{session_name}: Ошибка при обновлении профиля: {e}")
        
        await client.run_until_disconnected()


async def main():
    print("Выберите режим для всех аккаунтов:")
    get_mode = int(input("0 - Выйти в главное меню\n1 - Первонах\n2 - Изменение профилей\nВведите какой режим использовать: "))
    
    pervonah_mode = None
    if get_mode == 1:
        pervonah_mode = int(input("1 - Обычный первонах текстом\n2 - GPT первонах\nВыберите режим первонаха: "))
    
    await asyncio.gather(*(
        start_client(f"sessions/{str(s)}", get_mode, pervonah_mode) 
        for s in sessions
    ))


if __name__ == "__main__":
    asyncio.run(main())