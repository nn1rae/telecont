from hashlib import new
import random
import telebot
from tinydb import TinyDB, Query

db = TinyDB('db.json')

def new_user(id):
    db.insert({'userid': id, 'prom': 0})

quv = Query()

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


     

     
    # bot.send_message(messege.chat.id, str(getdb(user_id)))



@bot.message_handler(content_types=['text'])   
def text_input(messege):
    bot.send_message(messege.chat.id, '1')

   
    
bot.polling(none_stop=True)