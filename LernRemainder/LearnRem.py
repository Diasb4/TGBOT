import logging
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

BOT_TOKEN = "7675249718:AAG8HqJTsUu2zKjfm7taw_9EIPzqeNFF71E"

logging.basicConfig(level=logging.INFO)

# Словарь: {chat_id: дата начала}
user_start_dates = {}

# Кнопки меню
def get_menu_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("Установить дату")],
        [KeyboardButton("Удалить дату")],
        [KeyboardButton("Проверить дату")],
        [KeyboardButton("Инструкции по настройке даты")]
    ], one_time_keyboard=True)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in user_start_dates:
        user_start_dates[chat_id] = None
    await update.message.reply_text(
        "Привет! Я помогу тебе установить напоминания на обучение. Используй меню ниже для начала.",
        reply_markup=get_menu_keyboard()
    )

# Команда /setdate YYYY-MM-DD
async def set_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        date_str = context.args[0]
        start_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        user_start_dates[update.effective_chat.id] = start_date
        await update.message.reply_text(f" Дата начала установлена: {start_date}. Напоминание будет каждую неделю от этой даты.")
    except (IndexError, ValueError):
        await update.message.reply_text(" Используй формат: /setdate YYYY-MM-DD (например: /setdate 2025-05-11)")

# Команда /removedate
async def remove_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in user_start_dates and user_start_dates[chat_id]:
        user_start_dates[chat_id] = None
        await update.message.reply_text(" Дата успешно удалена.")
    else:
        await update.message.reply_text(" У вас нет установленной даты.")

# Команда /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in user_start_dates and user_start_dates[chat_id]:
        await update.message.reply_text(f" Ваша стартовая дата: {user_start_dates[chat_id]}")
    else:
        await update.message.reply_text(" Вы не устанавливали дату. Введите /setdate YYYY-MM-DD")

# Команда /help - Инструкции по настройке даты
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    instructions = (
        " **Инструкции по настройке даты**:\n\n"
        "1. Чтобы установить дату, используйте команду `/setdate YYYY-MM-DD`.\n"
        "   Пример: `/setdate 2025-05-11`\n"
        "2. Для удаления установленной даты, используйте команду `/removedate`.\n"
        "3. Чтобы проверить свою текущую дату, используйте команду `/status`.\n\n"
        " Помните, что напоминания будут приходить каждую неделю от выбранной вами даты."
    )
    await update.message.reply_text(instructions)

# Проверка каждый день — отправлять ли напоминание
async def daily_check(app):
    today = datetime.now().date()
    for chat_id, start_date in user_start_dates.items():
        if start_date:
            delta_days = (today - start_date).days
            if delta_days >= 0 and delta_days % 7 == 0:
                try:
                    await app.bot.send_message(chat_id=chat_id, text=f"🔔 Напоминание! Сегодня {delta_days // 7 + 1}-я неделя.")
                except Exception as e:
                    logging.error(f"Ошибка при отправке: {e}")

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "установить дату" in text:
        await set_date(update, context)
    elif "удалить дату" in text:
        await remove_date(update, context)
    elif "проверить дату" in text:
        await status(update, context)
    elif "инструкции" in text:
        await help(update, context)

# Основной запуск
async def main():
    # Инициализация приложения
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Добавление обработчиков команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setdate", set_date))
    app.add_handler(CommandHandler("removedate", remove_date))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Инициализация асинхронного планировщика
    scheduler = AsyncIOScheduler()

    # Планирование задачи daily_check на 22:00 каждый день
    scheduler.add_job(
        daily_check,
        trigger="cron",
        hour=1,
        minute=3,
        args=[app]
    )

    # Запуск планировщика
    scheduler.start()

    print("✅ Бот запущен")

    # Запуск приложения
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    # Ожидание завершения (чтобы бот не завершился)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())