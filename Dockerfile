# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем метаданные
LABEL authors="ilyaavtln"
LABEL description="Telegram Bot"

# Создаем рабочую директорию
WORKDIR /app

# Копируем только необходимые файлы
COPY requirements.txt .
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем бота
CMD ["python", "main.py"]