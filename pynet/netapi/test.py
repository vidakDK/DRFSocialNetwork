import requests

data = {
    "email": "vidakdk@gmail.com",
    "username": "vidak",
    "password": "password123",
    "first_name": "Vidak",
    "last_name": "Kazic",
}
url = "http://127.0.0.1:8000/users/"

# AUTH
token_url = "http://127.0.0.1:8000/api-token-auth/"
token_credentials = {"username": "vidak",
                     "password": "password123"}
token_header = {"Content-Type": "application/json"}
token_response = requests.post(url=token_url, json=token_credentials, headers=token_header)

auth_header = {"Authorization": "JWT {}".format(token_response.text)}

# Send Request
resp_gg = requests.post(url=url, data=data)
resp = requests.post(url=url, data=data, headers=auth_header)

print(resp.content)