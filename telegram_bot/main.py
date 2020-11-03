import requests
import asyncio
from aiogram import Bot, Dispatcher, exceptions, types
import logging
import config
import bd1
# client = telebot.TeleBot(config.config['token'])

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.config['token'])
dp = Dispatcher(bot)

# @client.message_handler(commands=['info'])
# def get_user_info(message):
#     markup_inline = types.InlineKeyboardMarkup()
#     item_yes = types.InlineKeyboardButton(text='ДА', callback_data='yes')
#     item_no = types.InlineKeyboardButton(text='НЕТ', callback_data='no')
#
#     markup_inline.add(item_yes, item_no)
#     client.send_message(message.chat.id, 'хотите узнать информачию о вас?',
#                         reply_markup=markup_inline)


@dp.message_handler(commmands=['start', 'help'])
def get_text(message):
    if message.text == 'Hi' or message.text == 'Hello' or  message.text == 'hi':
        dp.send_message(message.chat.id, f'Здравствуйте {message.from_user.first_name} '
                                             f'{message.from_user.last_name}')
    else:
        pass


dp.polling(none_stop=True, interval=1)


@dp.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'yes':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_username = types.KeyboardButton('my info')
        item_chat = types.KeyboardButton('Chat info')

        markup_reply.add(item_username, item_chat)
        dp.send_message(call.message.chat.id, 'Выберете кнопку', reply_markup=markup_reply)
    elif call.data == 'no':
        pass


# def get_updates_json(request):
#     response = requests.get(request + 'getUpdates')
#     return response.json()


# def last_update(data):
#     results = data['result']
#     total_updates = len(results) - 1
#     return results[total_updates]
#
#
# def get_chat_id(update):
#     chat_id = update['message']['chat']['id']
#     return chat_id
#
#
# def send_mess(chat, text):
#     params = {'chat_id': chat, 'text': text}
#     response = requests.post(url + 'sendMessage', data=params)
#     return response
#
#
# def main():
#     update_id = last_update(get_updates_json(url))['update_id']
#     while True:
#         if update_id == last_update(get_updates_json(url))['update_id']:
#            send_mess(get_chat_id(last_update(get_updates_json(url))), 'test')
#            update_id += 1
#         sleep(1)
#
#
# if __name__ == '__main__':
#     main()
#
# chat_id = get_chat_id(last_update(get_updates_json(url)))
# send_mess(chat_id, 'Your message goes here')