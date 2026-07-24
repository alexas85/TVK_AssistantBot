# handlers/contact_handler.py

def start_contacts_flow(message, bot):
    """Логика начала сбора контактов"""
    bot.send_message(
        message.chat.id,
        "👋 Привет! Давай добавим новый контакт.\n"
        "Напиши название компании или имя человека:"
    )
    # Тут можно сохранить состояние пользователя в БД или Redis

def handle_contact_name(message, bot):
    """Логика обработки введенного имени"""
    name = message.text
    bot.send_message(
        message.chat.id,
        f"✅ Отлично! Ты ввел: {name}.\n"
        "Теперь укажи телефон или нажми /cancel:"
    )
