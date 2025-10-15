import os
import threading
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Flask сервер
app = Flask(__name__)

# Токен бота
TOKEN = os.environ.get("BOT_TOKEN")

@app.route('/')
def home():
    return "Бот запущен и работает ✅"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот работает 💪")

# Запуск Telegram бота
def run_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

# Запуск Flask сервера
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Flask запущен на порту {port}")
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    print("🚀 Запускаем Telegram-бота...")
    threading.Thread(target=run_bot).start()
    run_flask()
