![Workflow status](https://github.com/moritys/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Foodrgam

Продуктовый помощник представляет собой сайт для публикации рецептов. Для разработки использовался готовый одностраничный фронтенд и API для него.
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
### Используемые технологии
 - DRF 3.14.0
 - Django 3.2.16
 - Python 3.7
 - Postgre 
 - Nginx 
 - Gunicorn
---
### Развертывание на сервере
Для разворачивания у себя на сервер необходимо:
 - изменить workflow
 - добавить все секретные переменные в проект на github
 - изменить данные docker-hub на свои
 - провести миграции внутри контейнера:

```python
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

#### Шаблон наполнения env-файла

    SECRET_KEY  =  'yoursecretdjangokey'
    
    DB_ENGINE = django.db.backends.postgresql # указываем, что работаем с postgresql
    
    DB_NAME = postgres_name # имя базы данных
    
    POSTGRES_USER = postgres_user # логин для подключения к базе данных
    
    POSTGRES_PASSWORD = password1234! # пароль для подключения к БД
    
    DB_HOST = db # название сервиса (контейнера)
    
    DB_PORT = 5432 # порт для подключения к БД
---

##### Автор
[Masha](https://t.me/mori_tys)
