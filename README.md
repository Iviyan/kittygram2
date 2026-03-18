# Kittygram API

REST API для управления котиками и их достижениями. Включает модуль «Кото-путешествия» для отслеживания поездок котов.

**Стек:** Python 3.11, Django 3.2, Django REST Framework 3.12, JWT-аутентификация (djoser + simplejwt)

**Источник:** https://github.com/yandex-praktikum/kittygram2.git

## Локальный запуск

Для запуска необходим Python 3.11.

```bash
# Создать и активировать виртуальное окружение
py -3.11 -m venv env
.\env\Scripts\activate
python -m pip install --upgrade pip

# Установить зависимости
pip install -r requirements.txt

# Настроить переменные окружения
cp .env.example .env
# Отредактировать .env при необходимости

# Выполнить миграции и создать суперпользователя
python manage.py migrate
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver
```

API доступен по адресу: http://127.0.0.1:8000/

## Запуск через Docker

```bash
# Скопировать и настроить .env
cp .env.example .env

# Собрать и запустить контейнеры
docker-compose up --build

# В отдельном терминале — миграции и суперпользователь
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

API доступен по адресу: http://localhost/

## Документация API

- Swagger UI: http://127.0.0.1:8000/swagger/
- ReDoc: http://127.0.0.1:8000/redoc/

## Аутентификация

Проект использует JWT-аутентификацию. Все эндпоинты (кроме регистрации и документации) требуют токен.

```bash
# Регистрация
curl -X POST http://127.0.0.1:8000/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "strongpass123"}'

# Получение токена
curl -X POST http://127.0.0.1:8000/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "strongpass123"}'

# Использование токена
curl http://127.0.0.1:8000/cats/ \
  -H "Authorization: Bearer <ваш_access_token>"
```

## Основные эндпоинты

| URL | Метод | Описание |
|-----|-------|----------|
| `/cats/` | GET, POST | Список / создание котов |
| `/cats/{id}/` | GET, PUT, PATCH, DELETE | Детали / редактирование / удаление кота |
| `/achievements/` | GET, POST | Список / создание достижений |
| `/achievements/{id}/` | GET, PUT, PATCH, DELETE | Детали достижения |
| `/users/` | GET | Список пользователей |
| `/users/{id}/` | GET | Детали пользователя |
| `/trips/` | GET, POST | Список / создание поездок |
| `/trips/{id}/` | GET, PUT, PATCH, DELETE | Детали поездки |
| `/trips/{id}/activate/` | POST | Начать поездку |
| `/trips/{id}/complete/` | POST | Завершить поездку |
| `/trips/{id}/stops/` | GET, POST | Остановки поездки |
| `/trips/{id}/stops/{pk}/` | GET, PUT, PATCH, DELETE | Детали остановки |
| `/auth/users/` | POST | Регистрация |
| `/auth/jwt/create/` | POST | Получение JWT-токена |
| `/auth/jwt/refresh/` | POST | Обновление токена |
| `/auth/jwt/verify/` | POST | Проверка токена |

## Зависимости

| Пакет | Версия | Назначение |
|-------|--------|------------|
| `Django` | 3.2.3 | Основной веб-фреймворк |
| `djangorestframework` | 3.12.4 | Django REST Framework — построение API |
| `PyJWT` | 2.1.0 | Работа с JWT-токенами |
| `djangorestframework-simplejwt` | 4.8.0 | JWT-аутентификация для DRF |
| `djoser` | 2.1.0 | Готовые эндпоинты для регистрации и управления пользователями |
| `drf-yasg` | latest | Автогенерация Swagger/ReDoc документации |
| `gunicorn` | latest | WSGI-сервер для production (используется в Docker) |

Все зависимости перечислены в [requirements.txt](requirements.txt).

## Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `SECRET_KEY` | Секретный ключ Django | dev-ключ (только для разработки) |
| `DEBUG` | Режим отладки | `True` |
| `ALLOWED_HOSTS` | Разрешённые хосты (через запятую) | пусто |
