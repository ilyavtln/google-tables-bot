# Telegram Bot

Этот проект представляет собой Telegram-бота, разработанного с использованием **Aiogram** и **Docker**. Бот выполняет задачи с возможностью взаимодействия с пользователем через inline-кнопки и отправляет данные в Google Sheets.

## Требования

Перед запуском убедитесь, что у вас установлены следующие инструменты:

- [Python 3.9+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/products/docker-desktop)


## 1. Cобрать образ
```bash
docker build -t my-app .
```

## 2. Запустить контейнер
```bash
docker run -d --name tg-bot my-app
```
