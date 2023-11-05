
# Lecture 4 SQL, Models, and Migrations

## SQLite Type

- Text
- Numeric
- Integer
- Real
- Blob

MySQL has more types

## SQLite Commands

- CREATE TABLE Command

## Constraints

- INSERT INTO

- SELECT

SELECT * FROM Flights;

SELECT origin, destination FROM flights;

SELECT * FROM flights WHERE id=3;

SELECT * FROM flights WHERE origin=New York;

- Format SQL

  - .mode columns
  - .headers yes

- FUNCTIONS

- UPDATE

- DELETE

- JOIN, ON
  - JOINs

- CREATE INDEX

- SQL Injection

- Race Conditions

- Django Models
  - Create Migration

- String representation of classes

- Commands to Create a Model

```terminal

(.venv) django-admin startproject airline
(.venv) cd airline
(.venv) python manage.py startapp flights
(.venv) # Add app to airline/settings.py
(.venv) # Add include url to airline/urls.py
(.venv) # Add path to flights/urls.py
(.venv) # Add function to views.py
(.venv) python manage.py runserver
(.venv) add model to flights/ 
(.venv) python manage.py makemigrations
(.venv) # you should see flights/migrations/0001_initial.py
(.venv) python manage.py migrate
(.venv) python manage.py shell
>>> from django.db import models
>>> from flights.models import Flight
>>> f = Flight(origin="New York", destination="London", duration=415)
>>> f.save()
>>> Flight.objects.all()
(.venv)

```
