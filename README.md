### Как запустить проект:

Источник: https://github.com/yandex-praktikum/kittygram2.git


Cоздать и активировать виртуальное окружение:
(Для запуска проекта необходима версия python 3.11)

```
py -3.11 -m venv env
.\env\Scripts\activate
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
