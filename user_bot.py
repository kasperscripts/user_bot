# user_bot.py
import asyncio
import logging
import os
from datetime import datetime
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()

# === КОНФИГ ===
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

CHANNEL_ID = "oxidebtatstvo"

# === СООБЩЕНИЕ ===
MESSAGE_TEXT = "продаю анрут чит магик 270 руб писать `@nikita1055`"
INTERVAL = 60  # 1 минута

# === ФУНКЦИЯ СОЗДАНИЯ КЛИЕНТА ===
def create_client():
    if SESSION_STRING:
        return Client(
            name="user_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION_STRING,
            sleep_threshold=60,
        )
    else:
        return Client(
            "my_user_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            sleep_threshold=60,
        )

# === КНОПКА ===
def get_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 НАПИСАТЬ @nikita1055", callback_data="copy_nikita1055")]
    ])

# === СОЗДАЁМ КЛИЕНТ ===
app = create_client()

# === ОБРАБОТЧИК КНОПКИ ===
@app.on_callback_query()
async def handle_copy(client, callback_query):
    if callback_query.data == "copy_nikita1055":
        await callback_query.answer("✅ @nikita1055 скопирован!", show_alert=True)
        await callback_query.message.reply("📋 Напиши: @nikita1055")

# === СПАМ-ЦИКЛ ===
async def spam_loop(client):
    while True:
        try:
            await client.send_message(
                CHANNEL_ID,
                MESSAGE_TEXT,
                reply_markup=get_button()
            )
            logging.info(f"✅ Отправлено в {datetime.now()}")
        except Exception as e:
            error_str = str(e)
            logging.error(f"❌ Ошибка: {error_str}")
            
            # Если дубликат сессии - пересоздаём клиент и выходим из цикла
            if "AUTH_KEY_DUPLICATED" in error_str:
                logging.warning("⚠️ Дубликат сессии! Перезапускаем бота...")
                # Сигнализируем о необходимости перезапуска
                return
        
        await asyncio.sleep(INTERVAL)

# === ЗАПУСК С ПЕРЕЗАПУСКОМ ПРИ ДУБЛИКАТЕ ===
async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Бесконечный цикл перезапусков при дубликате
    while True:
        try:
            # Создаём свежий клиент
            client = create_client()
            
            async with client:
                logging.info("🚀 Бот запущен")
                # Запускаем спам-цикл
                await spam_loop(client)
                
                # Если вышли из спам-цикла - значит была ошибка
                logging.warning("⚠️ Спам-цикл завершён, перезапускаем бота...")
                
        except Exception as e:
            logging.error(f"❌ Критическая ошибка: {e}")
            logging.info("🔄 Перезапуск через 10 секунд...")
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
