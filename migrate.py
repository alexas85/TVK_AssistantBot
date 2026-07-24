import sqlite3
import os

DB_NAME = os.getenv("DATABASE_NAME", "bot_database.db")

def run_migrations():
    print(f"🗄️ Подключение к базе данных: {DB_NAME}")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Миграция 1: Создание таблицы objects
    create_table_query = """
    CREATE TABLE IF NOT EXISTS objects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    print("✅ Таблица 'objects' готова (создана или уже существовала).")

    # Здесь можно добавить другие миграции...

    conn.close()
    print("🏁 Все миграции завершены.")

if __name__ == "__main__":
    try:
        run_migrations()
    except Exception as e:
        print(f"💥 Критическая ошибка при миграции: {e}")
        raise e
