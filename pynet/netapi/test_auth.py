#  Registration:
import requests


class AccountHandler:
    base_url = "http://127.0.0.1:8000/"
    registration_url = base_url + "registration/"
    login_url = base_url + "login/"
    update_url = base_url + "user/"

    def __init__(self, username, password, email, first_name, last_name):
        self.username = username
        self.password = password
        self.email = email
        self.token = None

    def register(self):
        data = {
            "username": self.username,
            "password1": self.password,
            "password2": self.password,
            "email": self.email
        }
        response = requests.post(url=self.registration_url, data=data)
        if int(response.status_code) == 201:
            self.token = response.json()['token']
            return True
        else:
            return False

    def login(self):
        data = {
            "username": self.username,
            "password": self.password,
            "email": self.email
        }
        response = requests.post(url=self.login_url, data=data)
        if int(response.status_code) == 201:
            self.token = response.json()['token']
            return True
        else:
            return False

    def add_name(self):
        """Requires that user be logged in"""
        data = {
            "username": self.username,

        }






reg_url = "http://127.0.0.1:8000/rest-auth/registration/"
reg_method = 'POST'
reg_data = {
    "username": "test8",
    "password1": "password123",
    "password2": "password123",
    "email": "test8@gmail.com",
    "first_name": "test8"
}
reg_put_data = {
    "username": "test8",
    "first_name": "Test8",
    "last_name": "Test8",
}
reg_resp_post = requests.post(url=reg_url, data=reg_data)

# Update to add details:
reg_url_put = "http://127.0.0.1:8000/rest-auth/user/"
reg_resp_put = requests.put(url=reg_url_put, data=reg_put_data)

print(reg_resp_put.text)

