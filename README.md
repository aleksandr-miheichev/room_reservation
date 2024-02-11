# Meeting room booking service

## Содержание

- [Описание проекта](#описание-проекта)
- [Технологический стек](#технологический-стек)
- [Как развернуть проект](#как-развернуть-проект)
- [Шаблон наполнения файла .env](#шаблон-наполнения-файла-env)
- [Настройка базы данных](#настройка-базы-данных)
- [Запуск приложения](#запуск-приложения)
- [Документация API](#документация-api)
- [Над проектом работал](#над-проектом-работал)

---

### Описание проекта:

Asynchronous API for an application that will provide an opportunity to book 
rooms for a certain period of time.

You can find out which meeting room is booked, by whom and for what period of 
time. The division of roles into regular users and system admins is 
implemented.

The user can book a free room for a certain period of time, and the application 
checks whether someone has already booked this room and whether the whole time 
for which this meeting room is booked is free. 

---

### Технологический стек:

- [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
- [![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [FastAPI Users](https://fastapi-users.github.io/fastapi-users/)
- [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

---

### Как развернуть проект:

Клонировать репозиторий и перейти в него в терминале используя команду

```
cd
```

```bash
git clone git@github.com:aleksandr-miheichev/room_reservation.git
```

Создать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

___

### Шаблон наполнения файла .env:

```
APP_NAME=Meeting room booking service
DATABASE_URL=postgresql+psycopg://user:password@localhost/dbname
SECRET=secret_word_for_token_generation
FIRST_SUPERUSER_EMAIL=email@email.com
FIRST_SUPERUSER_PASSWORD=creared_password
```

___

### Настройка базы данных:

Применить миграции:

```bash
alembic upgrade head 
```

---

### Запуск приложения:

Чтобы запустить приложение, необходимо в терминале использовать команду:

```bash
uvicorn app.main:app --reload
```

---

### Документация API:

- [Swagger](http://127.0.0.1:8000/docs)
- [Redoc](http://127.0.0.1:8000/redoc)

---

### Над проектом работал:

- [Михеичев Александр](https://github.com/aleksandr-miheichev)
