import json
import telebot
from telebot import types

with open('token.txt') as f:
    token = f.read()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Кинчик", "Сериальчик", "/Хелпе")
    bot.send_message(message.chat.id, 'Привет! Что хочется посмотреть?', reply_markup=keyboard)


@bot.message_handler(commands=['Хелпе'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Я простой кино боть созданный, чтобы упростить выбор вашего досуга. Потыкайте кнопочки и проведите врямя с удовольствием)')


@bot.message_handler(content_types=['text'])
def answer(message):
    with open('genre.json', encoding='utf-8') as f_in:
        filmography = json.load(f_in)
    if message.text == "Кинчик":
        markup = types.InlineKeyboardMarkup(row_width=3)
        di = dict()
        for data, name in filmography.items():
            di[name] = data
            if len(di) == 3:
                keys = list(di.keys())
                markup.add(types.InlineKeyboardButton(keys[0], callback_data=di[keys[0]]),
                           types.InlineKeyboardButton(keys[1], callback_data=di[keys[1]]),
                           types.InlineKeyboardButton(keys[2], callback_data=di[keys[2]]))
                di = {}

        bot.send_message(message.chat.id, 'Какой жанр хотите?', reply_markup=markup)

    elif message.text == "Сериальчик":
        sermarkup = types.InlineKeyboardMarkup(row_width=3)
        di = dict()
        for data, name in filmography.items():
            data = f"ser_{data}"
            di[name] = data
            if len(di) == 3:
                keys = list(di.keys())
                sermarkup.add(types.InlineKeyboardButton(keys[0], callback_data=di[keys[0]]),
                              types.InlineKeyboardButton(keys[1], callback_data=di[keys[1]]),
                              types.InlineKeyboardButton(keys[2], callback_data=di[keys[2]]))
                di = {}

        bot.send_message(message.chat.id, 'Какой жанр хотите?', reply_markup=sermarkup)
    else:
        bot.send_message(message.chat.id, 'Извините, я вас не понимаю(')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data[0:4] == 'ser_':
                bot.send_message(call.message.chat.id,
                                 f'Тогда вам сюда : https://www.kinopoisk.ru/lists/navigator/{call.data[4:]}/?quick_filters=serials&tab=all')
            else:
                bot.send_message(call.message.chat.id,
                                 f'Тогда вам сюда : https://www.kinopoisk.ru/lists/navigator/{call.data}/?quick_filters=films&tab=all')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Понял, принял", reply_markup=None)

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
