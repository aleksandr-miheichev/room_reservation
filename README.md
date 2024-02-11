# Meeting room booking service

## Contents

- [Project Description](#project-description)
- [Technology Stack](#technology-stack)
- [How to Deploy Project](#how-to-deploy-a-project)
- [Fill-in-the-file .env template](#template-for-populating-the-env-file)
- [Database Setup](#configuring-the-database)
- [Application Startup](#start-the-application)
- [API Documentation](#api-documentation)
- [Worked on project](#the-project-was-worked-on-by)

---

### Project Description:

Asynchronous API for an application that will provide an opportunity to book 
rooms for a certain period of time.

You can find out which meeting room is booked, by whom and for what period of 
time. The division of roles into regular users and system admins is 
implemented.

The user can book a free room for a certain period of time, and the application 
checks whether someone has already booked this room and whether the whole time 
for which this meeting room is booked is free. 

---

### Technology Stack:

- [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
- [![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [FastAPI Users](https://fastapi-users.github.io/fastapi-users/)
- [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

---

### How to deploy a project:

Clone a repository and navigate to it in the terminal using the command

```
cd
```

```bash
git clone git@github.com:aleksandr-miheichev/room_reservation.git
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

Install dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

___

### Template for populating the .env file:

```
APP_NAME=Meeting room booking service
DATABASE_URL=postgresql+psycopg://user:password@localhost/dbname
SECRET=secret_word_for_token_generation
FIRST_SUPERUSER_EMAIL=email@email.com
FIRST_SUPERUSER_PASSWORD=creared_password
```

___

### Configuring the database:

Apply Migrations:

```bash
alembic upgrade head 
```

---

### Start the application:

To run the application, you must use the command in the terminal:

```bash
uvicorn app.main:app --reload
```

---

### API Documentation:

- [Swagger](http://127.0.0.1:8000/docs)
- [Redoc](http://127.0.0.1:8000/redoc)

---

#### The project was worked on by:

- [Miheichev Aleksandr](https://github.com/aleksandr-miheichev)
