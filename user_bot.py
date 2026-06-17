# user_bot.py
import asyncio
import logging
import os
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()

# === КОНФИГ ===
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

# ⚠️ БЕЗ @ (как работало)
CHANNEL_ID = "oxidebtatstvo"

MESSAGE_TEXT = "продаю анрут чит магик 270 руб писать `@nikita1055`"

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

# === ОБРАБОТЧИК СООБЩЕНИЙ В КАНАЛЕ ===
@app.on_message(filters.chat(CHANNEL_ID) & filters.incoming)
async def handle_channel_messages(client, message):
    # Не отвечаем самому себе
    if message.from_user and message.from_user.is_self:
        return

    logging.info(f"📩 Новое сообщение в канале")

    try:
        await client.send_message(
            CHANNEL_ID,
            MESSAGE_TEXT,
            reply_markup=get_button()
        )
        logging.info(f"✅ Отправлено в {datetime.now()}")
    except Exception as e:
        logging.error(f"❌ Ошибка: {e}")

# === ЗАПУСК ===
async def main():
    logging.basicConfig(level=logging.INFO)
    async with app:
        logging.info(f"🚀 Бот запущен. Канал: {CHANNEL_ID}")
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
