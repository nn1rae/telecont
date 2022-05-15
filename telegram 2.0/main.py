import random
import string
from telebot import types
import telebot
from tinydb import TinyDB, Query
bot = telebot.TeleBot("5311428361:AAHmz1afEFRPBjN6fSHeARvarmyeNzsWIOA")
db = TinyDB('waldb.json')
q = Query()

admin_list = [999711677]
def addbal(id,ball):
    db.update({'ball': getuser(id) + ball}, q.userid == id)
def new_sell_id():
    prom_temp = ''
    alfab = string.ascii_uppercase + string.digits
    for i in range(8):
        prom_temp += random.choice(alfab)
    return prom_temp 
def get_sell_cost(id):
    list = db.search(q.id == id)
    list = list[0]
    return list['cost']
def sell(text: str, creator:str, cost = 1):
    id_j = new_sell_id()
    db.insert({'type': 'sell', 'text': text, 'creator': creator, 'cost': cost, 'id': id_j})
    return id_j


def user_name_to_id(username):
    user = db.search(q.username == username)
    if not user:
        return "NOT FOUND"
    else:
        return user[0]['userid']
def getuser(id,to_get = 'ball'):
    toto = db.search(q.userid == id)
    if not toto:
        return "NOT FOUND"
    else:
        return toto[0][to_get]
def transaction(froo: int, too: int, much: int):
    print('transaction from {} to {} ({})'.format(getuser(froo, 'username'),getuser(too, 'username'), much))
    db.update({'ball': getuser(froo) - much}, q.userid == froo)
    db.update({'ball': getuser(too) + much}, q.userid == too)
def new_user(data):
    id = data.from_user.id 
    username = data.from_user.username
    usid = db.search(q.userid == id)
    if not usid:
        db.insert({'userid': id, 'username': username, 'ball': 0, 'type': 'user'}) 
        return True
    else:
        return False
def new_code():
    prom_temp = ''
    alfab = string.ascii_uppercase + string.digits
    for i in range(9):
        prom_temp += random.choice(alfab)
    return prom_temp 
def get_code_much(code: str):
    code_l = db.search(q.code == code)
    return int(code_l[0]['much'])

def del_code(code):
    db.remove(q.code == code)
def check_code(code):
    check_l = db.search(q.code == code)
    if not check_l:
        return False
    else:
        return True
def menu_mark():
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton("Мой кошелек🏦")
    itembtn2 = types.KeyboardButton("Отправить моржей🦭")
    itembtn3 = types.KeyboardButton("Магазин🛒")
    itembtn4 = types.KeyboardButton("Мои продажи🪜")
    return markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

@bot.message_handler(commands=['nc'])
def newnew(message):
    if message.from_user.id in admin_list:
        sent = bot.send_message(message.chat.id, 'Сколько🦭?')
        bot.register_next_step_handler(sent, nnj)
def nnj(message):
    nn = new_code()
    db.insert({'type': 'code', 'code': nn, 'much': int(message.text)})
    bot.send_message(message.chat.id, nn)
@bot.message_handler(commands=['cc'])
def cc(message):
    if message.from_user.id in admin_list:
        codes = ''
        temP_c = db.search(q.type == 'code')
        if not temP_c:
            bot.send_message(message.chat.id, 'нема кодов')
        else:
            for i in range(len(temP_c)):
                codes += temP_c[i]['code'] + ' ({})'.format(temP_c[i]['much']) + '\n'
            bot.send_message(message.chat.id, codes)

@bot.message_handler(commands=['start'])
def start(message):
    new_user_status = new_user(message)
    match new_user_status:
        case True:
            bot.send_message(message.chat.id, 'Акаунт создан🧺', reply_markup=menu_mark())
        case False:
            bot.send_message(message.chat.id, 'И снова здравствуйте', reply_markup=menu_mark())


