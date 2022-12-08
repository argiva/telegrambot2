import telebot

bot = telebot.TeleBot('5973020450:AAGVUIsP8Qyt7wTgc-7B89e94rkNZyL5hKk')


@bot.message_handler(content_types=['text'])
def get_text_command(message) -> None:
    """
    Реалзиация реакции бота на текстовые запросы пользователя telegram

    :param message: пересылаемое сообщение от пользователем telegram
    :return: None
    """
    if message.text.lower() in ['привет', '/start']:
        bot.send_message(message.from_user.id, f'Привет, {message.chat.username}! Это бот для поиска отелей. Для вывода списка команд введите /help')
    elif message.text.lower() == 'hello world':
        bot.send_message(message.from_user.id, f'Hello, {message.chat.username}!')
    elif message.text.lower() == "/help":
        bot.send_message(message.from_user.id,
                         '● /history — вывод истории поиска отелей\n'
                         '● /lowprice — вывод списка самых дешёвых отелей в городе\n'
                         '● /highprice — вывод списка самых дорогих отелей в городе\n'
                         '● /bestdeal — вывод списка отелей, наиболее подходящих по цене и расположению от центра\n')
    else:
        bot.send_message(message.from_user.id, 'Некорректная команда. Для вывода списка команд введите /help...')


bot.polling(none_stop=True, interval=0)
