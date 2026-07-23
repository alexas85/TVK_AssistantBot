# main.py
import telebot
from config import BOT_TOKEN
from database import run_migration, get_connection
# Импортируем функции, но НЕ декораторы напрямую, если они внутри функций
from handlers.status_handler import show_status_keyboard, process_status_callback, State
# Для контактов нам нужно зарегистрировать хендлеры вручную или убедиться, что они видят объект bot

# 1. Миграция
print("🚀 Запуск миграций...")
run_migration()

# 2. Создаем бота
bot = telebot.TeleBot(BOT_TOKEN)

# --- РЕГИСТРАЦИЯ ХЕНДЛЕРОВ ДЛЯ КОНТАКТОВ (ВРУЧНУЮ) ---
# Так как в contact_handler.py мы использовали декораторы без привязки к bot,
# нам нужно либо переписать их, либо зарегистрировать явно.
# Самый простой способ для твоего случая - перенести логику контактов прямо сюда
# ИЛИ использовать утилиту регистрации.
# Но чтобы не усложнять, давай сделаем самый надежный вариант:
# В handlers/contact_handler.py убираем декораторы и регистрируем их здесь.

# Если ты оставил декораторы в contact_handler.py как в коде выше, они НЕ сработают,
# потому что не знают про переменную 'bot'.
# ИСПРАВЛЕНИЕ: Используй этот блок вместо импортов хендлеров контактов:

import handlers.contact_handler as contact_h
# Перепривязываем хендлеры к нашему экземпляру бота
bot.message_handler(commands=['add_contacts'])(contact_h.start_contacts_flow)
bot.message_handler(func=lambda msg: contact_h.user_states.get(msg.from_user.id) == contact_h.ContactState.WAIT_COMPANY)(contact_h.process_company)
bot.message_handler(func=lambda msg: contact_h.user_states.get(msg.from_user.id) == contact_h.ContactState.WAIT_POSITION)(contact_h.process_position)
bot.message_handler(func=lambda msg: contact_h.user_states.get(msg.from_user.id) == contact_h.ContactState.WAIT_NAME)(contact_h.process_name)
bot.message_handler(func=lambda msg: contact_h.user_states.get(msg.from_user.id) == contact_h.ContactState.WAIT_PHONE)(contact_h.process_phone)
bot.callback_query_handler(func=lambda call: call.data in ['save_contact', 'cancel_contact'])(contact_h.confirm_contact_action)

# --- РЕГИСТРАЦИЯ ХЕНДЛЕРОВ ДЛЯ СТАТУСОВ ---
bot.callback_query_handler(func=lambda call: call.data.startswith('status_') or call.data == 'cancel_status')(
    lambda call: process_status_callback(call, bot, get_connection())
)

bot.message_handler(commands=['set_status'])(lambda msg: show_status_keyboard(msg, bot))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Бот запущен. Используй /set_status или /add_contacts.")

print("🤖 Бот готов к работе!")
bot.polling(none_stop=True)
