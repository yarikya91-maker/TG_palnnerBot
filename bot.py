from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import asyncio

# Flask для Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает! ✅"

# Получаем токен из Render → Environment
TOKEN = os.environ.get("BOT_TOKEN", "")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен и работает 💪")

# Асинхронный запуск Telegram-бота
async def run_bot():
    app_tg = ApplicationBuilder().token(TOKEN).build()
    app_tg.add_handler(CommandHandler("start", start))
    await app_tg.initialize()
    await app_tg.start()
    await app_tg.updater.start_polling()
    await asyncio.Event().wait()  # держим бота активным

# Flask + Telegram в одном цикле
def main():
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
