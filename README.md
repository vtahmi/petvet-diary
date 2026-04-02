# 🐾 PetVet Diary

A web application for pet owners and veterinarians to manage pet health records, appointments, and vaccinations.

## Features

- User authentication (Pet Owners & Veterinarians)
- Pet management (CRUD)
- Vaccination tracking
- Appointment booking
- Email notifications (async with Celery)
- REST API

## Tech Stack

- Django 5.0+
- Django REST Framework
- Celery + Redis
- Bootstrap 5
- SQLite / PostgreSQL

## Installation

### 1. Clone repository

    git clone https://github.com/vtahmi/petvet-diary.git
    cd petvet-diary

### 2. Create virtual environment

    python -m venv venv

### 3. Activate virtual environment

Windows:

    venv\Scripts\activate

Mac/Linux:

    source venv/bin/activate

### 4. Install dependencies

    pip install -r requirements.txt

### 5. Create .env file

    SECRET_KEY=your-secret-key-here
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1

### 6. Run migrations

    python manage.py migrate

### 7. Create superuser

    python manage.py createsuperuser

### 8. Setup user groups

    python manage.py setup_groups

### 9. Run server

    python manage.py runserver

### 10. Run Celery (separate terminal)

Windows:

    celery -A petvet_project worker --loglevel=info --pool=solo

Mac/Linux:

    celery -A petvet_project worker --loglevel=info

## Running Tests

    python manage.py test

## Author

Viktor Tahmisyan - SoftUni Django Advanced

