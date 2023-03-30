import socket
import threading
import os
import json

from server import members
import json_handling
import db_handling


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


def connect(username: str, username_to_chat: str, s: socket.socket):
    while True:
        msg = input(f'you: ')
        if msg == 'q':
            # show_all_dialogues_of_user(username, s)
            db_handling.SaverMessageHistory.save_to_db()
        s.send(str(username_to_chat + '~' + msg).encode('ascii'))
        db_handling.SaverMessageHistory.add_message(username_from=username, username_to=username_to_chat, message=msg)


def send_initialize_message(username: str, s: socket.socket):
    with open('users.json') as file:
        users = json.load(file)
    users[username] = list(s.getsockname())
    with open('users.json', 'w') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)


def send_info_about_interviewer(username_to_chat: str, s: socket.socket) -> None:
    s.send(f'interviewer~{username_to_chat}'.encode('ascii'))


def remove_user_socket(username: str) -> None:
    with open('users.json') as file:
        users = json.load(file)
    users[username] = []
    with open('users.json', 'w') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)


def show_all_dialogues_of_user(username: str, s: socket.socket):
    os.system('clear')
    print_all_users(username)
    username_to_chat = input('Write down username to chat: ')
    if username_to_chat == 'q':
        remove_user_socket(username)
        show_registration_page()
    else:
        # send_info_about_interviewer(username_to_chat, s)
        connect(username, username_to_chat, s)


def show_registration_page():
    username = input('Write down your username: ')

    host = '127.0.0.1'
    port = 3000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.connect((host, port))

    threading.Thread(target=listen, args=(s,), daemon=True).start()
    send_initialize_message(username, s)
    show_all_dialogues_of_user(username, s)


if __name__ == '__main__':
    show_registration_page()
