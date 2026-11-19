FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Скрипт запуска: убираем возможные CR (\r) из переводов строк и ставим права.
# Это исключает ошибку "exec: no such file or directory" от CRLF-шебанга.
COPY entrypoint.sh /app/entrypoint.sh
RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Запускаем shell ЯВНО (не полагаемся на shebang и права исполнения)
ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]

# Порт (для healthcheck, если нужен; сам бот его не использует)
EXPOSE 8080