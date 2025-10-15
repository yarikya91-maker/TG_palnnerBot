from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import threading
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "")

@app.route('/')
def home():
    return "Бот работает! ✅"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен и отвечает 💬")

def run_bot():
    if not TOKEN:
        print("❌ Ошибка: BOT_TOKEN не найден!")
        return

    print("🚀 Запускаем Telegram-бота...")

    # создаём отдельный event loop для потока
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    # запускаем polling в этом event loop
    loop.run_until_complete(application.run_polling())

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Flask запущен на порту {port}")
    app.run(host="0.0.0.0", port=port)

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    run_flask()з
