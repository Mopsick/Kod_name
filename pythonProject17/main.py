# import telebot
# import json
# from telebot import types
# from datetime import datetime, date, time, timedelta
#
# TOKEN = "7204248058:AAH6RbR1tZOr7eZZUm-TqlIqtJgDYfunRPk"
#
# bot = telebot.TeleBot(TOKEN)
#
#
# @bot.message_handler(commands=["start"])
# def handle_start(message):
#     bot.send_message(message.chat.id, "Привет!")
#
#
# @bot.message_handler(commands=['show_dates'])
# def handle_schedule(message):
#     keyboard = generate_date_schedule()
#     bot.send_message(message.chat.id, "Выберите день:", reply_markup=keyboard)
#
#
# def generate_date_schedule():
#     keyboard = types.InlineKeyboardMarkup()
#
#     days = []
#
#     for i in range(7):
#         days.append(date.today() + timedelta(days=3 + i))
#
#     for button_text in days:
#         callback_data = f"day:{button_text}"
#         button = types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
#         keyboard.add(button)
#
#     return keyboard
#
#
# def generate_time():
#     keyboard = types.InlineKeyboardMarkup()
#
#     # Получаем кнопки для указанной даты
#     times = ["10:00", "12:00", "15:00", "17:00"]
#
#     for time in times:
#         callback_data = f"meeting:{time}"
#         button = types.InlineKeyboardButton(text=time, callback_data=callback_data)
#         keyboard.add(button)
#
#     return keyboard
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def handle_callback_query(call):
#     if call.data.startswith("day:"):
#         chosen_date = call.data.split(":")[1]
#         bot.send_message(call.message.chat.id, f"Вы выбрали дату: {chosen_date}")
#         bot.send_message(call.message.chat.id, "Выберите время:", reply_markup=generate_time())
#     elif call.data.startswith("time:"):
#         c_time = call.data.split(":")[1]
#         bot.send_message(call.message.chat.id, f"Вы выбрали время: {c_time}")
#
#
# def add_appointment(date, time, client):
#     try:
#         with open("data.json", "r", encoding="utf-8") as file:
#             user_data = json.load(file)
#     except FileNotFoundError:
#         user_data = {"appointments": [], "review": []}
#     new_appointments = {"date": date, "time": time, "client": client}
#     user_data["appointments"].append(new_appointments)
#
#     with open("data.json", "w", encoding="utf-8") as file:
#         json.dump(user_data, file, ensure_ascii=False, indent=4)
#
#
# def add_review(client, text):
#     try:
#         with open("data.json", "r", encoding="utf-8") as file:
#             user_data = json.load(file)
#     except FileNotFoundError:
#         user_data = {"appointments": [], "review": []}
#     new_review = {"client": client, "text": text}
#     user_data["review"].append(new_review)
#
#     with open("data.json", "w", encoding="utf-8") as file:
#         json.dump(user_data, file, ensure_ascii=False, indent=4)
#
#
# if __name__ == "__main__":
#     bot.polling(non_stop=True)


import random

import telebot
from telebot import types
import json
from datetime import date, timedelta

TOKEN = "7204248058:AAH6RbR1tZOr7eZZUm-TqlIqtJgDYfunRPk"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет")


@bot.message_handler(commands=['show_dates'])
def handle_schedule(message):
    """Выбор даты"""
    # Отправляем клавиатуру с кнопками

    keyboard = generate_date_schedule()
    bot.send_message(message.chat.id, "Выберите день:", reply_markup=keyboard)


def generate_date_schedule():
    keyboard = types.InlineKeyboardMarkup()

    # Получаем кнопки для указанной даты
    days = []

    for i in range(7):
        days.append(date.today() + timedelta(days=3 + i))

    # Создаем кнопки и добавляем их на клавиатуру
    for button_text in days:
        callback_data = f"day:{button_text}"
        button = types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
        keyboard.add(button)

    return keyboard


def generate_time_keyboard(date):
    keyboard = types.InlineKeyboardMarkup()

    # Получаем кнопки для указанной даты
    times = ["10:00", "12:00", "15:00", "17:00"]

    # Создаем кнопки и добавляем их на клавиатуру
    for time in times:
        callback_data = f"meeting: {date} {time}"
        button = types.InlineKeyboardButton(text=time, callback_data=callback_data)
        keyboard.add(button)

    return keyboard


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data.startswith("day:"):
        chosen_date = call.data.split(":")[1]
        bot.send_message(call.message.chat.id, f"Вы выбрали дату: {chosen_date}")
        # Отправляем клавиатуру с доступным временем
        bot.send_message(call.message.chat.id, "Выберите время:", reply_markup=generate_time_keyboard())

    elif call.data.startswith("time:"):
        chosen_time = call.data.split(":")[1]
        bot.send_message(call.message.chat.id, f"Вы выбрали время: {chosen_time}")


def add_appointment(date, time, client):
    # Чтение существующих данных из файла
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"appointments": [], "review": []}

    # Добавление новой записи
    new_appointment = {'date': date, 'time': time, 'client': client}
    data['appointments'].append(new_appointment)

    # Запись обновленных данных в файл
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


def add_review(client, text):
    try:
        # Чтение данных из файла
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        # Если файла нет, создаем пустую структуру
        data = {"appointments": [], "review": []}

    # Добавление нового отзыва в список отзывов
    data["review"].append({
        "client": client,
        "text": text
    })

    # Сохранение обновленных данных в файл
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
