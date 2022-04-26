from telebot import types
import random
import telebot
from tinydb import TinyDB, Query
import os


db = TinyDB('db.json')
quv = Query()
def new_user(id):
    db.insert({'userid': id, 'prom': 0, 'wait': False, 'mon': 0})
def getdb(id,arg2 = 1):
    get0 = db.search(quv.userid == id)
    try:
        new_get = get0[0]
        if arg2 == 0:
            return new_get['userid']
        elif arg2 == 1 :
            return new_get['prom']
        elif arg2 == 2 :
            return new_get['wait']
        elif arg2 == 3 :
            return new_get['mon']
    except:
        return False
bot = telebot.TeleBot('5311428361:AAHmz1afEFRPBjN6fSHeARvarmyeNzsWIOA')

#admin pannel
@bot.message_handler(commands=['adm'])
def adm(messege):
    if messege.from_user.id == 999711677:
        
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(row_width=2)
        admitem1 = types.KeyboardButton('👛new code👛')
        admitem2 = types.KeyboardButton('📃all codes📃')
        admitem3 = types.KeyboardButton('🧁List🧁')
        markup.add(admitem1, admitem2, admitem3)
        bot.send_message(messege.chat.id,'Your choise, my lord', reply_markup=markup)
    else:
        bot.send_message(messege.chat.id,'You are not alowed to use that')

#start
@bot.message_handler(commands=['start'])
def start(messege):
    user_id = messege.from_user.id
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('🔰my prom🔰')
    itembtn2 = types.KeyboardButton('play')
    markup.add(itembtn1, itembtn2)
    if getdb(user_id) != False:
        
        bot.send_message(messege.chat.id, f'Hello {messege.from_user.username}, wellcome back 😄, currently you have |{getdb(user_id)}| promo ', reply_markup=markup)
    else:
        new_user(user_id)
        bot.send_message(messege.chat.id, f'Hello {messege.from_user.username}, ?how you doing¿',reply_markup=markup)

#text handler
@bot.message_handler(content_types=['text'])   
def text_input(messege):
    if getdb(messege.from_user.id,2) == True:
            markup = types.ReplyKeyboardMarkup(row_width=2)
            itembtn1 = types.KeyboardButton('🔰my prom🔰')
            itembtn2 = types.KeyboardButton('play')
            itembtn3 = types.KeyboardButton('my ballance 🍾')
            markup.add(itembtn1, itembtn2, itembtn3)
            
            rend = random.randrange(0,2)
            if int(messege.text)== rend:
                bot.send_message(messege.chat.id,'Congrats, +1 to youre ballance🥂',reply_markup=markup)
                db.update({'mon': getdb(messege.from_user.id, 3) + 1}, quv.userid == messege.from_user.id)
            else:
                bot.send_message(messege.chat.id,'Not youre day I gess',reply_markup=markup)

            db.update({'wait': False}, quv.userid == messege.from_user.id)
            
            


    
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
        else:
            bot.send_message(messege.chat.id,'Sorry, you have 0 prom')

    elif messege.text == 'my ballance 🍾':
        bot.send_message(messege.chat.id, f'Youre corrent balance is {getdb(messege.from_user.id, 3)}')
            
    
    
    elif messege.from_user.id == 999711677:
        if messege.text == '👛new code👛':
            bot.send_message(messege.chat.id, 'soon')
        
        
        elif messege.text == '📃all codes📃':
            bot.send_message(messege.chat.id,'soon')
        
        
        elif messege.text == '🧁List🧁':
            tmp_list = db.all()
            for i in range(len(tmp_list)):
                temp_ran = tmp_list[i]
                with open('tmp_list.txt', 'a') as ttmp:
                    user = temp_ran['userid']
                    mon = temp_ran['mon']
                    prom = temp_ran['prom']
                    ttmp.write(f'\nid. {user} | mon. {mon} |prom. {prom} ')
            with open('tmp_list.txt', 'rb') as last_use_tmlist:
                bot.send_message(messege.chat.id,last_use_tmlist.read())
                os.remove("tmp_list.txt")


    
    else:
        bot.send_message(messege.chat.id,'I dont understand🦭')

    

bot.polling(none_stop=True)