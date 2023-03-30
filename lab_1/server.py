import json
import socket

import db_handling
import json_handling

UDP_MAX_SIZE = 65535

members = {'45325 username': ('127.0.0.1', 45325),
           '41789 username': ('127.0.0.1', 41789)}  # key - username, value - (ip, port)


def check_initialize_message(message: bytes, addr: tuple) -> bool:
    if message.decode('ascii').startswith('username~'):
        print(f'Client {message.decode("ascii").split("~")[1]} joined chat')
        with open('users.json') as file:
            users = json.load(file)
        with open('users.json', 'w') as file:
            users[message.decode('ascii').split('~')[1]] = list(addr)
            json.dump(users, file, ensure_ascii=False, indent=4)
        return True
    return False


def check_message_about_interviewer(message: bytes) -> tuple[str, int] or bool:
    if message.decode('ascii').startswith('interviewer~'):
        with open('users.json') as file:
            users = json.load(file)
        if message.decode('ascii').split('~')[1] in users:
            print(tuple(users[message.decode('ascii').split('~')[1]]))
            return tuple(users[message.decode('ascii').split('~')[1]])
    return False


def listen(host: str = '127.0.0.1', port: int = 3000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind((host, port))
    print(f'Listening at {host}:{port}')

    while True:
        message, addr = s.recvfrom(UDP_MAX_SIZE)

        print(message.decode('ascii'))

        if not message:
            continue

        username_to_chat, msg = message.decode('ascii').split('~')
        interviewer_addr = json_handling.get_socket_using_username(username_to_chat)
        user_from = json_handling.get_username_using_socket(addr)
        db_handling.SaverMessageHistory.add_message(username_from=user_from,
                                                    username_to=username_to_chat,
                                                    message=msg)
        s.sendto(msg.encode('ascii'), interviewer_addr)
        print(f'after sending from {addr}')


if __name__ == '__main__':
    listen()
