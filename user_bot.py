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

CHANNEL_ID = "oxidebtatstvo"  # или "@oxidebtatstvo"
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

# === КНОПКА С КОПИРОВАНИЕМ (РАБОТАЕТ!) ===
def get_copy_button():
    return InlineKeyboardMarkup([
        # Кнопка с callback - при нажатии копируется юзернейм
        [InlineKeyboardButton(
            "📋 НАПИСАТЬ @nikita1055",
            callback_data=f"copy_{ADMIN_USERNAME}"
        )],
        # Дополнительная кнопка с прямой ссылкой (если пропускает)
        [InlineKeyboardButton(
            "💬 НАПИСАТЬ В ЛС",
            url=f"https://t.me/{ADMIN_USERNAME}"
        )]
    ])

# === ОБРАБОТЧИК НАЖАТИЯ НА КНОПКУ ===
@app.on_callback_query()
async def handle_copy(client, callback_query):
    if callback_query.data.startswith("copy_"):
        username = callback_query.data.replace("copy_", "")
        
        # 1. Показываем алерт с юзернеймом
        await callback_query.answer(
            f"@{username} скопирован! ✅",
            show_alert=True
        )
        
        # 2. Отправляем сообщение с юзернеймом (его можно скопировать)
        await callback_query.message.reply(
            f"📋 **Юзернейм для связи:**\n\n"
            f"`@{username}`\n\n"
            f"👉 Нажми и удерживай, чтобы скопировать",
            parse_mode="Markdown"
        )
        
        # 3. Отправляем отдельное сообщение только с юзернеймом
        await callback_query.message.reply(
            f"@{username}",
            parse_mode="Markdown"
        )

# === КОМАНДЫ (РАБОТАЮТ ТОЛЬКО ДЛЯ ТЕБЯ) ===
@app.on_message(filters.private & filters.command("start"))
async def start_command(client, message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("⛔ Доступ запрещен!")
        return
    status = "✅ Активен" if settings["is_active"] else "❌ Остановлен"
    await message.reply(
        f"🤖 *Бот запущен*\n\n"
        f"• Интервал: {settings['interval']} сек\n"
        f"• Статус: {status}\n\n"
        f"📌 Используй /help для списка команд",
        parse_mode="Markdown"
    )

@app.on_message(filters.private & filters.command("help"))
async def help_command(client, message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("⛔ Доступ запрещен!")
        return
    await message.reply(
        f"📚 *Команды:*\n\n"
        f"/start — статус бота\n"
        f"/help — это сообщение\n"
        f"/status — текущие настройки\n"
        f"/set_text [текст] — изменить текст\n"
        f"/set_interval [сек] — изменить интервал\n"
        f"/start_spam — запустить рассылку\n"
        f"/stop_spam — остановить рассылку\n"
        f"/test — тест в канал\n\n"
        f"📊 *Сейчас:*\n"
        f"• Текст: `{settings['message']}`\n"
        f"• Интервал: {settings['interval']} сек\n"
        f"• Статус: {'✅ Активен' if settings['is_active'] else '❌ Остановлен'}",
        parse_mode="Markdown"
    )

@app.on_message(filters.private & filters.command("status"))
async def status(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.reply(
        f"📊 *Статус*\n\n"
        f"🔄 Активен: {'✅ Да' if settings['is_active'] else '❌ Нет'}\n"
        f"⏱ Интервал: {settings['interval']} сек\n"
        f"📝 Текст: `{settings['message']}`",
        parse_mode="Markdown"
    )

@app.on_message(filters.private & filters.command("set_text"))
async def set_text(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        await message.reply("❌ Использование: `/set_text [новый текст]`", parse_mode="Markdown")
        return
    settings["message"] = parts[1]
    await message.reply(f"✅ Текст обновлён!\n\n`{parts[1]}`", parse_mode="Markdown")

@app.on_message(filters.private & filters.command("set_interval"))
async def set_interval(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        await message.reply("❌ Использование: `/set_interval [секунды]`", parse_mode="Markdown")
        return
    try:
        interval = int(parts[1])
        if interval < 1:
            await message.reply("❌ Интервал должен быть > 0")
            return
        settings["interval"] = interval
        await message.reply(f"✅ Интервал: {interval} сек")
    except ValueError:
        await message.reply("❌ Введите число!")

@app.on_message(filters.private & filters.command("start_spam"))
async def start_spam(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    if settings["is_active"]:
        await message.reply("⚠️ Спам уже запущен!")
        return
    settings["is_active"] = True
    await message.reply("✅ Спам запущен!")

@app.on_message(filters.private & filters.command("stop_spam"))
async def stop_spam(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    settings["is_active"] = False
    await message.reply("⛔ Спам остановлен!")

@app.on_message(filters.private & filters.command("test"))
async def test_send(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        await app.send_message(
            CHANNEL_ID,
            settings["message"],
            reply_markup=get_copy_button()
        )
        await message.reply("✅ Тест отправлен в канал!")
    except Exception as e:
        await message.reply(f"❌ Ошибка: {e}")

# === ОСНОВНОЙ ЦИКЛ ===
async def spam_loop():
    while True:
        if settings["is_active"]:
            try:
                await app.send_message(
                    CHANNEL_ID,
                    settings["message"],
                    reply_markup=get_copy_button()
                )
                logging.info(f"✅ Отправлено в {datetime.now()}")
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
