# config.py
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден!")

# --- Словарь статусов: код -> (эмодзи, описание) ---
STATUSES = {
    "new": ("⬜", "Ещё не готов к монтажу"),
    "ready": ("🟦", "Готов к монтажу"),
    "in_progress": ("🟨", "В стадии монтажа / Есть замечания"),
    "partial": ("🟧", "Монтаж завершён не полностью"),
    "done": ("🟢", "Монтаж завершён"),
    "issues": ("🔴", "Требуется устранение замечаний"),
    "inspection": ("🟪", "Предъявление стройконтролю"),
    "signing": ("🔵", "Подписание объёмов работ"),
    "closed": ("✅", "Объект сдан")
}

# --- Шаблоны для кнопок (если нужно группировать) ---
STATUS_BUTTON_TEMPLATES = {
    "in_progress": "🟨 🛠️ В стадии монтажа",
    "issues": "🔴 ↩️ Устранение замечаний",
    "closed": "✅ 🎉 Объект сдан"
}
