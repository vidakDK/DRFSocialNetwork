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
`/api` to access the api
    `/users`
    `/posts`
    `/votes`

#### Actions:

* Send post request to `/register`



