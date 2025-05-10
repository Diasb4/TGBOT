import os
import logging
from datetime import datetime
import pytz
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
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
        "Привет! Я буду напоминать тебе учиться каждый день.\n"
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
        await update.message.reply_text(f"Дата начала установлена: {start_date}")
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
async def send_reminder(app):
    for chat_id, start_date in user_start_dates.items():
        days = (datetime.now(pytz.timezone("Asia/Almaty")).date() - start_date).days + 1  # с учётом часового пояса
        await app.bot.send_message(chat_id, text=f"📚 Не забывай пройти квиз на https://learn.astanait.edu.kz !")

# Запуск приложения
async def run():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setdate", set_date))
    app.add_handler(CommandHandler("removedate", remove_date))
    app.add_error_handler(error_handler)

    # Планировщик
    scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Almaty"))  # Устанавливаем таймзону
    scheduler.add_job(send_reminder, "cron", day_of_week="mon", hour=1, minute=42, args=[app])  # Напоминание каждую неделю в понедельник в 1:42
    scheduler.start()
    logger.info("Планировщик запущен, напоминания настроены.")

    # Запуск бота с long polling
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio

    nest_asyncio.apply()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
