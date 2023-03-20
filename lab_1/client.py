import socket
import threading
import os
import json

from server import members

UDP_MAX_SIZE = 65535


def print_all_users(username: str) -> None:
    with open('users.json') as file:
        users = json.load(file)
        for username in [user for user in users if user != username]:
            print(username)
    # message_with_users = ''
    # for user in members.values():
    #     for username, address in members.items():
    #         if user != address:
    #             message_with_users += username + str(address[0]) + ' ' + str(address[1]) + '\n'
    #     print(message_with_users)
    #     message_with_users = ''


def listen(s: socket.socket):
    while True:
        msg = s.recv(UDP_MAX_SIZE)
        print('\r\r' + msg.decode('ascii') + '\n' + f'you: ', end='')


def connect(username: str, host: str = '127.0.0.1', port: int = 3000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.connect((host, port))

    threading.Thread(target=listen, args=(s,), daemon=True).start()

    s.send(f'username {username}'.encode('ascii'))

    while True:
        msg = input(f'you: ')
        s.send(msg.encode('ascii'))


def show_registration_page():
    username = input('Write down your username: ')
    # with open('users.json') as file:
    #     users = json.load(file)
    # users[username] = []
    # with open('users.json', 'w') as file:
    #     json.dump(users, file, ensure_ascii=False, indent=4)

    show_all_dialogues_of_user(username)


def show_all_dialogues_of_user(username: str):
    print_all_users(username)
    connect(username)

    # username = input('Write down username: ')
    if username == 'q':
        show_start_page()


def show_login_page():
    username = input('Write down your username: ')
    with open('users.json') as file:
        users = json.load(file)
    if username in users:
        show_all_dialogues_of_user(username)
    elif username == 'q':
        show_start_page()
    else:
        raise ValueError("This username doesn't exist(")


def show_start_page():
    os.system('clear')
    print('Registration')
    print('Log in')
    start_page = input('1 - Registration, 2 - Log in\n')
    match start_page:
        case '1':
            show_registration_page()
        case '2':
            show_login_page()
        case 'q':
            exit()
        case _:
            raise ValueError('Incorrect choice(')


if __name__ == '__main__':
    show_start_page()
    # connect('')
