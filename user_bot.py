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

# === СООБЩЕНИЕ (ТОЧНО КАК ТЫ НАПИСАЛ) ===
MESSAGE_TEXT = "продаю анрут чит магик 270 руб писать `@nikita1055`"
INTERVAL = 60  # 1 минута

# === КЛИЕНТ ===
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

app = create_client()

# === КНОПКА ===
def get_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 НАПИСАТЬ @nikita1055", callback_data="copy_nikita1055")]
    ])

# === ОБРАБОТЧИК КНОПКИ ===
@app.on_callback_query()
async def handle_copy(client, callback_query):
    if callback_query.data == "copy_nikita1055":
        await callback_query.answer("✅ @nikita1055 скопирован!", show_alert=True)
        await callback_query.message.reply("📋 Напиши: @nikita1055")

# === СПАМ-ЦИКЛ ===
async def spam_loop():
    while True:
        try:
            await app.send_message(
                CHANNEL_ID,
                MESSAGE_TEXT,
                reply_markup=get_button()
            )
            logging.info(f"✅ Отправлено в {datetime.now()}")
        except Exception as e:
            logging.error(f"❌ Ошибка: {e}")
            # Если дубликат сессии - пересоздаём клиент
            if "AUTH_KEY_DUPLICATED" in str(e):
                logging.warning("⚠️ Дубликат сессии! Пересоздаём клиент...")
                try:
                    await app.stop()
                    global app
                    app = create_client()
                    logging.info("✅ Клиент пересоздан!")
                except Exception as e2:
                    logging.error(f"❌ Ошибка при пересоздании: {e2}")
        
        await asyncio.sleep(INTERVAL)

# === ЗАПУСК ===
async def main():
    logging.basicConfig(level=logging.INFO)
    try:
        async with app:
            asyncio.create_task(spam_loop())
            logging.info("🚀 Бот запущен")
            await asyncio.Event().wait()
    except Exception as e:
        logging.error(f"❌ Ошибка при запуске: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
