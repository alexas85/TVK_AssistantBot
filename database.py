# database.py
import sqlite3
import os

DB_NAME = "tvk_objects.db"


def get_connection():
    """Возвращает соединение с БД"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Чтобы обращаться к колонкам по имени
    return conn


def run_migration():
    """
    Проверяет структуру БД и добавляет недостающие колонки/таблицы.
    Запускается один раз при старте бота.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Добавляем колонки в таблицу objects, если их нет
        # SQLite не поддерживает ALTER TABLE ADD COLUMN IF NOT EXISTS напрямую в старых версиях,
        # поэтому мы просто пытаемся добавить. Если колонка есть — SQLite выдаст ошибку, которую мы поймаем.

        columns_to_add = [
            ("objects", "status", "TEXT DEFAULT 'new'"),
            ("objects", "status_emoji", "TEXT DEFAULT '⬜'")
        ]

        for table, col, definition in columns_to_add:
            try:
                query = f"ALTER TABLE {table} ADD COLUMN {col} {definition}"
                cursor.execute(query)
                print(f"[MIGRATION] Добавлена колонка {col} в таблицу {table}")
            except sqlite3.OperationalError as e:
                # Если ошибка "duplicate column name", значит колонка уже есть — это нормально
                if "duplicate column name" not in str(e):
                    raise e
                else:
                    print(f"[MIGRATION] Колонка {col} уже существует, пропускаем.")

        # 2. Создаем таблицу contacts, если её нет
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
    finally:
        conn.close()
