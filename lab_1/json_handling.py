import json


def get_socket_using_username(username: str) -> tuple[str, int]:
    with open('users.json') as file:
        users = json.load(file)
    return tuple(users[username])


def get_username_using_socket(addr: tuple[str, int]) -> str:
    with open('users.json') as file:
        users = json.load(file)
    addr = list(addr)
    for username in users:
        if users[username] == addr:
            return username

