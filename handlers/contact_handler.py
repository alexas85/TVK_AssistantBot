# handlers/contact_handler.py
from telebot import types


class ContactState:
    WAIT_COMPANY = "wait_company"
    WAIT_POSITION = "wait_position"
    WAIT_NAME = "wait_name"
    WAIT_PHONE = "wait_phone"
    CONFIRM = "confirm"


# Временное хранилище данных, которые пользователь вводит прямо сейчас
user_temp_data = {}


@bot.message_handler(commands=['add_contacts'])
def start_contacts(message):
    user_id = message.from_user.id
    user_temp_data[user_id] = {}
    user_states[user_id] = ContactState.WAIT_COMPANY
    bot.send_message(user_id, "🏢 Введите название компании:")


@bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == ContactState.WAIT_COMPANY)
def process_company(message):
    user_id = message.from_user.id
    user_temp_data[user_id]['company'] = message.text
    user_states[user_id] = ContactState.WAIT_POSITION
    bot.send_message(user_id, "💼 Введите должность контакта:")


@bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == ContactState.WAIT_POSITION)
def process_position(message):
    user_id = message.from_user.id
    user_temp_data[user_id]['position'] = message.text
    user_states[user_id] = ContactState.WAIT_NAME
    bot.send_message(user_id, "👤 Введите ФИО контакта:")


@bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == ContactState.WAIT_NAME)
def process_name(message):
    user_id = message.from_user.id
    user_temp_data[user_id]['name'] = message.text
    user_states[user_id] = ContactState.WAIT_PHONE
    bot.send_message(user_id, "📱 Введите номер телефона:")


@bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == ContactState.WAIT_PHONE)
def process_phone(message):
    user_id = message.from_user.id
    user_temp_data[user_id]['phone'] = message.text

    # Показываем сводку и кнопку
    data = user_temp_data[user_id]
    summary = (
        f"📋 Проверка данных:\n\n"
        f"Компания: {data['company']}\n"
        f"Должность: {data['position']}\n"
        f"ФИО: {data['name']}\n"
        f"Телефон: {data['phone']}"
    )

    markup = types.InlineKeyboardMarkup()
    save_btn = types.InlineKeyboardButton("✅ Сохранить", callback_data="save_contact")
    cancel_btn = types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_contact")
    markup.add(save_btn, cancel_btn)

    bot.send_message(user_id, summary, reply_markup=markup)
    user_states[user_id] = ContactState.CONFIRM


@bot.callback_query_handler(func=lambda call: call.data in ['save_contact', 'cancel_contact'])
def confirm_contact(call):
    user_id = call.from_user.id
    if call.data == 'save_contact':
        data = user_temp_data.get(user_id)
        if data:
            # --- ЗДЕСЬ ТВОЯ ЛОГИКА СОХРАНЕНИЯ КОНТАКТОВ В БД ---
            # cursor.execute("INSERT INTO contacts (...) VALUES (...)", ...)

            bot.answer_callback_query(call.id, "Контакты успешно сохранены!")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="✅ Данные сохранены в базу.")
            # Очистка
            del user_temp_data[user_id]
            del user_states[user_id]
        else:
            bot.answer_callback_query(call.id, "Ошибка: данные потеряны", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "Ввод отменен")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❌ Ввод отменен.")
        del user_temp_data[user_id]
        del user_states[user_id]
