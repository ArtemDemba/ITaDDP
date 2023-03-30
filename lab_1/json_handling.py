import json


def get_socket_using_username(username: str):
    with open('users.json') as file:
        users = json.load(file)
    return tuple(users[username])
