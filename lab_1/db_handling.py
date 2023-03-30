class SaverMessageHistory:
    __messages = []

    @classmethod
    def add_message(cls, username_from: str, username_to: str,  message: str) -> None:
        cls.__messages.append([username_from, username_to, message])

    @classmethod
    def save_to_db(cls):
        print('All message history: ')
        for user_from, user_to, message in cls.__messages:
            print(f'{user_from} - {user_to} - {message}')
        cls.__clear_messages()

    @classmethod
    def __clear_messages(cls):
        cls.__messages.clear()
