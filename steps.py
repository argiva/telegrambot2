import req
import telebot
from bot_data import bot, calendar_1, calendar, now, Calendar


@bot.callback_query_handler(func=lambda call: call.data.isalnum())
def callback_worker(call) -> None:
    """
    Обработчик нажатия на inline клавиатуру

    :param call: значение нажатой кнопки
    :return: None
    """
    bot.delete_message(call.message.chat.id, call.message.message_id)

    with bot.retrieve_data(call.from_user.id) as data:

        if data['operation'] == 'get_in':
            data.update({'city_id': call.data, 'operation': 'get_out'})
            bot.send_message(call.from_user.id, f'Вы выбрали {data["city_list"][call.data]}')
            get_date(data['command'], 'Введите дату заселения:')
        elif call.data == 'Да' and data['operation'] == 'get_city':
            bot.send_message(call.from_user.id, 'Введите город: ')
            bot.register_next_step_handler(call.message, get_city)
        elif call.data == 'Да' and data['operation'] == 'get_photo':
            bot.send_message(call.from_user.id, 'Введите количество фотографий: ')
            bot.register_next_step_handler(call.message, get_photo)
        elif call.data == 'Да' and data['operation'] == 'get_size':
            bot.send_message(call.from_user.id, 'Введите количество выводимых результатов поиска: ')
            bot.register_next_step_handler(call.message, get_results_size)
        elif call.data == 'Нет':
            bot.send_message(call.from_user.id, 'Введите команду. Для вывода списка команд введите /help...')


@bot.callback_query_handler(func=Calendar)
def callback_calendar(call) -> None:
    """
    Обработчик Inline календаря

    :param call: значение нажатой кнопки
    :return: None
    """
    name, action, year, month, day = call.data.split(calendar_1.sep)
    date = calendar.calendar_query_handler(bot=bot, call=call, name=name, action=action, year=year, month=month, day=day)

    with bot.retrieve_data(call.from_user.id) as data:
        if action == 'DAY' and data['operation'] == 'get_out':
            bot.send_message(call.from_user.id, f'Вы выбрали дату заселения: {date.date()}')
            data.update({'operation': 'get_photo', 'check_in': date})
            get_date(data['command'], 'Введите дату выселения:')
        elif action == 'DAY' and data['operation'] == 'get_photo':
            data['check_out'] = date
            bot.send_message(call.from_user.id, f'Вы выбрали дату выселения: {date.date()}')
            bot.send_message(call.from_user.id, 'Введите количество фотографий: ')
            bot.register_next_step_handler(call.message, get_photo)
        elif action == 'CANCEL':
            bot.send_message(call.from_user.id, 'Введите команду. Для вывода списка команд введите /help...')


def get_city(message) -> None:
    """
    Функция выбора города и возврат пользователю результата с вариантами местоположения

    :param message: сообщение пользователя
    :return: None
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    with bot.retrieve_data(message.from_user.id) as data:
        data.update({'city_list': req.get_city_id(message.text), 'operation': 'get_city'})
        if data['city_list']:
            for city in data['city_list']:
                keyboard.add(telebot.types.InlineKeyboardButton(text=data['city_list'][city], callback_data=city))
            data['operation'] = 'get_in'
            bot.send_message(message.from_user.id, 'Выберите подходящий вариант из списка:', reply_markup=keyboard)
        else:
            for answer in ['Да', 'Нет']:
                keyboard.add(telebot.types.InlineKeyboardButton(text=answer, callback_data=answer))
            data['operation'] = 'get_city'
            bot.send_message(message.from_user.id, 'Ничего не найдено. Хотите повторить?', reply_markup=keyboard)


def get_date(message, text: str) -> None:
    """
    Функция отправки пользователю календаря для выбора дат

    :param message: сообщение пользователя
    :param text: аннотация к календарю для пользователя
    :return: None
    """
    bot.send_message(message.from_user.id, text,
                     reply_markup=calendar.create_calendar(
                         name=calendar_1.prefix,
                         year=now.year,
                         month=now.month
                                                          )
                     )


def get_photo(message) -> None:
    """
    Функция выбора пользователем количества выводимых фотографий

    :param message: сообщение пользователя
    :return: None
    """
    keyboard = telebot.types.InlineKeyboardMarkup()
    if message.text.isdigit():
        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            data.update({'photo': [num for num in range(int(message.text))], 'operation': 'get_size'})
        bot.send_message(message.from_user.id, 'Введите количество выводимых результатов поиска:')
        bot.register_next_step_handler(message, get_results_size)
    else:
        for answer in ['Да', 'Нет']:
            keyboard.add(telebot.types.InlineKeyboardButton(text=answer, callback_data=answer))
        bot.send_message(message.from_user.id, 'Необходимо ввести цифру. Хотите повторить?', reply_markup=keyboard)


def get_results_size(message) -> None:
    """
    Функция выбора количества выводимых отелей пользователем

    :param message: сообщение пользователя
    :return: None
    """
    keyboard = telebot.types.InlineKeyboardMarkup()
    if message.text.isdigit():
        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            data['resultsSize'] = int(message.text)
        results(message)
    else:
        for answer in ['Да', 'Нет']:
            keyboard.add(telebot.types.InlineKeyboardButton(text=answer, callback_data=answer))
        bot.send_message(message.from_user.id, 'Необходимо ввести цифру. Хотите повторить?', reply_markup=keyboard)


def results(message) -> None:
    """
    Функция отправки пользователю результатов поиска отелей

    :param message: сообщение пользователя
    :return: None
    """
    with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
        js = req.get_hotel_id(cache=data)
    for hotel in js:
        bot.send_message(message.from_user.id, hotel['text'])
        bot.send_message(message.from_user.id, 'Фотографии:')
        if data['photo']:
            for photo in hotel['photo']:
                bot.send_photo(message.from_user.id, photo)