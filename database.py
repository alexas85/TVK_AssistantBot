# database.py
import sqlite3
import os

DB_NAME = os.getenv("DATABASE_NAME", "tvk_objects.db")

# Соответствие статусов из config.py -> эмодзи для хранения в БД
STATUS_EMOJI = {
    "new": "⬜",
    "ready": "🟦",
    "in_progress": "🟨",
    "partial": "🟧",
    "done": "🟢",
    "issues": "🔴",
    "inspection": "🟪",
    "signing": "🔵",
    "closed": "✅",
}


def get_connection():
    """Возвращает соединение с БД"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Чтобы обращаться к колонкам по имени
    return conn


def run_migration():
    """
    Проверяет структуру БД и добавляет недостающие таблицы/колонки.
    Запускается один раз при старте бота.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Таблица objects
        create_objects_table = """
        CREATE TABLE IF NOT EXISTS objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT DEFAULT 'new',
            status_emoji TEXT DEFAULT '⬜',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_objects_table)
        print("[MIGRATION] Таблица objects проверена/создана.")

        # 2. Добавляем колонки status/status_emoji, если их нет (для старых БД)
        columns_to_add = [
            ("objects", "status", "TEXT DEFAULT 'new'"),
            ("objects", "status_emoji", "TEXT DEFAULT '⬜'"),
        ]
        for table, col, definition in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {definition}")
                print(f"[MIGRATION] Добавлена колонка {col} в таблицу {table}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" not in str(e):
                    raise
                print(f"[MIGRATION] Колонка {col} уже существует, пропускаем.")

        # 3. Таблица contacts
        create_contacts_table = """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            object_id INTEGER,
            company TEXT,
            position TEXT,
            full_name TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_contacts_table)
        print("[MIGRATION] Таблица contacts проверена/создана.")

        conn.commit()
        print("[MIGRATION] Все миграции успешно применены!")

    except Exception as e:
        print(f"[MIGRATION ERROR] Произошла ошибка при миграции: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


def add_object(name, status="new"):
    """Добавляет новый объект и возвращает его id"""
    conn = get_connection()
    cursor = conn.cursor()
    emoji = STATUS_EMOJI.get(status, "⬜")
    cursor.execute(
        "INSERT INTO objects (name, status, status_emoji) VALUES (?, ?, ?)",
        (name, status, emoji),
    )
    conn.commit()
    object_id = cursor.lastrowid
    conn.close()
    return object_id


def get_objects():
    """Возвращает все объекты, отсортированные по времени создания"""
    conn = get_connection()
    rows = conn.execute("SELECT id, name, status, status_emoji FROM objects ORDER BY id").fetchall()
    conn.close()
    return rows


def get_object(object_id):
    """Возвращает один объект по id или None"""
    conn = get_connection()
    row = conn.execute(
        "SELECT id, name, status, status_emoji FROM objects WHERE id = ?", (object_id,)
    ).fetchone()
    conn.close()
    return row


def update_object_status(object_id, status):
    """Обновляет производственный статус объекта"""
    emoji = STATUS_EMOJI.get(status, "⬜")
    conn = get_connection()
    conn.execute(
        "UPDATE objects SET status = ?, status_emoji = ? WHERE id = ?",
        (status, emoji, object_id),
    )
    conn.commit()
    conn.close()