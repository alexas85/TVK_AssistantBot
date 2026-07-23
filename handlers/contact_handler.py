# handlers/contact_handler.py
import telebot
from telebot import types

# Предполагаем, что у тебя есть глобальные словари user_states и user_temp_data
# Если они у тебя в database.py или main.py, импортируй их оттуда.
# Для примера я оставлю их здесь как глобальные, но лучше вынести в отдельный модуль states.py
user_states = {}
user_temp_data = {}


class ContactState:
    WAIT_COMPANY = "wait_company"
    WAIT_POSITION = "wait_position"
    WAIT_NAME = "wait_name"
    WAIT_PHONE = "wait_phone"
    CONFIRM = "confirm"


# 1. Обработчик команды /add_contacts (ТО, ЧЕГО НЕ ХВАТАЛО)
@telebot.util.message_handler(commands=['add_contacts'])
def start_contacts_flow(message, bot):
    user_id = message.from_user.id
    user_temp_data[user_id] = {}
    user_states[user_id] = ContactState.WAIT_COMPANY

    bot.send_message(
        user_id,
        "🏢 Отлично! Начнем заполнение контактов. \n\nВведите название компании:"
    )


# 2. Обработчики пошагового ввода
@telebot.util.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == ContactState.WAIT_COMPANY)
def process_company(message, bot):
    user_id = message.from_user.id
    user_temp_data[user_id]['company'] = message.text
    user_states[user_id] = ContactState.WAIT_POSITION
    bot.send_message(user_id, "💼 Теперь введите должность контакта:")


@telebot.util.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == ContactState.WAIT_POSITION)
def process_position(message, bot):
    user_id = message.from_user.id
    user_temp_data[user_id]['position'] = message.text
    user_states[user_id] = ContactState.WAIT_NAME
    bot.send_message(user_id, "👤 Теперь введите ФИО контакта:")


@telebot.util.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == ContactState.WAIT_NAME)
def process_name(message, bot):
    user_id = message.from_user.id
    user_temp_data[user_id]['name'] = message.text
    user_states[user_id] = ContactState.WAIT_PHONE
    bot.send_message(user_id, "📱 И наконец, номер телефона:")


@telebot.util.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == ContactState.WAIT_PHONE)
def process_phone(message, bot):
    user_id = message.from_user.id
    user_temp_data[user_id]['phone'] = message.text

    # Формируем сводку
    data = user_temp_data[user_id]
    summary = (
        f"📋 Проверка данных:\n\n"
        f"Компания: {data['company']}\n"
        f"Должность: {data['position']}\n"
        f"ФИО: {data['name']}\n"
        f"Телефон: {data['phone']}"
    )

    # Создаем кнопки
    markup = types.InlineKeyboardMarkup()
    save_btn = types.InlineKeyboardButton("✅ Сохранить", callback_data="save_contact")
    cancel_btn = types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_contact")
    markup.add(save_btn, cancel_btn)

    bot.send_message(user_id, summary, reply_markup=markup)
    user_states[user_id] = ContactState.CONFIRM


# 3. Обработчик кнопок (Сохранить / Отмена)
@telebot.util.callback_query_handler(func=lambda call: call.data in ['save_contact', 'cancel_contact'])
def confirm_contact_action(call, bot):
    user_id = call.from_user.id

    if call.data == 'save_contact':
        data = user_temp_data.get(user_id)
        if data:
            # --- ЗДЕСЬ ТВОЯ ЛОГИКА СОХРАНЕНИЯ В БД ---
            # Пример (заглушка):
            print(f"[DB] Сохраняем контакт для пользователя {user_id}: {data}")

            bot.answer_callback_query(call.id, "Контакты сохранены!")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="✅ Данные успешно сохранены в базу."
            )

            # Очищаем память
            del user_temp_data[user_id]
            del user_states[user_id]
        else:
            bot.answer_callback_query(call.id, "Ошибка: данные потеряны", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "Ввод отменен")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="❌ Ввод контактов отменен."
        )
        del user_temp_data[user_id]
        del user_states[user_id]
