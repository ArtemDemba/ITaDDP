import json
import socket


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


interviewer_addr = ()


def listen(host: str = '127.0.0.1', port: int = 3000):
    global interviewer_addr
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind((host, port))
    print(f'Listening at {host}:{port}')

    while True:
        message, addr = s.recvfrom(UDP_MAX_SIZE)

        print(message.decode('ascii'))

        # if str(addr[1]) + ' username' not in members:
        #     members[str(addr[1]) + ' username'] = addr

        if not message:
            continue

        print('members: ', members)
        is_check_message = check_initialize_message(message=message, addr=addr)
        if is_check_message:
            continue
        is_message_about_interviewer = check_message_about_interviewer(message=message)
        if is_message_about_interviewer:
            interviewer_addr = is_message_about_interviewer
            continue
        print(f'before sending to {interviewer_addr}\nmessage: {message}')
        s.sendto(message, interviewer_addr)
        print(f'after sending from {addr}')


if __name__ == '__main__':
    listen()
