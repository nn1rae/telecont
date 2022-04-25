from telebot import types
import random
import telebot
from tinydb import TinyDB, Query


db = TinyDB('db.json')
quv = Query()
def new_user(id):
    db.insert({'userid': id, 'prom': 0})
def getdb(id,arg2 = 1):
    get0 = db.search(quv.userid == id)
    new_get = get0[0]
    if arg2 == 0:
        return new_get['userid']
    else :
        return new_get['prom']

bot = telebot.TeleBot('5311428361:AAHmz1afEFRPBjN6fSHeARvarmyeNzsWIOA')


@bot.message_handler(commands=['start'])
def start(messege):
    user_id = messege.from_user.id
    try:
        getdb(user_id,0)
        bot.send_message(messege.chat.id, f'Hello {messege.from_user.username}, wellcome back 😄, currently you have |{getdb(user_id)}| promo ')
    except:
        new_user(user_id)
        bot.send_message(messege.chat.id, f'Hello {messege.from_user.username}, ?how you doing¿')
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('🔰my prom🔰')
    itembtn2 = types.KeyboardButton('play♿️')
    markup.add(itembtn1, itembtn2)



@bot.message_handler(content_types=['text'])   
def text_input(messege):
    if messege.text == '🔰my prom🔰':
        bot.send_message(messege.chat.id, f'currently you have |{getdb(messege.from_user.id)}| promo')
    elif messege.text == 'play♿️':
        bot.send_message(messege.chat.id,'not yet')
   
    
bot.polling(none_stop=True)