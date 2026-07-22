from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_objects_menu():
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("Текущие объекты", callback_data="obj_current"))
    kb.row(InlineKeyboardButton("Завершенные объекты", callback_data="obj_completed"))
    kb.row(InlineKeyboardButton("Добавить объект", callback_data="obj_add"))
    return kb

def back_to_main_objects():
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("← Назад к меню объектов", callback_data="obj_menu"))
    return kb