@bot.message_handler(content_types=['text'])   
def text(message):
    new_user(message)
    if len(message.text) == 9:
        codes = db.search(q.type == 'code')
        if check_code(message.text):
            addbal(message.from_user.id, get_code_much(message.text))
            del_code(message.text)
            bot.send_message(message.chat.id, 'Успешно активировал {}🦭'.format(codes[0]['much']))
            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEEvIJigWmhXxLdMBI1TM7mCaAuStA5bQACMBkAAjalGUovXTYAAT6tdfkkBA")
    else:
        match message.text:
            case "Мой кошелек🏦":
                bot.send_message(message.chat.id, 'На твоем кошельке в данный момент {}🦭'.format(getuser(message.from_user.id, 'ball')))
                bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEEvHJigWmN5m5yloTGPlAwe09WCs-VMgACzhgAAugXiEkYalZKAtxN1CQE")
            case "Отправить моржей🦭":
                if getuser(message.from_user.id) > 0:
                    user_db = db.search(q.type == 'user')
                    user_list = ''
                    for i in range(len(user_db)):
                        user_list += str(user_db[i]['username']) + '\n'
                    sent = bot.send_message(message.chat.id, 'Кому отправляем?🚬')
                    bot.send_message(message.chat.id, user_list)
                    bot.register_next_step_handler(sent, handler_to_get_to_who_sent)
                else:
                    bot.send_message(message.chat.id, 'У тебя {}🦭'.format(getuser(message.from_user.id)))
                    bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAEEvHRigWmQ_sNfD-ND5sF4Dw5VUmlkHQAC9hQAAp29kUnq7g7zsQk01iQE")
            case "Магазин🛒":
                temp_var = 0
                buy_list = db.search(q.type == 'sell')
                if not buy_list:
                    bot.send_message(message.chat.id, 'Пока что ничего не продаеться🛌')
                    bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAEEvGxigWmH9KWM_Yq8mZ_wRYCveW_BNgACCRgAArj1yEnK5EQMf2T4RiQE")
                else:
                    for i in range(len(buy_list)):
                        if buy_list[i]['creator'] != getuser(message.from_user.id, "username"):
                            temp_var += 1
                            mj_markup = types.InlineKeyboardMarkup()
                            m1 = types.InlineKeyboardButton('Купить💳', callback_data='b' + buy_list[i]['id'])
                            mj_markup.add(m1)
                            bot.send_message(message.chat.id, '{}\n———————————\nСтоимость🍰: {}\nВладелец обьявления {}'.format(buy_list[i]['text'], buy_list[i]['cost'], buy_list[i]['creator']), reply_markup=mj_markup)
                    if temp_var == 0:
                        bot.send_message(message.chat.id, 'Ничего не продаеться🗞')
            case "Мои продажи🪜":
                temp_var = 0
                my_sells = db.search(q.type == 'sell') 
                if my_sells:
                    for i in range(len(my_sells)):
                        if my_sells[i]['creator'] == getuser(message.from_user.id, 'username'):
                            temp_var += 1
                            mj_markup = types.InlineKeyboardMarkup()
                            m1 = types.InlineKeyboardButton('❌Удалить', callback_data='0' + my_sells[i]['id'])
                            mj_markup.add(m1)
                            bot.send_message(message.chat.id, '{}\n———————————\nСтоимость🦭: {}'.format(my_sells[i]['text'], my_sells[i]['cost']), reply_markup=mj_markup)
                    if temp_var == 0:
                        bot.send_message(message.chat.id, 'У тебя нет продаж🧋')
                else:
                    bot.send_message(message.chat.id, 'У тебя нет продаж🧋')
                markup_sell = types.InlineKeyboardMarkup()
                m1 = types.InlineKeyboardButton('Продать🍸', callback_data='s')
                markup_sell.add(m1)
                bot.send_message(message.chat.id, 'Создать обьявление о продаже💶', reply_markup=markup_sell)
            
            
            
            case _:
                bot.send_message(message.chat.id, 'Увы я вас не понял🌡')
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEEvHhigWmVmmQ_ZLMOJMDhno5M5ZuoxgACdRcAAn63uUn3C806paO7uCQE')
            
user_to_send = ''
def handler_to_get_to_who_sent(message):
    global user_to_send
    
    if db.search(q.username == message.text):
        user_to_send = message.text
        bot.send_message(message.chat.id, 'Доступно {}🦭'.format(getuser(message.from_user.id)))
        sent = bot.send_message(message.chat.id, 'Сколько отправить?♻️')
        bot.register_next_step_handler(sent, how_much_sent)
    else:
        bot.send_message(message.chat.id,'Пользователь не найден📡')
        bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAEEvGpigWmE6w9WQpqCbGzBpU96Szq3ewACyxkAAt0gaUmGDL3McQ00tCQE")
