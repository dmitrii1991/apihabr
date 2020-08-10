[![Python version](https://img.shields.io/badge/Python-3.8.4-green)](https://www.python.org/)
[![Django version](https://img.shields.io/badge/Django-3.0.8-green)](https://docs.djangoproject.com/en/3.0/)
[![djangorestframework version](https://img.shields.io/badge/djangorestframework-3.11.0-green)](https://www.django-rest-framework.org/)
[![celery version](https://img.shields.io/badge/celery-4.4.6-green)](https://www.django-rest-framework.org/)

# APIHABR - aggregator of the best articles per day

## Main design goals

- Написать RESTful приложение, которое является агрегатором лучших статей за сутки на ресурсе. Статьи парсятся без картинок, интересующая информация - это заголовок, текст, ссылка на оригинал. Должны быть представлены методы доступа к листингу полученных статей с пагинацией и к отдельно взятой статье. 
В ресурсе листинга каждый элемент представляет собой заголовок статьи и  700 символов тела статьи
Ресурс отдельно взятой статьи должен отдавать заголовок, тело статьи и ссылку на оригинал.
Статьи должны парситься по расписанию с Хабры раз в сутки и складываться в хранилище (выбор хранилища на свое усмотрение).

## Specifications

- Использование при решении Python 3.8
- Реализация на Django + django rest framework
- Хранилище выбирается на свое усмотрение
- Инструменты для парсинга выбираются на свое усмотрение
- В приложении должно быть реализовано логгирование.
- В приложении должна быть обработка ошибок
- Приложение должно быть готово к тестированию без дополнительных трудозатрат. Это могут быть как автотесты (UnitTest, PyTest), так и простейший интерфейс или готовые curl запросы.

## Requirements for registration

- Модули, классы и методы должны быть задокументированы в формате docstring

## application launch

```shell script
pip install -r requirements.txt
```

в apihabr.apihabr.settings.py указываем настройки redis и postgresql

```python
# REDIS related settings
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
```
Например, можно поднять c помощью доскера redis/postgresql
```shell script
docker run -d --rm  -p 6379:6379 redis
```
или
```shell script
docker-compose up
```
запускаем след команды
```shell script
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

celery -A apihabr worker -l info
celery -A apihabr beat -l info
```


Postman Collection v2.1 (recommended)
* *Habr_api_test.postman_collection.json*