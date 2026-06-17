# user_bot.py (исправленная версия)
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

# ✅ ИСПРАВЛЕНО: используем username канала (без https://t.me/)
CHANNEL_ID = "oxidebtatstvo"  # или "@oxidebtatstvo" - тоже работает
ADMIN_ID = 1302493787
ADMIN_USERNAME = "nikita1055"

settings = {
    "message": "продаю анрут чит магик 270 руб писать @nikita1055",
    "interval": 60,
    "is_active": True,
}

# === КЛИЕНТ ===
if SESSION_STRING:
    app = Client(
        name="user_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STRING,
    )
else:
    app = Client(
        "my_user_bot",
        api_id=API_ID,
        api_hash=API_HASH,
    )

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

# === КОМАНДЫ ===
@app.on_message(filters.private & filters.command("help"))
async def help_command(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.reply(
        f"📚 Команды:\n"
        f"/start — статус\n"
        f"/help — помощь\n"
        f"/status — настройки\n"
        f"/set_text [текст] — сменить текст\n"
        f"/set_interval [сек] — сменить интервал\n"
        f"/start_spam — запустить\n"
        f"/stop_spam — остановить\n"
        f"/test — тест в канал"
    )

@app.on_message(filters.private & filters.command("start"))
async def start_command(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    status = "✅ Активен" if settings["is_active"] else "❌ Остановлен"
    await message.reply(f"🤖 Бот запущен\nИнтервал: {settings['interval']} сек\nСтатус: {status}")

@app.on_message(filters.private & filters.command("set_text"))
async def set_text(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        await message.reply("❌ Использование: /set_text [текст]")
        return
    settings["message"] = parts[1]
    await message.reply(f"✅ Текст обновлён:\n{parts[1]}")

@app.on_message(filters.private & filters.command("set_interval"))
async def set_interval(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        await message.reply("❌ Использование: /set_interval [сек]")
        return
    try:
        interval = int(parts[1])
        if interval < 1:
            await message.reply("❌ Минимум 1 секунда")
            return
        settings["interval"] = interval
        await message.reply(f"✅ Интервал: {interval} сек")
    except ValueError:
        await message.reply("❌ Введите число")

@app.on_message(filters.private & filters.command("start_spam"))
async def start_spam(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    settings["is_active"] = True
    await message.reply("✅ Спам запущен")

@app.on_message(filters.private & filters.command("stop_spam"))
async def stop_spam(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    settings["is_active"] = False
    await message.reply("⛔ Спам остановлен")

@app.on_message(filters.private & filters.command("status"))
async def status(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.reply(
        f"🔄 Активен: {'✅' if settings['is_active'] else '❌'}\n"
        f"⏱ Интервал: {settings['interval']} сек\n"
        f"📝 Текст: {settings['message']}"
    )

@app.on_message(filters.private & filters.command("test"))
async def test_send(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        await app.send_message(CHANNEL_ID, settings["message"], reply_markup=get_copy_button())
        await message.reply("✅ Тест отправлен")
    except Exception as e:
        await message.reply(f"❌ Ошибка: {e}")

# === ЦИКЛ СПАМА ===
async def spam_loop():
    while True:
        if settings["is_active"]:
            try:
                await app.send_message(CHANNEL_ID, settings["message"], reply_markup=get_copy_button())
                logging.info(f"✅ Отправлено {datetime.now()}")
                await asyncio.sleep(settings["interval"] + random.uniform(-2, 2))
            except Exception as e:
                logging.error(f"❌ Ошибка: {e}")
                await asyncio.sleep(10)
        else:
            await asyncio.sleep(1)

# === ЗАПУСК ===
async def main():
    logging.basicConfig(level=logging.INFO)
    async with app:
        asyncio.create_task(spam_loop())
        logging.info("🚀 Бот запущен")
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
