import telebot
import datetime
from telebot_calendar import Calendar, RUSSIAN_LANGUAGE, CallbackData


calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1 = CallbackData('calendar_1', 'action', 'year', 'month', 'day')
now = datetime.datetime.now()
bot = telebot.TeleBot(token='5973020450:AAGVUIsP8Qyt7wTgc-7B89e94rkNZyL5hKk')