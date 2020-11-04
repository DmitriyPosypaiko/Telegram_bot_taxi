from telebot import TeleBot, types
from config import BOT_TOKEN, api_key
import requests
from bd1 import select_user, insert_user_row, is_authenticated
bot = TeleBot(BOT_TOKEN)
headers={'dev': api_key}


@bot.message_handler(content_types=['text'])
def get_text(message):
    bot.send_message(message.chat.id, f'Здравствуйте {message.from_user.first_name} '
                                         f'{message.from_user.last_name}')
    msg = bot.send_message(message.chat.id, 'Пожалуйста укажите свой позывной и пароль через пробел')
    bot.register_next_step_handler(msg, name_password_step)
    # bot.register_next_step_handler(send, create_uis(message))
    # authenticate = requests.post('https://txcloud.atlassian.net/wiki/spaces/API/drivers/sign-in/',
    #                              params={'login': name, 'password': password}, headers=headers)
    #                               information is required whether the user is registered as a driver


@bot.message_handler(commands=["help"])
def name_password_step(message):
    try:
        name = message.text.split()[0]
        password = message.text.split()[1]
        msg = bot.send_message(message.chat.id, f"login: {name}, password: {password}")
        if msg:
            create_user(message)
    except Exception as e:
        bot.reply_to(message, 'oooops')
        get_text(message)


@bot.message_handler(content_types=['text'])
def create_user(message):
    authenticate = True
    if authenticate:
        if is_authenticated([message.from_user.id]):
            send = bot.send_message(message.chat.id, 'Вы зарегистрированы')
            bot.register_next_step_handler(send, menu(message))
        else:
            insert_user_row([message.from_user.first_name, message.from_user.id])
            print('Print select user:  ', select_user())
            menu(message)

    else:
        bot.send_message(message.chat.id, f'Вы не зарегистрированы как водитель, пожалуйста удостоверьтесь '
                                          f'что у вас есть аккаунт, пройдя по этой ссылке.\n'
                                          f'https://demo-kiev.ligataxi.com/accounts/login/')


@bot.message_handler(content_types=['text'])
def menu(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_balance = types.InlineKeyboardButton(text='Пополнить баланс водителя', callback_data='balance')
    item_history_balance = types.InlineKeyboardButton(text='Посмотреть историю пополнений',
                                                      callback_data='history_balance')
    item_settings_commission = types.InlineKeyboardButton(text='Задать настройки комиссии',
                                                          callback_data='settings_commission')
    markup_inline.add(item_balance)
    markup_inline.add(item_history_balance)
    markup_inline.add(item_settings_commission)
    bot.send_message(message.chat.id, f'Добро пожаловать', reply_markup=markup_inline)


@bot.callback_query_handler(func = lambda call: True)
def balance(call):
    '''
        Тут нужно получить обьект driver с API JIRA, но так как на данный момент нету возможности получить
        эти данные код очень приблезителен и скорее всего запросы будут иными и с использованием методов самого API JIRA
    '''
    # driver = requests.post('https://txcloud.atlassian.net/wiki/spaces/API/drivers/sign-in/',
    #                        params={'login': name, 'password': password}, headers=headers)
    if call.data == 'balance':
        # if driver:
        msg = bot.send_message(call.message.chat.id, f'Пожалуйста введите сумму платежа')
        bot.register_next_step_handler(msg, velues_balance)

    elif call.data == 'history_balance':
        # if driver:
        '''
            Также нужно получить данные о клиенте для того чтобы получить историю его платежей с указаными параметрами
            'limit' и тд.
        '''
        bot.send_message(call.message.chat.id, f'Также нужно получить данные о клиенте для того чтобы получить историю '
                                               f'его платежей с указаными параметрами limit')
        # req = requests.get('https://txcloud.atlassian.net/wiki/spaces/API/drivers/history/',
        #                    params={'driver_id': driver['driver_id'], 'limit': 10})
        # bot.send_message(call.message.chat.id, f'{req}')
    if call.data == 'settings_commission':
        msg = bot.send_message(call.message.chat.id, f'Плжалуйста укажите минимальную, максимальную, процент комиссии и'
                                                     f' фикс. комиссию, через пробел')
        bot.register_next_step_handler(msg, velues_commission_settings)


@bot.message_handler(commands=["help"])
def velues_commission_settings(message):
    try:
        minimum = message.text.split()[0]
        maximum = message.text.split()[1]
        percent = message.text.split()[2]
        fixed_commission = message.text.split()[3]
        msg = bot.send_message(message.chat.id, f"minimum: {minimum}, maximum: {maximum}\n"
                                                f"percent: {percent}, fixed_commission: {fixed_commission}")
        if msg:
            set_settings_commission(message, minimum, maximum, percent, fixed_commission)
    except Exception as e:
        bot.reply_to(message, 'ooops')


def set_update_balance(message, payment):
    '''
        здесь должен быть post запрос driver.fin_operation.create с параметрами
        {
            'driver_id': int
            'payment': float
            'comment': str
        }

    '''
    # driver = requests.post('https://txcloud.atlassian.net/wiki/spaces/API/drivers/sign-in/',
    #                        params={'login': name, 'password': password}, headers=headers)
    # if driver:
    # req = requests.post('https://txcloud.atlassian.net/wiki/spaces/API/drivers/fin_operation/create/',
    #                     params={'driver_id': driver['driver_id'], 'payment': payment}, headers=headers)
    # else:
    # bot.send_message(call.message.chat.id, f'Вы не зарегистрированы как водитель, пожалуйста удостоверьтесь '
    #                                      f'что у вас есть аккаунт, пройдя по этой ссылке.\n'
    #                                      f'https://demo-kiev.ligataxi.com/accounts/login/')
    bot.send_message(message.chat.id, f'Баланс пополнен на сумму: {payment}')


@bot.message_handler(commands=["help"])
def velues_balance(message):
    try:
        payment = message.text.split()[0]
        msg = bot.send_message(message.chat.id, f'payment: {int(payment)}')
        if msg:
            set_update_balance(message, payment)
    except Exception as e:
        bot.reply_to(message, 'ooops')

def set_settings_commission(message, munimum, maximum, percent, fixed_commission):
    '''
        Как будет возможность взаимодействовать с API JIRA, появитсься возможность передать все нужные параметры
        такие как  munimum, maximum, percent, fixed_commission
    '''
    # driver = requests.post('https://txcloud.atlassian.net/wiki/spaces/API/drivers/sign-in/',
    #                        params={'login': name, 'password': password}, headers=headers)
    # driver.fin_operation.create(driver_id=driver['driver_id'], payment=payment)
    bot.send_message(message.chat.id, f'Настройки комиссии заданы')

bot.polling(none_stop=True, interval=0)