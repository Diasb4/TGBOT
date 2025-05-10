import os
import asyncio
import logging
from datetime import datetime, timedelta
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле.")

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Хранилище пользовательских дат
user_start_dates = {}

# Обработчики команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я буду напоминать тебе учиться через неделю после установленной даты.\n"
        "Установи дату начала: /setdate YYYY-MM-DD\n"
        "Удалить дату: /removedate"
    )

async def set_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Укажи дату в формате YYYY-MM-DD. Пример: /setdate 2024-10-01")
        return
    try:
        start_date = datetime.strptime(context.args[0], "%Y-%m-%d").date()
        user_start_dates[update.effective_chat.id] = start_date
        
        # Запланировать напоминание через неделю в 10:00
        reminder_time = start_date + timedelta(weeks=1)
        reminder_time = reminder_time.replace(hour=2, minute=28, second=0, microsecond=0)
        
        # Добавляем задачу в планировщик
        scheduler.add_job(send_reminder, "date", run_date=reminder_time, args=[update.effective_chat.id])
        
        await update.message.reply_text(f"Дата начала установлена: {start_date}. Напоминание будет отправлено {reminder_time}.")
    except ValueError:
        await update.message.reply_text("Неверный формат. Используй YYYY-MM-DD.")

async def remove_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if user_start_dates.pop(update.effective_chat.id, None):
        await update.message.reply_text("Напоминание удалено.")
    else:
        await update.message.reply_text("Дата ещё не была установлена.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Ошибка:", exc_info=context.error)
    if update and hasattr(update, "message") and update.message:
        await update.message.reply_text("Произошла ошибка. Попробуйте позже.")

# Напоминание
async def send_reminder(chat_id):
    await bot.send_message(chat_id, text="📚 Не забывай пройти квиз на https://learn.astanait.edu.kz!")

# Запуск приложения
async def run():
    global bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot = app.bot

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setdate", set_date))
    app.add_handler(CommandHandler("removedate", remove_date))
    app.add_error_handler(error_handler)

    # Запуск бота (создаёт event loop сам)
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio

    nest_asyncio.apply()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
