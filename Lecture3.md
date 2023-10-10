
# lecture 3 Django

## Install

```terminal
$
$ pip3 install djang0
$ django-admin startproject PROJECT_NAME
$ pip install django
$ django-admin startproject lecture3
$ python manage.py startapp tasks
```

## Edit TheProject/settings.py

Add your app to installed apps in this case tasks

```python
INSTALLED_APPS = [
    'hello',
    'newyear',
    'tasks',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

## Edit TheApp/views.py

The code for the app goes here.

For example:

```python
from django.http import HttpResponse
from django.shortcuts import render

def index0(request):
    return HttpResponse("Hello, world!")

def index1(request):
    return render(request, "hello/index.html")

def brian(request):
    return HttpResponse("Hello, Brian!")

def david(request):
    return HttpResponse("Hello, David!")

def greet0(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}!")

def greet1(request, name):
    return render(request, "hello/greet.html", {
        "name": name.capitalize()
    })
```

## Edit urls.py

First add the urls to the project TheProject/urls.py. Handling the urls this way we can include urls on a per app basis.

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("hello/", include("hello.urls")),
    path("tasks/", include("tasks.urls")),
    path("newyear/", include("newyear.urls")),
]
```

Then add the urls for each TheAPP/urls.py

```python
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index1, name="index"),
    path("<str:name>", views.greet1, name="greet"),
    path("brian", views.brian, name="brian"),
    path("david", views.david, name="david"),
]
```

## When using session tables

When using session tables run the following

```terminal
$
$ python manage.py migrate
$
```
