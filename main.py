import telebot
import os
from handlers.objects import register_objects_handlers
from handlers.status_handler import register_status_handlers
from database import run_migration

# 1. Получаем токен из переменных окружения (обязательно для DADA Console)
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ Ошибка: Переменная окружения BOT_TOKEN не найдена!")

# Проверка формата токена (защита от заглушки)
if ":" not in TOKEN:
    raise ValueError("❌ Ошибка: Токен невалиден (нет двоеточия). Проверь настройки в DADA Console.")

bot = telebot.TeleBot(TOKEN)

# 2. Применяем миграции БД при старте
run_migration()

# 3. Регистрируем хендлеры
register_status_handlers(bot)
register_objects_handlers(bot)

print("🤖 Бот инициализирован. Ожидание команд...")

if __name__ == "__main__":
    try:
        # none_stop=True заставляет бота перезапускаться при ошибках сети
        bot.polling(none_stop=True, interval=1, timeout=20)
    except Exception as e:
        print(f"💥 Критическая ошибка бота: {e}")