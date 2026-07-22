import telebot
from telebot import types
from database import add_object, get_objects
from keyboards.object_keyboard import main_objects_menu, back_to_main_objects

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

    @bot.callback_query_handler(func=lambda c: c.data in ["obj_current", "obj_completed"])
    def callback_list_objects(call):
        status_map = {"obj_current": "current", "obj_completed": "completed"}
        status = status_map[call.data]
        rows = get_objects(status=status)
        if not rows:
            text = "Нет объектов в этой категории."
        else:
            lines = [f"{r[0]}. {r[1]} ({r[2]})" for r in rows]
            text = "Объекты ТВК:\n" + "\n".join(lines)

        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=back_to_main_objects()
        )

    @bot.callback_query_handler(func=lambda c: c.data == "obj_add")
    def callback_add_object(call):
        user_id = call.from_user.id
        user_states[user_id] = "waiting_for_object_name"
        bot.answer_callback_query(call.id, "Введите название объекта:")
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

        add_object(name, "current")
        user_states.pop(message.from_user.id, None)
        bot.reply_to(
            message,
            f"✅ Объект «{name}» добавлен в систему ТВК со статусом «текущий»."
        )
