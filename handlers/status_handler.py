# handlers/status_handler.py
from telebot import types
from config import STATUSES


class State:
    WAITING_FOR_STATUS = "wait_status"
    WAITING_FOR_CONTACTS = "wait_contacts"


# Хранилище состояний пользователей (в продакшене лучше Redis, для старта хватит dict)
user_states = {}


def show_status_keyboard(message, bot):
    """Показываем кнопки со статусами"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = []

    for code, (emoji, text) in STATUSES.items():
        # Формируем красивую кнопку: 🟦 Готов к монтажу
        btn_text = f"{emoji} {text}"
        btn = types.InlineKeyboardButton(btn_text, callback_data=f"status_{code}")
        buttons.append(btn)

    # Кнопка отмены
    cancel_btn = types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_status")
    buttons.append(cancel_btn)

    markup.add(*buttons)
    bot.send_message(message.chat.id, "Выберите статус объекта:", reply_markup=markup)
    # Сохраняем, что пользователь сейчас выбирает статус
    user_states[message.from_user.id] = State.WAITING_FOR_STATUS


def process_status_callback(call, bot, db_connection):
    """Обрабатываем нажатие на статус"""
    user_id = call.from_user.id

    if user_states.get(user_id) != State.WAITING_FOR_STATUS:
        bot.answer_callback_query(call.id, "Сессия истекла или действие неактуально", show_alert=True)
        return

    status_code = call.data.replace("status_", "")
    emoji, description = STATUSES[status_code]

    # --- ЗДЕСЬ ТВОЯ ЛОГИКА СОХРАНЕНИЯ В БД ---
    # Примерный SQL (адаптируй под свою таблицу objects)
    # cursor.execute("UPDATE objects SET status = ?, status_emoji = ? WHERE user_id = ?", (status_code, emoji, user_id))
    # db_connection.commit()

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"✅ Статус установлен: {emoji} {description}"
    )

    # Сбрасываем состояние
    del user_states[user_id]

    # Тут можно сразу предложить добавить контакты или вернуться в меню
    bot.send_message(user_id, "Хотите добавить контакты к этому объекту? Нажмите /add_contacts")
