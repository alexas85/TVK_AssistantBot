FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Скрипт запуска (миграции + бот)
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Порт (если нужен для здоровья, но для телеграма не обязателен)
EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]
