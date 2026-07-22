import telebot
import config
from handlers import objects as obj_handlers
from database import init_db

if __name__ == "__main__":
    init_db()
    bot = telebot.TeleBot(config.BOT_TOKEN, parse_mode="HTML")

    obj_handlers.register_objects_handlers(bot)

    print("TVK AssistantBot запущен...")
    bot.infinity_polling()
