import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "")

@app.route('/')
def home():
    return "✅ Flask работает! Telegram бот тоже должен быть активен."

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает 💪")

async def run_bot():
    if not TOKEN:
        print("❌ Ошибка: токен отсутствует! Проверь переменные окружения (BOT_TOKEN).")
        return

    print("🚀 Запуск Telegram бота...")
    app_telegram = ApplicationBuilder().token(TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    await app_telegram.initialize()
    await app_telegram.start()
    print("✅ Бот успешно запущен (polling)!")
    await app_telegram.updater.start_polling()
    await app_telegram.updater.wait_until_closed()

async def run_flask():
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Flask запущен на порту {port}")
    # Flask блокирует поток, поэтому запускаем его в отдельном executor
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: app.run(host="0.0.0.0", port=port))

async def main():
    # Запускаем Flask и Telegram одновременно
    await asyncio.gather(run_flask(), run_bot())

if __name__ == "__main__":
    asyncio.run(main())
