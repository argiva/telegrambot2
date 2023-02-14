from bot_data import bot


def add_history(message):
    with open(f'{message.from_user.id}.log', 'a') as file:
        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            file.write(f'{data["time"].date()} {data["time"].time()}: команда {data["command"].text}\n\n')
            for hotel in data['answer']:
                file.write(f'{hotel}\n\n')
