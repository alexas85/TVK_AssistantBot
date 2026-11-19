from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_objects_menu():
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("📋 Список объектов", callback_data="obj_list"))
    kb.row(InlineKeyboardButton("➕ Добавить объект", callback_data="obj_add"))
    return kb


def objects_list_markup(rows):
    """Кнопки для перехода к конкретному объекту из списка"""
    kb = InlineKeyboardMarkup()
    for r in rows:
        kb.row(InlineKeyboardButton(
            f"{r['id']}. {r['name']} — {r['status_emoji']}",
            callback_data=f"obj_view_{r['id']}"
        ))
    kb.row(InlineKeyboardButton("🔄 Обновить список", callback_data="obj_list"))
    kb.row(InlineKeyboardButton("← Назад к меню объектов", callback_data="obj_menu"))
    return kb


def object_detail_markup(object_id):
    """Кнопки в карточке объекта"""
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("🔄 Изменить статус", callback_data=f"obj_status_{object_id}"))
    kb.row(InlineKeyboardButton("← Назад к списку объектов", callback_data="obj_list"))
    return kb


def back_to_main_objects():
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("← Назад к меню объектов", callback_data="obj_menu"))
    return kb