from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import threading
import asyncio

app = Flask(__name__)

# Получаем токен из переменных окружения (Render → Environment)
TOKEN = os.environ.get("BOT_TOKEN", "")

@app.route('/')
def home():
    return "✅ Бот работает и Flask жив!"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот успешно запущен и отвечает 💪")

def run_bot():
    print("🚀 Проверка токена...")
    if not TOKEN:
        print("❌ Ошибка: токен отсутствует! Проверь переменные окружения в Render (BOT_TOKEN).")
        return

    print("✅ Токен найден, создаем Telegram приложение...")

    # Для Python 3.10+ создаем отдельный event loop
    asyncio.set_event_loop(asyncio.new_event_loop())
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    print("🟢 Запуск Telegram polling...")
    try:
        application.run_polling()
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Flask запущен на порту {port}")
    app.run(host="0.0.0.0", port=port)

if __name__ == '__main__':
    print("🚀 Запускаем Telegram-бота и Flask одновременно...")
    threading.Thread(target=run_bot).start()
    run_flask()
