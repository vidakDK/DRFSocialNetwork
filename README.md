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

### Usage

#### Project URL structure:
`/register` to register
`/login` to login
`/logout` to logout
`/api` to access the api
    `/users`
    `/posts`
    `/votes`

#### Actions:

* Send POST request to `/register` with required fields.
  Example:
  ```
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
  ```
  request.data = {
    "email": "user@host.com",
    "password": "password1",
  }
  Response gives JWT token in data:
  ```
  token = response.data
  ```

* Send POST request to `/api` with required fields and JWT token in the header:
  Example of a like action, action_type is 1 for like and 0 for unlike:
  ```
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



