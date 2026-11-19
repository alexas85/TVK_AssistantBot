import database

if __name__ == "__main__":
    try:
        print(f"🗄️ Подключение к базе данных: {database.DB_NAME}")
        database.run_migration()
    except Exception as e:
        print(f"💥 Критическая ошибка при миграции: {e}")
        raise e