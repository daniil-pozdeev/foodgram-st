# Продуктовый помощник Foodgram

## Описание проекта

Из задания: Вам предстоит поработать с проектом «Фудграм» — сайтом, на котором пользователи будут публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Зарегистрированным пользователям также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

## Технологии

![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![Nginx](https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)


## Запуск проекта в dev-режиме (только backend)

- Клонируйте репозиторий с проектом на свой компьютер. В терминале из рабочей директории выполните команду:

```bash
git clone https://github.com/daniil-pozdeev/foodgram-st.git
cd foodgram-st/backend
```

- Установите и активируйте виртуальное окружение (для linux, для windows используйте ```env/Scripts/activate```)

```bash
python -m venv env
source ./env/bin/activate
```
- Установите зависимости из файла `requirements.txt`

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
### Выполните миграции:

```bash
# foodgram-st/backend
python manage.py migrate
```
- Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

### Загрузите статику:

```bash
python manage.py collectstatic --no-input
```

### Заполните базу тестовыми данными:

```bash
python manage.py loaddata initial_data.json
```

- Запустите сервер 


```bash
python manage.py runserver
```

После выполнения команд произойдёт активация backend-части, этого достаточно для запуска тестов postman-api.
Рекомендуем использовать конфигурацию по умолчанию db: sqlite3, DEBUG: True

## Полный запуск проекта

Для полноценного рабочего сайта необходимы еще прокси, фронтенд и база данных.

Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). Отдельно потребуется установть [Docker Compose](https://docs.docker.com/compose/install/)

Клонируйте репозиторий с проетом на свой компьютер, если этого не было сделано ранее:

```bash
git clone https://github.com/daniil-pozdeev/foodgram-st.git
```
- Создайте файл .env в папке проекта:

```.env
SECRET_KEY="..."                      # используйте свой ключ (get_random_secret_key())
DB_ENGINE=django.db.backends.postgres # укажите что работаем с postgres
DB_NAME=postgres                      # имя базы данных
POSTGRES_USER=postgres                # логин для подключения к базе
POSTGRES_PASSWORD=password            # пароль для подключения к БД
DB_HOST=db                            # название контейнера
DB_PORT=5432                          # порт для подключения к БД
DEBUG=True                            # порт для подключения к БД
```

- Выполните команду сборки контейнеров

```bash
docker compose up -d --build
```
В результате выполнения данной команды должно быть собрано четыре контейнера, три из которых активные, а foodgram - статичный (служит хранилищем, поэтому не будет отображаться как активный)

- Для просмотра всех контейнеров используйте команду

```bash
docker container ls -a
```
Получаем список контейнеров

```
|    NAMES        |     DESCRIPTIONS       |
|infra-nginx-1    | обратный прокси        |
|infra-db-1       | база данных            |
|infra-backend-1  | приложение Django      |
|infra-frontend-1 | приложение  React      |          |

```

- Выполните миграции:

```bash
docker compose exec backend python manage.py migrate
```

- Создайте суперпользователя:

```bash
docker compose exec backend python manage.py createsureruser
```

- Заполните базу тестовыми данными:

```bash
docker compose exec backend python manage.py loaddata initial_data.json
```

- Загрузите статику

```bash
docker compose exec backend python manage.py collectstatic --no-input
```

### Основные адреса:


```
|    Адрес            |     Описание            |
|127.0.0.1            | Главная страница        |
|127.0.0.1/admin      | Панель администратора   |
|127.0.0.1/api/docs/  | Документация к API      |

```


### Автор проекта
Статус проекта: на ревью
_Поздеев Даниил_<br>
