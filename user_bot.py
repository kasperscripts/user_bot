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

CHANNEL_ID = "oxidebtatstvo"

# === СООБЩЕНИЕ ===
MESSAGE_TEXT = "продаю анрут чит магик 270 руб писать `@nikita1055`"

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

# === СОЗДАЁМ КЛИЕНТ ===
app = create_client()

# === КНОПКА ===
def get_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 НАПИСАТЬ @nikita1055", callback_data="copy_nikita1055")]
    ])

# === ОБРАБОТЧИК СООБЩЕНИЙ В КАНАЛЕ ===
@app.on_message(filters.chat(CHANNEL_ID) & filters.incoming)
async def handle_channel_messages(client, message: Message):
    # Игнорируем свои же сообщения
    if message.from_user and message.from_user.is_self:
        return
    
    logging.info(f"📩 Новое сообщение в канале от {message.from_user.id if message.from_user else 'аноним'}")
    
    # Отправляем НОВОЕ сообщение (НЕ ответ)
    try:
        await client.send_message(
            CHANNEL_ID,
            MESSAGE_TEXT,
            reply_markup=get_button()
        )
        logging.info(f"✅ Сообщение отправлено после сообщения {message.id}")
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
    
    while True:
        try:
            async with app:
                logging.info("🚀 Бот запущен. Ожидаю сообщения в канале...")
                await asyncio.Event().wait()
                
        except Exception as e:
            logging.error(f"❌ Критическая ошибка: {e}")
            logging.info("🔄 Перезапуск через 10 секунд...")
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
