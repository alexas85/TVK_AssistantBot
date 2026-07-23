# main.py
import telebot
from handlers.status_handler import process_status_callback, show_status_keyboard, State
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

@bot.callback_query_handler(func=lambda call: call.data.startswith('status_') or call.data == 'cancel_status')
def callback_status(call):
    # Импортируем подключение к БД здесь или передаем через глобальную переменную
    from database import get_connection
    conn = get_connection()
    process_status_callback(call, bot, conn)

@bot.message_handler(commands=['set_status'])
def cmd_set_status(message):
    show_status_keyboard(message, bot)
