from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_first_superuser()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(main_router)

# Step 1: Install PostgreSQL Download and Install PostgreSQL: Download the
# PostgreSQL installer for Windows from the official PostgreSQL website. Run
# the installer. During installation, remember the password you set for the
# default postgres user and the port (default is 5432) unless you have a
# reason to change it.

# Step 2: Verify Installation Check PostgreSQL Service: Ensure that the
# PostgreSQL service is running. You can do this by going to Windows
# Services (services.msc - WIN+R) and looking for a service named something
# like postgresql-x64-16 - PostgreSQL Server 16. Access PostgreSQL via
# Command Line:
# Open the command prompt or PowerShell. Connect to PostgreSQL by running
# psql -U postgres. Enter the password you set during installation.

# Step 3:
# Create Database and Superuser Create a New Database:
# In the psql command line, create a new database for your FastAPI application:

# CREATE DATABASE fastapi;

# Create a New Superuser:
# Instead of creating a regular user, create a superuser. Replace
# your_password with a secure password of your choice:

# CREATE USER aleksandr WITH SUPERUSER PASSWORD 'your_password';

# This command creates a new superuser named aleksandr with the specified
# password.
