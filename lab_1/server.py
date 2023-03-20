import json
import socket

UDP_MAX_SIZE = 65535


members = {'45325 username': ('127.0.0.1', 45325), '41789 username': ('127.0.0.1', 41789)}  # key - username, value - (ip, port)


def listen(host: str = '127.0.0.1', port: int = 3000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind((host, port))
    print(f'Listening at {host}:{port}')

    while True:
        message, addr = s.recvfrom(UDP_MAX_SIZE)

        print(message.decode('ascii'))

        if str(addr[1]) + ' username' not in members:
            members[str(addr[1]) + ' username'] = addr

        if not message:
            continue

        client_id = addr[1]
        print('members: ', members)
        if message.decode('ascii').startswith('username'):
            print(f'Client {client_id} joined chat')
            with open('users.json') as file:
                users = json.load(file)
            with open('users.json', 'w') as file:
                users[message.decode('ascii').split()[1]] = list(addr)
                json.dump(users, file, ensure_ascii=False, indent=4)

        # msg = f'client{client_id}: {message.decode("ascii")}'
        s.sendto(message, members[message.decode('ascii') + ' username'])


if __name__ == '__main__':
    listen()
