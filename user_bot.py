# user_bot.py
import asyncio
import logging
import random
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

CHANNEL_ID = "oxidebtatstvo"
ADMIN_ID = 1302493787
ADMIN_USERNAME = "nikita1055"

settings = {
    "message": "продаю анрут чит магик 270 руб писать @nikita1055",
    "interval": 60,
    "is_active": True,
}

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
def get_copy_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 НАПИСАТЬ @nikita1055", callback_data="copy_nikita1055")]
    ])

@app.on_callback_query()
async def handle_copy(client, callback_query):
    if callback_query.data == "copy_nikita1055":
        await callback_query.answer("✅ @nikita1055 скопирован!", show_alert=True)
        await callback_query.message.reply("📋 Напиши: @nikita1055")

# === УНИВЕРСАЛЬНЫЙ ОБРАБОТЧИК (БЕЗ ФИЛЬТРОВ!) ===
@app.on_message()
async def handle_all_messages(client, message):
    # Логируем ВСЕ сообщения
    logging.info(f"📩 ВСЕ СООБЩЕНИЯ: от {message.from_user.id} в чате {message.chat.id}: {message.text}")
    
    # Если сообщение из лички
    if message.chat.type == "private":
        # Если это команда от админа
        if message.from_user.id == ADMIN_ID and message.text:
            text = message.text.strip()
            
            # Обрабатываем команды
            if text == "/start":
                status = "✅ Активен" if settings["is_active"] else "❌ Остановлен"
                await message.reply(
                    f"🤖 Бот запущен\n\n"
                    f"• Интервал: {settings['interval']} сек\n"
                    f"• Статус: {status}\n\n"
                    f"📌 Используй /help"
                )
            
            elif text == "/help":
                await message.reply(
                    f"📚 Команды:\n\n"
                    f"/start — статус\n"
                    f"/help — помощь\n"
                    f"/status — настройки\n"
                    f"/set_text [текст] — сменить текст\n"
                    f"/set_interval [сек] — сменить интервал\n"
                    f"/start_spam — запустить\n"
                    f"/stop_spam — остановить\n"
                    f"/test — тест в канал"
                )
            
            elif text == "/status":
                await message.reply(
                    f"🔄 Активен: {'✅' if settings['is_active'] else '❌'}\n"
                    f"⏱ Интервал: {settings['interval']} сек\n"
                    f"📝 Текст: {settings['message']}"
                )
            
            elif text.startswith("/set_text "):
                new_text = text.replace("/set_text ", "").strip()
                if new_text:
                    settings["message"] = new_text
                    await message.reply(f"✅ Текст обновлён:\n{new_text}")
                else:
                    await message.reply("❌ Использование: /set_text [текст]")
            
            elif text.startswith("/set_interval "):
                try:
                    interval = int(text.replace("/set_interval ", "").strip())
                    if interval > 0:
                        settings["interval"] = interval
                        await message.reply(f"✅ Интервал: {interval} сек")
                    else:
                        await message.reply("❌ Минимум 1 секунда")
                except:
                    await message.reply("❌ Введите число")
            
            elif text == "/start_spam":
                settings["is_active"] = True
                await message.reply("✅ Спам запущен!")
            
            elif text == "/stop_spam":
                settings["is_active"] = False
                await message.reply("⛔ Спам остановлен!")
            
            elif text == "/test":
                try:
                    await app.send_message(CHANNEL_ID, settings["message"], reply_markup=get_copy_button())
                    await message.reply("✅ Тест отправлен в канал!")
                except Exception as e:
                    await message.reply(f"❌ Ошибка: {e}")
            
            else:
                await message.reply("❌ Неизвестная команда. Используй /help")
        else:
            # Если пишет не админ
            if message.from_user.id != ADMIN_ID:
                await message.reply("⛔ Доступ запрещен!")

# === СПАМ-ЦИКЛ ===
async def spam_loop():
    while True:
        if settings["is_active"]:
            try:
                await app.send_message(CHANNEL_ID, settings["message"], reply_markup=get_copy_button())
                logging.info(f"✅ Отправлено в {datetime.now()}")
                await asyncio.sleep(settings["interval"] + random.uniform(-2, 2))
            except Exception as e:
                logging.error(f"❌ Ошибка в спам-цикле: {e}")
                await asyncio.sleep(10)
        else:
            await asyncio.sleep(1)

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
