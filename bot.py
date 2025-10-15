import os
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))

if not BOT_TOKEN:
    raise ValueError("❌ Ошибка: BOT_TOKEN не найден в переменных окружения!")

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask работает, бот активен!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот запущен и готов работать 🚀")

async def run_bot():
    print("🚀 Запуск Telegram бота...")
    app_telegram = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    app_telegram.add_handler(CommandHandler("start", start))

    await app_telegram.run_polling(
        allowed_updates=Update.ALL_TYPES
    )

async def main():
    # Запуск Flask и Telegram в одном цикле
    from threading import Thread

    def run_flask():
        print(f"🌐 Flask запущен на порту {PORT}")
        app.run(host="0.0.0.0", port=PORT)

    Thread(target=run_flask, daemon=True).start()

    await run_bot()

if __name__ == "__main__":
    asyncio.run(main())
