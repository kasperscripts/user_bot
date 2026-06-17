# user_bot.py
import asyncio
import logging
import os
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from dotenv import load_dotenv

load_dotenv()

# === КОНФИГ ===
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

CHANNEL_ID = "@oxidebtatstvo"  # Пробуем с @

# === СООБЩЕНИЕ ===
MESSAGE_TEXT = "продаю анрут чит магик 270 руб писать `@nikita1055`"

# === СОЗДАЁМ КЛИЕНТ ===
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

# === ТЕСТОВЫЙ ОБРАБОТЧИК (ЛОГИРУЕТ ВСЁ) ===
@app.on_message()
async def log_all(client, message: Message):
    logging.info(f"🔔 ВСЕ СООБЩЕНИЯ: чат={message.chat.id}, тип={message.chat.type}, текст={message.text}")

# === ОБРАБОТЧИК СООБЩЕНИЙ В КАНАЛЕ ===
@app.on_message(filters.chat(CHANNEL_ID) & filters.incoming)
async def handle_channel_messages(client, message: Message):
    logging.info(f"📩 КАНАЛ: сообщение от {message.from_user.id if message.from_user else 'аноним'}")
    
    # Игнорируем свои же сообщения
    if message.from_user and message.from_user.is_self:
        logging.info("⏭️ Пропускаем своё сообщение")
        return
    
    try:
        await client.send_message(
            CHANNEL_ID,
            MESSAGE_TEXT,
            reply_markup=get_button()
        )
        logging.info(f"✅ Сообщение отправлено!")
    except Exception as e:
        logging.error(f"❌ Ошибка при отправке: {e}")

# === ОБРАБОТЧИК КНОПКИ ===
@app.on_callback_query()
async def handle_copy(client, callback_query: CallbackQuery):
    if callback_query.data == "copy_nikita1055":
        await callback_query.answer("✅ @nikita1055 скопирован!", show_alert=True)
        await callback_query.message.reply("📋 Напиши: @nikita1055")

# === ЗАПУСК ===
async def main():
    logging.basicConfig(level=logging.INFO)
    
    try:
        async with app:
            logging.info(f"🚀 Бот запущен. Отслеживаю канал: {CHANNEL_ID}")
            await asyncio.Event().wait()
    except Exception as e:
        logging.error(f"❌ Критическая ошибка: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
