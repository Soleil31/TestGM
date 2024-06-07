# Birthday Notifications Service

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-black.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.12-green.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0.6-blue.svg)](https://www.docker.com/)

Сервис для отправки уведомлений о Днях Рождений пользователей. Разработан как часть тестового задания и успешно реализует все требуемые функции.

## 🛠 Стек

- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **FastAPI-Mail**
- **APScheduler**

## 🚀 Начало работы

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Soleil31/TestGM.git

2. В корне проекта создайте файл .env, пример такого файла можно найти в env.example
3. Запустите при помощи одной из двух команд:
    ```
    docker-compose up -d
    ```
    ```
    uvicorn main:app --reload
    ```
4. Тестируйте! :)

## Пример работы
![alt text](Email_receive_example.png)
