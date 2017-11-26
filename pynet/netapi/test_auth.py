#  Registration:
import requests


class AccountHandler:
    base_url = "http://127.0.0.1:8000/"
    registration_url = base_url + "rest-auth/registration/"
    login_url = base_url + "rest-auth/login/"
    update_url = base_url + "rest-auth/user/"

    def __init__(self, username, password, email, first_name, last_name):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.token = None

    @staticmethod
    def __send_request(url, data, headers, req_type):
        response = 0
        if req_type == 'POST':
            response = requests.post(url=url, json=data, headers=headers)

        elif req_type == 'GET':
            s = requests.Session()
            response = s.get(url=url, headers=headers, params=data)

        if int(response.status_code) in [200, 201]:
            return True, response
        else:
            return False, response

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
        if int(response.status_code) in [200, 201]:
            self.token = response.json()['token']
            return True
        else:
            print(response.text)
            return False

    def add_name(self):
        """Requires that user be logged in"""
        data = {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT {}".format(self.token),
        }
        response = requests.put(url=self.update_url, json=data, headers=headers)
        if int(response.status_code) in [200, 201]:
            return True
        else:
            print(response.text)
            return False

    def vote(self, vote_type):
        """vote_type is 1 for upvode and 0 for downvote"""
        url = self.base_url + "votes/up/"
        # param: model, id, vote
        # i.e.model = movies & id = 359 & vote = true
        data = {
            "model": "Post",
            "id": 1,
            "vote": "true" if vote_type else "false",
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "JWT {}".format(self.token),
        }
        req_type = 'GET'
        success, resp = self.__send_request(url, data, headers, req_type)
        return success, resp


ah = AccountHandler("test16", "password123", "test16@gmail.com", "Vidak", "Kazic")

## Register and update:
# reg_success = ah.register()
# if reg_success:
#     up_success = ah.add_name()
#     if up_success:
#         print("yay")
#     else:
#         print("failed updating name")
# else:
#     print("failed registration")

## Login:
login_success = ah.login()
if login_success:
    vote_success, vote_response = ah.vote(1)

print("end")


#
# reg_url = "http://127.0.0.1:8000/rest-auth/registration/"
# reg_method = 'POST'
# reg_data = {
#     "username": "test8",
#     "password1": "password123",
#     "password2": "password123",
#     "email": "test8@gmail.com",
#     "first_name": "test8"
# }
# reg_put_data = {
#     "username": "test8",
#     "first_name": "Test8",
#     "last_name": "Test8",
# }
# reg_resp_post = requests.post(url=reg_url, data=reg_data)
#
# # Update to add details:
# reg_url_put = "http://127.0.0.1:8000/rest-auth/user/"
# reg_resp_put = requests.put(url=reg_url_put, data=reg_put_data)
#
# print(reg_resp_put.text)
#
