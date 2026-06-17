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
ADMIN_ID = 1302493787  # ТВОЙ ОСНОВНОЙ ID
ADMIN_USERNAME = "nikita1055"

# Настройки спама
settings = {
    "message": "продаю анрут чит магик 270 руб писать @nikita1055",
    "interval": 60,
    "is_active": True,
}

# === СОЗДАНИЕ КЛИЕНТА С ЗАЩИТОЙ ОТ ДУБЛИКАТА ===
def create_client():
    """Создает клиент с обработкой ошибки дубликата сессии"""
    if SESSION_STRING:
        return Client(
            name="user_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION_STRING,
            # Автоматически переподключается при ошибке
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

# === КНОПКА С КОПИРОВАНИЕМ ===
def get_copy_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "📋 НАПИСАТЬ @nikita1055",
            callback_data=f"copy_{ADMIN_USERNAME}"
        )]
    ])

# === ОБРАБОТЧИК НАЖАТИЯ НА КНОПКУ ===
@app.on_callback_query()
async def handle_copy(client, callback_query):
    if callback_query.data.startswith("copy_"):
        username = callback_query.data.replace("copy_", "")
        await callback_query.answer(
            f"@{username} скопирован! ✅",
            show_alert=True
        )
        await callback_query.message.reply(
            f"📋 **Юзернейм для связи:**\n\n"
            f"`@{username}`\n\n"
            f"👉 Нажми и удерживай, чтобы скопировать",
            parse_mode="Markdown"
        )

# === УНИВЕРСАЛЬНЫЙ ОБРАБОТЧИК КОМАНД (ДЛЯ ТВОЕГО ОСНОВНОГО ID) ===
@app.on_message(filters.private)
async def handle_commands(client, message):
    # Проверяем, что сообщение от твоего основного аккаунта
    if message.from_user.id != ADMIN_ID:
        await message.reply("⛔ Доступ запрещен!")
        return
    
    text = message.text.strip()
    
    # Команда /start
    if text == "/start":
        status = "✅ Активен" if settings["is_active"] else "❌ Остановлен"
        await message.reply(
            f"🤖 *Бот управления*\n\n"
            f"• Интервал: {settings['interval']} сек\n"
            f"• Статус: {status}\n\n"
            f"📌 Используй /help для списка команд",
            parse_mode="Markdown"
        )
    
    # Команда /help
    elif text == "/help":
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
    
    # Команда /status
    elif text == "/status":
        await message.reply(
            f"📊 *Статус*\n\n"
            f"🔄 Активен: {'✅ Да' if settings['is_active'] else '❌ Нет'}\n"
            f"⏱ Интервал: {settings['interval']} сек\n"
            f"📝 Текст: `{settings['message']}`",
            parse_mode="Markdown"
        )
    
    # Команда /set_text
    elif text.startswith("/set_text "):
        new_text = text.replace("/set_text ", "").strip()
        if not new_text:
            await message.reply("❌ Использование: `/set_text [новый текст]`", parse_mode="Markdown")
            return
        settings["message"] = new_text
        await message.reply(f"✅ Текст обновлён!\n\n`{new_text}`", parse_mode="Markdown")
    
    # Команда /set_interval
    elif text.startswith("/set_interval "):
        try:
            interval = int(text.replace("/set_interval ", "").strip())
            if interval < 1:
                await message.reply("❌ Интервал должен быть > 0")
                return
            settings["interval"] = interval
            await message.reply(f"✅ Интервал: {interval} сек")
        except ValueError:
            await message.reply("❌ Введите число!")
    
    # Команда /start_spam
    elif text == "/start_spam":
        if settings["is_active"]:
            await message.reply("⚠️ Спам уже запущен!")
            return
        settings["is_active"] = True
        await message.reply("✅ Спам запущен!")
    
    # Команда /stop_spam
    elif text == "/stop_spam":
        settings["is_active"] = False
        await message.reply("⛔ Спам остановлен!")
    
    # Команда /test
    elif text == "/test":
        try:
            await app.send_message(
                CHANNEL_ID,
                settings["message"],
                reply_markup=get_copy_button()
            )
            await message.reply("✅ Тест отправлен в канал!")
        except Exception as e:
            await message.reply(f"❌ Ошибка: {e}")
    
    # Неизвестная команда
    else:
        await message.reply("❌ Неизвестная команда. Используй /help")

# === ОСНОВНОЙ ЦИКЛ СПАМА ===
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
                logging.error(f"❌ Ошибка в спам-цикле: {e}")
                # Если ошибка связана с сессией - пробуем переподключиться
                if "AUTH_KEY_DUPLICATED" in str(e):
                    logging.warning("⚠️ Обнаружен дубликат сессии, пересоздаём клиент...")
                    # Пересоздаём клиент
                    global app
                    app = create_client()
                await asyncio.sleep(10)
        else:
            await asyncio.sleep(1)

# === ЗАПУСК ===
async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Обработка ошибки дубликата при старте
    try:
        async with app:
            asyncio.create_task(spam_loop())
            logging.info("🚀 Бот запущен")
            await asyncio.Event().wait()
    except Exception as e:
        if "AUTH_KEY_DUPLICATED" in str(e):
            logging.error("❌ Ошибка дубликата сессии при старте!")
            logging.error("👉 Удали все сессии в Telegram (Настройки → Устройства)")
            logging.error("👉 И пересоздай сессию заново через Termux")
        raise

if __name__ == "__main__":
    asyncio.run(main())
