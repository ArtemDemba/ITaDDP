import socket

UDP_MAX_SIZE = 65535


def listen(host: str = '127.0.0.1', port: int = 3000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind((host, port))
    print(f'Listening at {host}:{port}')

    members = {}  # key - username, value - port
    while True:
        message, addr = s.recvfrom(UDP_MAX_SIZE)

        print(message.decode('ascii'))

        if str(addr[1]) + ' username' not in members:
            members[str(addr[1]) + ' username'] = addr[1]

        if not message:
            continue

        client_id = addr[1]
        if message.decode('ascii') == '__join':
            print(f'Client {client_id} joined chat')
            continue

        # msg = f'client{client_id}: {message.decode("ascii")}'
        s.sendto(message, (addr[0], members[message.decode('ascii') + ' username']))


if __name__ == '__main__':
    listen()
