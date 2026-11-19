import telebot
from telebot import types
from database import add_object, get_objects, get_object
from keyboards.object_keyboard import (
    main_objects_menu,
    objects_list_markup,
    object_detail_markup,
    back_to_main_objects,
)
from handlers.status_handler import build_status_selection_markup

user_states = {}  # user_id -> state


def register_objects_handlers(bot: telebot.TeleBot):

    @bot.message_handler(commands=["start"])
    def send_welcome(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton("🏗 Объекты")
        markup.add(btn)
        bot.send_message(
            message.chat.id,
            "Привет! Это TVK Assistant — бот для управления объектами компании ТВК.",
            reply_markup=markup
        )

    @bot.message_handler(func=lambda m: m.text == "🏗 Объекты")
    def handle_objects_main(message):
        bot.send_message(
            message.chat.id,
            "Меню объектов ТВК:",
            reply_markup=main_objects_menu()
        )

    @bot.callback_query_handler(func=lambda c: c.data == "obj_menu")
    def callback_obj_menu(call):
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Меню объектов ТВК:",
            reply_markup=main_objects_menu()
        )

    @bot.callback_query_handler(func=lambda c: c.data == "obj_list")
    def callback_list_objects(call):
        rows = get_objects()
        if not rows:
            text = "Список объектов пуст. Добавьте первый объект."
            markup = back_to_main_objects()
        else:
            lines = [f"{r['id']}. {r['name']} — {r['status_emoji']} {r['status']}" for r in rows]
            text = "Объекты ТВК:\n" + "\n".join(lines)
            markup = objects_list_markup(rows)

        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=markup
        )

    @bot.callback_query_handler(func=lambda c: c.data.startswith("obj_view_"))
    def callback_view_object(call):
        try:
            object_id = int(call.data.split("_")[2])
        except (IndexError, ValueError):
            bot.answer_callback_query(call.id, "Некорректный id объекта", show_alert=True)
            return

        row = get_object(object_id)
        if not row:
            bot.answer_callback_query(call.id, "Объект не найден", show_alert=True)
            return

        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"📌 Объект: {row['name']}\nСтатус: {row['status_emoji']} {row['status']}",
            reply_markup=object_detail_markup(object_id)
        )

    @bot.callback_query_handler(func=lambda c: c.data.startswith("obj_status_"))
    def callback_choose_status(call):
        try:
            object_id = int(call.data.split("_")[2])
        except (IndexError, ValueError):
            bot.answer_callback_query(call.id, "Некорректный id объекта", show_alert=True)
            return

        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Выберите новый статус для объекта #{object_id}:",
            reply_markup=build_status_selection_markup(object_id)
        )

    @bot.callback_query_handler(func=lambda c: c.data == "obj_add")
    def callback_add_object(call):
        user_id = call.from_user.id
        user_states[user_id] = "waiting_for_object_name"
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Введите название нового объекта ТВК:"
        )

    @bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "waiting_for_object_name")
    def handle_object_name_input(message):
        name = message.text.strip()
        if not name:
            bot.reply_to(message, "Название не может быть пустым. Попробуйте ещё раз:")
            return

        add_object(name)
        user_states.pop(message.from_user.id, None)
        bot.reply_to(
            message,
            f"✅ Объект «{name}» добавлен в систему ТВК."
        )