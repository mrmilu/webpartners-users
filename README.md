# webpartners_users django package

[![image](https://img.shields.io/pypi/v/webpartners_users.svg)](https://pypi.org/project/webpartners_users/)
[![image](https://img.shields.io/pypi/l/webpartners_users.svg)](https://pypi.org/project/webpartners_users/)
[![image](https://img.shields.io/pypi/pyversions/webpartners_users.svg)](https://pypi.org/project/webpartners_users/)
[![image](https://img.shields.io/pypi/djversions/webpartners_users.svg)](https://pypi.org/project/webpartners_users/)
[![image](https://img.shields.io/github/last-commit/mrmilu/webpartners-users.svg)](https://github.com/mrmilu/webpartners-users)
[![image](https://img.shields.io/github/contributors/mrmilu/webpartners-users.svg)](https://github.com/mrmilu/webpartners-users/graphs/contributors)

This package provides a combination of common functionalities for simple projects:
- django user model without username field, email only is used. It also brings and AbstractUser subclass.
- django_rest_framework views for user CRUD and change-password
- JWT authentication and views
- Simple password validators for common patterns (see configuration)

## Requirements

- Python 2.7, 3.6, 3.7
- Django 1.11, 2.0, 2.1, 2.2
- Django REST framework  3.9.x

## Installation

Install using pip

```pip install webpartners-users```

Add ```webpartners_users``` and ```rest_framework``` to your ```INSTALLED_APPS``` settings:

```python
INSTALLED_APPS = (
    ...
    'rest_framework',
    'webpartners_users',
)
```

Set your model class:

```python
# Package class
AUTH_USER_MODEL = 'webpartners_users.User'

# OR your own subclass
AUTH_USER_MODEL = 'my_app.User'
```

and optionally include our views to your urls.py:

```python
urlpatterns = [
    # ...
    path('', 'webpartners_users.urls'),
]
```

## Configuration

```python
# settings.py

# This is the default configuration

WEBPARTNERS_USERS = {
    'MIN_LENGTH': None,
    'AT_LEAST_ONE_NUMBER': False,
    'NUMERIC_DISALLOWED': False,
}
```

###### Sponsored by https://mrmilu.com
