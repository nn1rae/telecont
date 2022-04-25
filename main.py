from telebot import types
import random
import telebot
from tinydb import TinyDB, Query


db = TinyDB('db.json')
quv = Query()
def new_user(id):
    db.insert({'userid': id, 'prom': 0, 'wait': False})
def getdb(id,arg2 = 1):
    get0 = db.search(quv.userid == id)
    new_get = get0[0]
    if arg2 == 0:
        return new_get['userid']
    elif arg2 == 1 :
        return new_get['prom']
    elif arg2 == 2 :
        return new_get['wait']


bot = telebot.TeleBot('5311428361:AAHmz1afEFRPBjN6fSHeARvarmyeNzsWIOA')

#admin pannel
@bot.message_handler(commands=['adm'])
def adm(messege):
    if messege.from_user.id == 999711677:
        
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(row_width=2)
        admitem1 = types.KeyboardButton('👛new code👛')
        admitem2 = types.KeyboardButton('📃all codes📃')
        markup.add(admitem1, admitem2)
        bot.send_message(messege.chat.id,'Your choise, my lord', reply_markup=markup)
    else:
        bot.send_message(messege.chat.id,'You are not alowed to use that')


@bot.message_handler(commands=['start'])
def start(messege):
    user_id = messege.from_user.id
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('🔰my prom🔰')
    itembtn2 = types.KeyboardButton('play')
    markup.add(itembtn1, itembtn2)
    try:
        getdb(user_id,0)
        bot.send_message(messege.chat.id, f'Hello {messege.from_user.username}, wellcome back 😄, currently you have |{getdb(user_id)}| promo ', reply_markup=markup)
    except:
        new_user(user_id)
        bot.send_message(messege.chat.id, f'Hello {messege.from_user.username}, ?how you doing¿',reply_markup=markup)

@bot.poll_answer_handler()


@bot.message_handler(content_types=['text'])   
def text_input(messege):
    if getdb(messege.from_user.id,2) == True:
            rend = random.randrange(0,2)
            if int(messege.text)== rend:
                bot.send_message(messege.chat.id,'cool')
            db.update({'wait': False}, quv.userid == messege.from_user.id)
            markup = types.ReplyKeyboardMarkup(row_width=2)
            itembtn1 = types.KeyboardButton('🔰my prom🔰')
            itembtn2 = types.KeyboardButton('play')
            markup.add(itembtn1, itembtn2)
            bot.send_message(messege.chat.id,'nice',reply_markup=markup)


    
    elif messege.text == '🔰my prom🔰':
        bot.send_message(messege.chat.id, f'currently you have |{getdb(messege.from_user.id)}| promo')
    elif messege.text == 'play':
        if getdb(messege.from_user.id) > 0 :
            markup_pl = types.ReplyKeyboardMarkup()
            itembtn_pl = types.KeyboardButton('0')
            itembtn_pl1 = types.KeyboardButton('1')
            markup_pl.add(itembtn_pl1, itembtn_pl)
            bot.send_message(messege.chat.id,'0 or 1?',reply_markup=markup_pl)
            tmp_prom = getdb(messege.from_user.id) - 1
            db.update({'prom': tmp_prom, 'wait': True}, quv.userid == messege.from_user.id)
            
            
        
        
    elif messege.from_user.id == 999711677:
        if messege.text == '👛new code👛':
            bot.send_message(messege.chat.id, 'soon')
        elif messege.text == '📃all codes📃':
            bot.send_message(messege.chat.id,'soon')
    else:
        bot.send_message(messege.chat.id,'I dont understand🦭')

    

bot.polling(none_stop=True)