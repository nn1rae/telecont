
from hashlib import new
import random
import telebot
from tinydb import TinyDB, Query

db = TinyDB('db.json')

def new_user(id):
    db.insert({'userid': id, 'prom': 0})

quv = Query()

def getdb(id,arg2 = 1):
    return db.search(quv.userid == id)
    # if arg2 == 0:
    #     return new_get['userid']
    # else :
    #     return new_get['much']



bot = telebot.TeleBot('5311428361:AAHmz1afEFRPBjN6fSHeARvarmyeNzsWIOA')

print(str(getdb(999711677)))

@bot.message_handler(commands=['start'])
def start(messege):
     user_id = messege.from_user.id
     new_user(user_id)

     
    # bot.send_message(messege.chat.id, str(getdb(user_id)))



@bot.message_handler(content_types=['text'])   
def text_input(messege):
    bot.send_message(messege.chat.id, '1')

   
    
bot.polling(none_stop=True)