# handlers/status_handler.py
from telebot import types
from config import STATUSES
from database import update_object_status
from keyboards.object_keyboard import object_detail_markup


def build_status_selection_markup(object_id):
    """Клавиатура выбора производственного статуса для объекта"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    for code, (emoji, text) in STATUSES.items():
        btn = types.InlineKeyboardButton(
            f"{emoji} {text}",
            callback_data=f"set_status_{object_id}_{code}"
        )
        markup.add(btn)
    markup.add(types.InlineKeyboardButton("↩️ Назад", callback_data=f"obj_view_{object_id}"))
    return markup


def register_status_handlers(bot):
    """Регистрирует обработчик выбора статуса по кнопкам (вызывается из main)"""

    @bot.callback_query_handler(func=lambda c: c.data.startswith("set_status_"))
    def process_status_callback(call):
        parts = call.data.split("_")
        # формат: set_status_<object_id>_<status_code>
        try:
            object_id = int(parts[2])
            status_code = parts[3]
        except (IndexError, ValueError):
            bot.answer_callback_query(call.id, "Некорректные данные", show_alert=True)
            return

        if status_code not in STATUSES:
            bot.answer_callback_query(call.id, "Неизвестный статус", show_alert=True)
            return

        update_object_status(object_id, status_code)
        emoji, description = STATUSES[status_code]

        bot.answer_callback_query(call.id, f"Статус: {emoji} {description}")

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"✅ Статус установлен: {emoji} {description}",
            reply_markup=object_detail_markup(object_id)
        )