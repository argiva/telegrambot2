from bot_data import bot
from steps import get_city


@bot.message_handler(commands=['highprice', 'lowprice', 'bestdeal'])
def get_message(message) -> None:
    """
    Функция приёма команды /highprice и её обработка

    :param message: сообщение от пользователя
    :return: None
    """
    bot.set_state(message.from_user.id, 1, message.chat.id)

    with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
        data.update({'command': message})
        bot.send_message(message.from_user.id, 'Введите город: ')
        bot.register_next_step_handler(message, get_city)


bot.polling(none_stop=True, interval=0)
