# DRF Social Network

Simple Social Network API implemented in Django Rest Framework (DRF).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installation

1. Install & activate virtual env:
    `python3 -m venv .env`
    `source ./env/bin/activate`

2. Install requirements:
    `pip3 install -r requirements.txt`

3. Source into API, create database, and migrate:
    `cd pynet`
    `python manage.py makemigrations`
    `python manage.py migrate`

4. Run Django server:
    `python manage.py runserver`

### API Details

#### Project URL structure:
url | `GET` action | `POST` action
--- | ------------ | -------------
`/register` | - | register new user
`/login` | - | login new user and obtain JWT token
`/logout` | - | logout current user
`/api/users` | list all registered users and their posts | -
`/api/posts` | view all current posts | create a new post |
`/api/votes` | view all current (user,post,like) tuples | like/unlike a post

#### Standard Actions:

* Send POST request to `/register` with required fields.
  Example:
  ```python
  request.data = {
    "email": "user@host.com",
    "first_name": "John",
    "last_name": "Doe",
    "password1": "password1",
    "password2": "password1"
  }
  ```

* Send POST request to `/login` with required fields.
  Example:
  ```python
  request.data = {
    "email": "user@host.com",
    "password": "password1",
  }
  ```
  Response gives JWT token in data:
  ```python
  token = response.json()['token']
  ```

* Send POST request to `/api/` with required fields and JWT token in the header:
  Example of a like action, action_type is 1 for like and 0 for unlike:
  ```python
  url = "http://127.0.0.1:8000/api/votes/"
  json = {
    "post_id": 1,
    "action_type": 1
  }
  headers = {
    "Content-Type": "application/json",
    "Authorization": "JWT {}".format(self.token),
  }
  response = requests.post(url=url, json=json, headers=headers)
  ```
  Analogue actions are made for creating posts and liking posts.


### Automated Bot

The bot satisfies pre-made conditions that test the API functionality, i.e. user/post registration, liking posts, etc.

It is started by running the following commands:
```
cd bot
python bot_actions.py
```

### Acknowledgments
* Thanks to the awesome django-rest-auth package from @tivix.
