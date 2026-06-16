# user_bot.py
import asyncio
import logging
import random
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Конфигурация
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION_NAME = 'my_user_bot'
CHANNEL_ID = 'https://t.me/oxidebtatstvo'
ADMIN_ID = 1302493787
ADMIN_USERNAME = 'nikita1055'

# Настройки
settings = {
    'message': 'продаю анрут чит магик 270 руб писать @nikita1055',
    'interval': 60,
    'is_active': True
}

app = Client(
    SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH
)

# Кнопка с копированием юзернейма
def get_copy_button():
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text="📋 НАПИСАТЬ @nikita1055",
            callback_data=f"copy_{ADMIN_USERNAME}"
        )]
    ])
    return keyboard

# Обработчик нажатия на кнопку
@app.on_callback_query()
async def handle_copy(client, callback_query):
    if callback_query.data.startswith("copy_"):
        username = callback_query.data.replace("copy_", "")
        
        # Показываем уведомление с юзернеймом
        await callback_query.answer(
            f"@{username} скопирован! ✨",
            show_alert=True
        )
        
        # Отправляем юзернейм для копирования
        await callback_query.message.reply(
            f"📋 Напиши: @{username}",
            parse_mode='Markdown'
        )

# Команда /help
@app.on_message(filters.private & filters.command('help'))
async def help_command(client, message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("⛔ Доступ запрещен!")
        return
    
    help_text = """
📚 *Доступные команды:*

🤖 *Управление ботом:*
/start - Показать статус бота
/help - Показать это сообщение
/status - Текущие настройки

✏️ *Настройка сообщения:*
/set_text [текст] - Изменить текст сообщения
Пример: `/set_text продаю анрут чит магик 270 руб`

⏱ *Настройка интервала:*
/set_interval [секунды] - Изменить интервал отправки
Пример: `/set_interval 30`

▶️ *Управление спамом:*
/start_spam - Запустить рассылку
/stop_spam - Остановить рассылку

🧪 *Тестирование:*
/test - Отправить тестовое сообщение в канал

📊 *Текущие настройки:*
• Текст: `{settings['message']}`
• Интервал: {settings['interval']} сек
• Статус: {'✅ Активен' if settings['is_active'] else '❌ Остановлен'}

💡 *Важно:* 
Все команды доступны только владельцу бота!
"""
    
    await message.reply(
        help_text.format(
            message=settings['message'],
            interval=settings['interval'],
            is_active=settings['is_active']
        ),
        parse_mode='Markdown'
    )

# Команды управления
@app.on_message(filters.private & filters.command('start'))
async def start_command(client, message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("⛔ Доступ запрещен!")
        return
    
    status = "✅ Активен" if settings['is_active'] else "❌ Остановлен"
    await message.reply(
        f"🤖 *Юзер-бот активирован!*\n\n"
        f"📊 Текущие настройки:\n"
        f"• Текст: {settings['message']}\n"
        f"• Интервал: {settings['interval']} сек\n"
        f"• Статус: {status}\n\n"
        f"🔧 Команды:\n"
        f"/help - Все команды\n"
        f"/set_text [текст] - Изменить текст\n"
        f"/set_interval [сек] - Изменить интервал\n"
        f"/start_spam - Запустить спам\n"
        f"/stop_spam - Остановить спам\n"
        f"/status - Статус бота\n"
        f"/test - Тестовая отправка",
        parse_mode='Markdown'
    )

@app.on_message(filters.private & filters.command('set_text'))
async def set_text(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        await message.reply("❌ Использование: /set_text [новый текст]")
        return
    
    settings['message'] = parts[1]
    await message.reply(f"✅ Текст обновлен!\n\n{parts[1]}")

@app.on_message(filters.private & filters.command('set_interval'))
async def set_interval(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        await message.reply("❌ Использование: /set_interval [секунды]")
        return
    
    try:
        interval = int(parts[1])
        if interval < 1:
            await message.reply("❌ Интервал должен быть > 0")
            return
        settings['interval'] = interval
        await message.reply(f"✅ Интервал: {interval} сек")
    except ValueError:
        await message.reply("❌ Введите число!")

@app.on_message(filters.private & filters.command('start_spam'))
async def start_spam(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    
    if settings['is_active']:
        await message.reply("⚠️ Спам уже запущен!")
        return
    
    settings['is_active'] = True
    await message.reply("✅ Спам запущен!")

@app.on_message(filters.private & filters.command('stop_spam'))
async def stop_spam(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    
    settings['is_active'] = False
    await message.reply("⛔ Спам остановлен!")

@app.on_message(filters.private & filters.command('status'))
async def status(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    
    status = "✅ Да" if settings['is_active'] else "❌ Нет"
    await message.reply(
        f"📊 *Статус*\n\n"
        f"🔄 Активен: {status}\n"
        f"⏱ Интервал: {settings['interval']} сек\n"
        f"📝 Текст: {settings['message']}",
        parse_mode='Markdown'
    )

@app.on_message(filters.private & filters.command('test'))
async def test_send(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        await app.send_message(
            chat_id=CHANNEL_ID,
            text=settings['message'],
            reply_markup=get_copy_button()
        )
        await message.reply("✅ Тестовое сообщение отправлено!")
    except Exception as e:
        await message.reply(f"❌ Ошибка: {e}")

# Основной цикл отправки
async def spam_loop():
    while True:
        if settings['is_active']:
            try:
                # Отправка в канал
                await app.send_message(
                    chat_id=CHANNEL_ID,
                    text=settings['message'],
                    reply_markup=get_copy_button()
                )
                logging.info(f"✅ Сообщение отправлено в {datetime.now()}")
                
                # Рандомная задержка
                await asyncio.sleep(settings['interval'] + random.uniform(-2, 2))
                
            except Exception as e:
                logging.error(f"❌ Ошибка: {e}")
                await app.send_message(
                    ADMIN_ID,
                    f"⚠️ Ошибка отправки!\n{str(e)}"
                )
                await asyncio.sleep(10)
        else:
            await asyncio.sleep(1)

# Запуск
async def main():
    logging.basicConfig(level=logging.INFO)
    
    async with app:
        asyncio.create_task(spam_loop())
        logging.info("🚀 Бот запущен!")
        await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
