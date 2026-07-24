import telebot
import os
from handlers.contact_handler import start_contacts_flow, handle_contact_name

# 1. Получаем токен из переменных окружения (обязательно для DADA)
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ Ошибка: Переменная окружения BOT_TOKEN не найдена!")

# Проверка формата токена (защита от заглушки)
if ":" not in TOKEN:
    raise ValueError("❌ Ошибка: Токен невалиден (нет двоеточия). Проверь настройки в DADA Console.")

bot = telebot.TeleBot(TOKEN)

print("🤖 Бот инициализирован. Ожидание команд...")

# 2. Регистрируем команды и хендлеры ЗДЕСЬ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот TVK Assistant. Используй /add_contacts для добавления.")

@bot.message_handler(commands=['add_contacts'])
def cmd_add_contacts(message):
    # Вызываем логику из handlers
    start_contacts_flow(message, bot)

# Пример хендлера для текста (если нужно ловить любой текст)
# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)

if __name__ == "__main__":
    try:
        # none_stop=True заставляет бота перезапускаться при ошибках сети
        bot.polling(none_stop=True, interval=1, timeout=20)
    except Exception as e:
        print(f"💥 Критическая ошибка бота: {e}")
