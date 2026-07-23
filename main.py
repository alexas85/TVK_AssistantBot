# main.py
import telebot
from config import BOT_TOKEN
from database import run_migration, get_connection  # 1. Импортируем функцию миграции
from handlers.status_handler import process_status_callback, show_status_keyboard, State

# --- ШАГ 1: ЗАПУСКАЕМ МИГРАЦИЮ ПРИ СТАРТЕ (ДО создания бота!) ---
print("🚀 Запуск миграций базы данных...")
try:
    run_migration()  # 2. Вызываем правильно: имя_функции() без дефисов
    print("✅ Миграции успешно применены.")
except Exception as e:
    print(f"❌ Ошибка при миграции: {e}")
    # Решать, останавливать ли бота при ошибке миграции, зависит от тебя.
    # Сейчас бот продолжит запускаться, но в логах будет ошибка.
# ------------------------------------------------------------------

# Создаем бота
bot = telebot.TeleBot(BOT_TOKEN)

@bot.callback_query_handler(func=lambda call: call.data.startswith('status_') or call.data == 'cancel_status')
def callback_status(call):
    from database import get_connection
    conn = get_connection()
    process_status_callback(call, bot, conn)

@bot.message_handler(commands=['set_status'])
def cmd_set_status(message):
    show_status_keyboard(message, bot)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Бот запущен. Используй /set_status для выбора статуса объекта.")

print("🤖 Бот готов к работе!")
bot.polling(none_stop=True)
