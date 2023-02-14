from bot_data import bot
from steps import get_city
import datetime


@bot.message_handler(commands=['highprice', 'lowprice', 'bestdeal'])
def get_message(message) -> None:
    """
    Функция приёма команды /highprice и её обработка

    :param message: сообщение от пользователя
    :return: None
    """
    bot.set_state(message.from_user.id, 1, message.chat.id)

    with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
        data.update({'command': message, 'time': datetime.datetime.now(), 'answer': []})
        bot.send_message(message.from_user.id, 'Введите город: ')
        bot.register_next_step_handler(message, get_city)


@bot.message_handler(commands=['history'])
def get_history(message):
    try:
        with open(f'{message.from_user.id}.log', 'r') as file:
            bot.send_message(message.from_user.id, file.read())
    except FileNotFoundError:
        bot.send_message(message.from_user.id, 'История пуста')


bot.polling(none_stop=True, interval=0)