def how_much_sent(message):
    global user_to_send
    try:
        mts = getuser(message.from_user.id) - int(message.text)
        if mts >= 0:
            transaction(message.from_user.id, user_name_to_id(user_to_send), int(message.text))
            bot.send_message(message.chat.id, 'Моржики в пути')
            bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAEEvG5igWmJfIm_wlBSPjMjWXFxg4vVwAACfhQAAvVtYElZ121GRfbP_CQE")
            bot.send_message(user_name_to_id(user_to_send), 'Вам пришло {}🦭 от {}🧇'.format(message.text, message.from_user.username))
            bot.send_sticker(user_name_to_id(user_to_send),"CAACAgIAAxkBAAEEvGBigWl3LQhfjn2j45nazFWqCYzmpwACBhQAAiNfAAFKfqNt14rwwKUkBA")
        else:
            bot.send_message(message.chat.id, 'Тебе не хватает {}🦭'.format(-mts))
        
    except Exception:
        bot.send_message(message.chat.id, 'Введи число')
        bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAEEvGhigWmCyN3fPPGRSUz5D2f06PXDAQAC9hgAArxzuEmjv6WqccYocCQE")
@bot.callback_query_handler(lambda query: query.data)
def call_back(data):
    try:
        id = data.data[1:]
        match data.data[0]:
            case 's':
                sent = bot.send_message(data.from_user.id, 'Что вы продаете?🛍')
                bot.register_next_step_handler(sent, get_sell_text)
            case '0':
                bot.delete_message(data.from_user.id,data.message.id)
                db.remove(q.id == id)
                bot.send_message(data.from_user.id, 'Успешно удалил обьявление📦❌')
            case 'b':
                can_buy_check = getuser(data.from_user.id) - get_sell_cost(id)
                if can_buy_check >= 0:
                    job_desc = db.search(q.id == id)
                    creator_tmp = db.search(q.id == id)
                    creator = db.search(q.username == creator_tmp[0]['creator'])
                    bot.delete_message(data.from_user.id,data.message.id)
                    transaction(data.from_user.id, creator[0]['userid'],get_sell_cost(id))
                    bot.send_message(data.from_user.id, 'Покупка успешна📦\nКод: {}🔑'.format(id))
                    bot.send_sticker(data.from_user.id,"CAACAgIAAxkBAAEEvHBigWmL70IzVrfxgwvqSf8yW3_e4gACdRoAAgb-aUnKEzbSS0rckSQE")
                    bot.send_message(creator[0]['userid'], 'У вас купили\n~~~~~~~~\n{}\n~~~~~~~~\nПокупатель: {}🥁\nКлюч: {}🔑'.format(job_desc[0]['text'],getuser(data.from_user.id, "username"), id))
                    db.remove(q.id == id)
                else:
                    bot.send_message(data.from_user.id, 'Вам нехватает {}🦭'.format(-can_buy_check))
    except Exception as e:
        print(e)
get_sell_text_var = ''
def get_sell_text(message):
    global get_sell_text_var
    get_sell_text_var = message.text
    sent = bot.send_message(message.chat.id, 'Укажите стоимость🛸')
    bot.register_next_step_handler(sent, get_sell_cost_hand)
def get_sell_cost_hand(message):
    global get_sell_text_var 
    try:
        if int(message.text) > 0:
            sell_id = sell(get_sell_text_var,getuser(message.from_user.id,"username"), int(message.text))
            bot.send_message(message.chat.id, 'Успешно🧉')
            my_sells = db.search(q.id == sell_id)
            mj_markup = types.InlineKeyboardMarkup()
            m1 = types.InlineKeyboardButton('❌Удалить', callback_data='0' + my_sells[0]['id'])
            mj_markup.add(m1)
            bot.send_message(message.chat.id, '{}\n———————————\nСтоимость🦭: {}'.format(my_sells[0]['text'], my_sells[0]['cost']), reply_markup=mj_markup)
        else:
            bot.send_message(message.chat.id,'Увы меньше нуля нульзя указывать цену🧯')
    except:
        sent = bot.send_message(message.from_user.id,'Введите число🔢')
        bot.register_next_step_handler(sent, get_sell_cost_hand)

bot.polling(True)


