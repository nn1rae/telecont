from secrets import choice
from telebot import types
import random
import telebot
from tinydb import TinyDB, Query
import os
import string


db = TinyDB('db.json')
quv = Query()
def new_user(id,username='none'):
    db.insert({'userid': id, 'prom': 0, 'wait': False, 'mon': 0, 'username': username})
def getdb(id,arg2 = 1):
    get0 = db.search(quv.userid == id)
    new_get = get0[0]
    if arg2 == 0:
        return new_get['userid']
    elif arg2 == 1 :
        return new_get['prom']
    elif arg2 == 2 :
        return new_get['wait']
    elif arg2 == 3 :
        return new_get['mon']
    elif arg2 == 4 :
        return new_get['username']

def del_mon(id,num):
    db.update({'mon': getdb(id, 3) - num}, quv.userid == id)
    
def new_code():
    prom_temp = ''
    alfab = string.ascii_uppercase + string.digits
    for i in range(5):
        prom_temp += random.choice(alfab)
    return prom_temp 
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
        admitem4 = types.KeyboardButton('💳🔨DEL mon')
        markup.add(admitem1, admitem2, admitem3, admitem4)
        bot.send_message(messege.chat.id,'Your choise, my lord', reply_markup=markup)
    else:
        bot.send_message(messege.chat.id,'You are not alowed to use that')

#start
@bot.message_handler(commands=['start'])
def start(messege):
    user_id = messege.from_user.id
    username = messege.from_user.username
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('🔰my prom🔰')
    itembtn2 = types.KeyboardButton('play')
    markup.add(itembtn1, itembtn2)
    try:
        
        bot.send_message(messege.chat.id, f'Hello {messege.from_user.username}, wellcome back 😄, currently you have |{getdb(user_id)}| promo ', reply_markup=markup)
    except:
        new_user(user_id, username)
        bot.send_message(messege.chat.id, f'Hello {messege.from_user.username}, ?how you doing¿',reply_markup=markup)
@bot.message_handler(commands=['menu'])
def menu(messege):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('🔰my prom🔰')
    itembtn2 = types.KeyboardButton('play')
    itembtn3 = types.KeyboardButton('my ballance 🍾')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(messege.chat.id,'Menu:',reply_markup=markup)



#text handler
@bot.message_handler(content_types=['text'])   
def text_input(messege):
    with open('promos.txt', 'r') as promos:
        check_prom_tmp = promos.read()

    if getdb(messege.from_user.id,2) == True:
            markup = types.ReplyKeyboardMarkup(row_width=2)
            itembtn1 = types.KeyboardButton('🔰my prom🔰')
            itembtn2 = types.KeyboardButton('play')
            itembtn3 = types.KeyboardButton('my ballance 🍾')
            markup.add(itembtn1, itembtn2, itembtn3)
            rend_cal = {'🥎': 0, '⚾️': 1}
            rend = random.randrange(0,2)
            if rend_cal[messege.text] == rend:
                bot.send_message(messege.chat.id,'Congrats, +1 to youre ballance🥂',reply_markup=markup)
                db.update({'mon': getdb(messege.from_user.id, 3) + 1}, quv.userid == messege.from_user.id)
            else:
                bot.send_message(messege.chat.id,'Not youre day I gess',reply_markup=markup)

            db.update({'wait': False}, quv.userid == messege.from_user.id)
        
    elif messege.text in check_prom_tmp and len(messege.text) == 5:
        new_prom = check_prom_tmp.replace(messege.text, '')
        db.update({'prom': getdb(messege.from_user.id) + 1}, quv.userid == messege.from_user.id)
        with open('promos.txt', 'w') as new_prom_list:
            new_prom_list.write(new_prom)
        bot.send_message(messege.chat.id,'+1 to your proms🍬')    
    elif messege.text == '🔰my prom🔰':
        bot.send_message(messege.chat.id, f'currently you have |{getdb(messege.from_user.id)}| promo')
    elif messege.text == 'play':
        if getdb(messege.from_user.id) > 0 :
            markup_pl = types.ReplyKeyboardMarkup()
            itembtn_pl = types.KeyboardButton('⚾️')
            itembtn_pl1 = types.KeyboardButton('🥎')
            markup_pl.add(itembtn_pl1, itembtn_pl)
            bot.send_message(messege.chat.id,'⚾️ or 🥎?',reply_markup=markup_pl)
            tmp_prom = getdb(messege.from_user.id) - 1
            db.update({'prom': tmp_prom, 'wait': True}, quv.userid == messege.from_user.id)
        else:
            bot.send_message(messege.chat.id,'Sorry, you have 0 prom')

    elif messege.text == 'my ballance 🍾':
        bot.send_message(messege.chat.id, f'Youre corrent balance is {getdb(messege.from_user.id, 3)}')
            
    
    
    elif messege.from_user.id == 999711677:
        with open('tmp_del', 'r') as del_check:
            del_check = int(del_check.read())
        if del_check == 1:
            with open('tmp_user_del', 'w') as tmp_user_del:
                tmp_user_del.write(messege.text)
                with open('tmp_del','w') as del_write:
                    del_write.write('2')
                bot.send_message(messege.chat.id, 'How much wuld you like to take?🙃')
        elif del_check == 2:
            with open('tmp_user_del', 'a') as tmp_user_del:
                tmp_user_del.write('\n' + messege.text)
                with open('tmp_del','w') as del_write:
                    del_write.write('0')
            with open('tmp_user_del','r')as tmp_user_del:
                del_list = list(tmp_user_del.read().split('\n'))
            try:
                del_mon(int(del_list[0]),int(del_list[1]))
                bot.send_message(messege.chat.id,f'just took {del_list[1]} from {del_list[0]}🍜🍜')

            except:
                bot.send_message(messege.chat.id,'Error wille deleting👻')
        if messege.text == '👛new code👛':
            ncode = new_code()
            with open('promos.txt', 'a') as promos:
                promos.write('\n' + ncode)
            with open('promos.txt', 'rb') as promos:
                bot.send_message(messege.chat.id, f'Code.{ncode} just ganereted')
        
        elif messege.text == '📃all codes📃':
            with open('promos.txt', 'rb') as promosr:
                try:
                    bot.send_message(messege.chat.id,promosr.read())
                except:
                    bot.send_message(messege.chat.id,'no codes left')

        elif messege.text == '🧁List🧁':
            tmp_list = db.all()
            for i in range(len(tmp_list)):
                temp_ran = tmp_list[i]
                with open('tmp_list.txt', 'a') as ttmp:
                    user = temp_ran['userid']
                    mon = temp_ran['mon']
                    prom = temp_ran['prom']
                    username = temp_ran['username']
                    ttmp.write(f'\nid. {user} |username. {username}| mon. {mon} |prom. {prom} ')
            with open('tmp_list.txt', 'rb') as last_use_tmlist:
                bot.send_message(messege.chat.id,last_use_tmlist.read())
                os.remove("tmp_list.txt")
        elif messege.text == '💳🔨DEL mon':
            with open('tmp_del', 'w') as tmp_del:
                tmp_del.write('1')
            bot.send_message(messege.chat.id,'return ID')
    else:
        bot.send_message(messege.chat.id,'I dont understand🦭')
    

bot.polling(none_stop=True)