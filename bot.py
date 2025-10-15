import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Flask-приложение
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Flask жив, бот тоже должен быть онлайн!"

# Получаем токен из переменных окружения
TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    print("❌ Ошибка: BOT_TOKEN не найден в переменных окружения!")
else:
    print("✅ Токен найден, бот готов к запуску.")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот работает 💪")

def run_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    loop.run_until_complete(application.run_polling())

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 Flask запущен на порту {port}")
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    print("🚀 Запуск Telegram бота...")
    threading.Thread(target=run_bot).start()
    run_flask()
