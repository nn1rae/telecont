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

def del_mon(id: int,num):
    db.update({'mon': getdb(id, 3) - num}, quv.userid == id)
def add_mon(id,num):
    db.update({'mon': getdb(id, 3) + num}, quv.userid == id)
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
        admitem1 = types.KeyboardButton('👛Новый код👛')
        admitem2 = types.KeyboardButton('📃Показать все коды📃')
        admitem3 = types.KeyboardButton('🧁Информация о пользователях🧁')
        admitem4 = types.KeyboardButton('💳🔨Изъять монеты')
        admitem5 = types.KeyboardButton('📥💵Добавить монеты')
        admitem6 = types.KeyboardButton('📨Отправить сообщение')
        markup.add(admitem1, admitem2, admitem3, admitem4, admitem5, admitem6)
        bot.send_message(messege.chat.id,'⚗️Что мне делать🪬', reply_markup=markup)
    else:
        bot.send_message(messege.chat.id,'Вам нельзя пользоваться этой функцией🔐')

#start
@bot.message_handler(commands=['start'])
def start(messege):
    user_id = messege.from_user.id
    username = messege.from_user.username
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('🚧Кол-во моих попыток')
    itembtn2 = types.KeyboardButton('Попытать удачу🎢')
    markup.add(itembtn1, itembtn2)
    try:
        
        bot.send_message(messege.chat.id, f'Добро пожаловать обратно {messege.from_user.username} 🖇,на текущий момент у вас {getdb(user_id)} попыток', reply_markup=markup)
    except:
        new_user(user_id, username)
        bot.send_message(messege.chat.id, f'Здравствуй {messege.from_user.username}, и добро пожаловать.',reply_markup=markup)
@bot.message_handler(commands=['menu'])
def menu(messege):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('🚧Кол-во моих попыток')
    itembtn2 = types.KeyboardButton('Попытать удачу🎢')
    itembtn3 = types.KeyboardButton('Кол-во моих монет🏦')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(messege.chat.id,'Чего хочешь:',reply_markup=markup)



#text handler
@bot.message_handler(content_types=['text'])   
def text_input(messege):
    print(str(messege.text) + ' |  from ' + str(messege.from_user.username))
    with open('promos.txt', 'r') as promos:
        check_prom_tmp = promos.read()

    if getdb(messege.from_user.id,2) == True:
            markup = types.ReplyKeyboardMarkup(row_width=2)
            itembtn1 = types.KeyboardButton('🚧Кол-во моих попыток')
            itembtn2 = types.KeyboardButton('Попытать удачу🎢')
            itembtn3 = types.KeyboardButton('Кол-во моих монет🏦')
            markup.add(itembtn1, itembtn2, itembtn3)
            rend_cal = {'🥎': 0, '⚾️': 1}
            rend = random.randrange(0,2)
            try:
                if rend_cal[messege.text] == rend:
                    bot.send_message(messege.chat.id,'Кросс, добавляю +1 к твоему текущему балансу🥂',reply_markup=markup)
                    db.update({'mon': getdb(messege.from_user.id, 3) + 1}, quv.userid == messege.from_user.id)
                else:
                    rand_ans = random.randint(0,4)
                    if rand_ans >= 0 and rand_ans < 4:
                        bot.send_message(messege.chat.id,'Если коротко, то ты проиграл',reply_markup=markup)
                    else:
                        bot.send_message(messege.chat.id,'Ну что я могу тебе сказать, ты лох',reply_markup=markup)
                db.update({'wait': False}, quv.userid == messege.from_user.id)
            except:
                markup_ppl = types.ReplyKeyboardMarkup()
                itembtn_ppl = types.KeyboardButton('⚾️')
                itembtn_ppl1 = types.KeyboardButton('🥎')
                markup_ppl.add(itembtn_ppl1, itembtn_ppl)
                bot.send_message(messege.chat.id, 'Пж выбери мячик и не пиши мне пургу', reply_markup=markup_ppl)
        
    elif messege.text in check_prom_tmp and len(messege.text) == 5:
        new_prom = check_prom_tmp.replace(messege.text, '')
        db.update({'prom': getdb(messege.from_user.id) + 1}, quv.userid == messege.from_user.id)
        with open('promos.txt', 'w') as new_prom_list:
            new_prom_list.write(new_prom)
        rand_ans = random.randint(0,4)
        if rand_ans >= 0 and rand_ans < 4:
            bot.send_message(messege.chat.id,'Код заюзан, +1 к твоим попыткам🎫')
        else:
            bot.send_message(messege.chat.id,'+1 к твоим несчастным попыткам выиграть, вот медалька за старание🥉')
    elif messege.text == '🚧Кол-во моих попыток':
        bot.send_message(messege.chat.id, f'В данный момент у тебя {getdb(messege.from_user.id)} попыток')
    elif messege.text == 'Попытать удачу🎢':
        if getdb(messege.from_user.id) > 0 :
            markup_pl = types.ReplyKeyboardMarkup()
            itembtn_pl = types.KeyboardButton('⚾️')
            itembtn_pl1 = types.KeyboardButton('🥎')
            markup_pl.add(itembtn_pl1, itembtn_pl)
            bot.send_message(messege.chat.id,'⚾️ Или 🥎?',reply_markup=markup_pl)
            tmp_prom = getdb(messege.from_user.id) - 1
            db.update({'prom': tmp_prom, 'wait': True}, quv.userid == messege.from_user.id)
        else:
            bot.send_message(messege.chat.id,'Свалил/а, у тебя 0 попыток')

    elif messege.text == 'Кол-во моих монет🏦':
        #bot.send_message(messege.chat.id, f'У тебя {getdb(messege.from_user.id, 3)} монет')
        rand_ans = random.randint(0,4)
        if rand_ans >= 0 and rand_ans < 3:
            bot.send_message(messege.chat.id,f'У тебя {getdb(messege.from_user.id, 3)} монет.')
        elif rand_ans == 3:
            bot.send_message(messege.chat.id,f'У тебя {getdb(messege.from_user.id, 3)} монет, ну ты и бомж конечно.')
        else:
            bot.send_message(messege.chat.id,f'У тебя {getdb(messege.from_user.id, 3)} монет, ШИКУЕМ 🥁🎉🎉.')
            
    #admin pan inside
    elif messege.from_user.id == 999711677:
        with open('tmp_del', 'r') as del_check:
            del_check = int(del_check.read())
        if del_check == 1:
            with open('tmp_user_del', 'w') as tmp_user_del:
                tmp_user_del.write(messege.text)
                with open('tmp_del','w') as del_write:
                    del_write.write('2')
                bot.send_message(messege.chat.id, 'Сколько монет изъять??🙃')
        elif del_check == 2:
            with open('tmp_user_del', 'a') as tmp_user_del:
                tmp_user_del.write('\n' + messege.text)
                with open('tmp_del','w') as del_write:
                    del_write.write('0')
            with open('tmp_user_del','r')as tmp_user_del:
                del_list = list(tmp_user_del.read().split('\n'))
            try:
                del_mon(int(del_list[0]),int(del_list[1]))
                tem_user_var = getdb(int(del_list[0]), 4)
                how_much_has = getdb(int(del_list[0]), 3)
                bot.send_message(messege.chat.id,f'Только что изъял {del_list[1]} от {tem_user_var}🍜🍜, теперь у него/нее на счету монет {how_much_has}')

            except:
                bot.send_message(messege.chat.id,'Ошибонька при изъятии 🤯')
        
        with open('tmp_add', 'r') as del_check:
            del_check = int(del_check.read())
        if del_check == 1:
            with open('tmp_user_add', 'w') as tmp_user_del:
                tmp_user_del.write(messege.text)
                with open('tmp_add','w') as del_write:
                    del_write.write('2')
                bot.send_message(messege.chat.id, 'Скок добавить?🤔')
        elif del_check == 2:
            with open('tmp_user_add', 'a') as tmp_user_del:
                tmp_user_del.write('\n' + messege.text)
                with open('tmp_add','w') as del_write:
                    del_write.write('0')
            with open('tmp_user_add','r')as tmp_user_del:
                del_list = list(tmp_user_del.read().split('\n'))
            try:
                add_mon(int(del_list[0]),int(del_list[1]))
                tem_user_var = getdb(int(del_list[0]), 4)
                how_much_has = getdb(int(del_list[0]), 3)
                bot.send_message(messege.chat.id,f'Только что добавил {del_list[1]} к балансу {tem_user_var}🥱, теперь у него/нее на счету монет {how_much_has}.')

            except:
                bot.send_message(messege.chat.id,'Ошибонька при добавлении 🫢')
        
        with open('tmp_send', 'r') as del_check:
            del_check = int(del_check.read())
        if del_check == 1:
            with open('tmp_user_send', 'w') as tmp_user_del:
                tmp_user_del.write(messege.text)
            with open('tmp_send','w') as del_write:  #posib error
                    del_write.write('2')
            with open('tmp_user_send', 'r') as tmp_user_del:
                user_id_send_for_db = tmp_user_del.read()
            try:
                bot.send_message(messege.chat.id, 'Что отправить {}?🛍'.format(getdb(int(user_id_send_for_db),4)))
            except:
                bot.send_message(messege.chat.id,'Ошибонька при отправлении📭')
                with open('tmp_send','w') as del_write:
                    del_write.write('0')
        elif del_check == 2:
            with open('tmp_user_send', 'a') as tmp_user_del:
                tmp_user_del.write('\n' + messege.text)
                with open('tmp_send','w') as del_write:
                    del_write.write('0')
            with open('tmp_user_send','r')as tmp_user_del:
                del_list = list(tmp_user_del.read().split('\n'))
            try:
                tem_user_var = getdb(int(del_list[0]), 4)
                bot.send_message(int(del_list[0]), str(del_list[1]))
                bot.send_message(messege.chat.id, 'Только что отправил # {} # кому: {} 📬'.format(del_list[1], tem_user_var))

            except:
                bot.send_message(messege.chat.id,'Ошибонька при отправлении📭')
        

        if messege.text == '👛Новый код👛':
            ncode = new_code()
            with open('promos.txt', 'a') as promos:
                promos.write('\n' + ncode)
            with open('promos.txt', 'rb') as promos:
                bot.send_message(messege.chat.id, f'Только что сгенерировал {ncode} ') 
        elif messege.text == '📃Показать все коды📃':
            with open('promos.txt', 'rb') as promosr:
                try:
                    bot.send_message(messege.chat.id,promosr.read())
                except:
                    bot.send_message(messege.chat.id,'Все коды украл валера')
        elif messege.text == '🧁Информация о пользователях🧁':
            tmp_list = db.all()
            for i in range(len(tmp_list)):
                temp_ran = tmp_list[i]
                with open('tmp_list.txt', 'a') as ttmp:
                    user = temp_ran['userid']
                    mon = temp_ran['mon']
                    prom = temp_ran['prom']
                    username = temp_ran['username']
                    ttmp.write(f'\nИдшка.  {user} Нейм.  {username} Монетки.  {mon} Попытки.  {prom}')
            with open('tmp_list.txt', 'rb') as last_use_tmlist:
                bot.send_message(messege.chat.id,last_use_tmlist.read())
                os.remove("tmp_list.txt")
        elif messege.text == '💳🔨Изъять монеты':
            with open('tmp_del', 'w') as tmp_del:
                tmp_del.write('1')
            bot.send_message(messege.chat.id,'Кинь idшку')
        elif messege.text == '📥💵Добавить монеты':
            with open('tmp_add', 'w') as tmp_del:
                tmp_del.write('1')
                bot.send_message(messege.chat.id,'Кинь idшку')
        elif messege.text == '📨Отправить сообщение':
            with open('tmp_send', 'w') as tmp_del:
                tmp_del.write('1')
                bot.send_message(messege.chat.id,'Кинь idшку')
    else:
        rand_ans = random.randint(0,3)
        if rand_ans == 0:
            bot.send_message(messege.chat.id,'Не пон че ты шпрехаеш')
        elif rand_ans == 1:
            bot.send_message(messege.chat.id,'Я тебя не понимать блин')
        elif rand_ans == 2:
            bot.send_message(messege.chat.id,'Нефига не понял, Миша давай все по новой')
        elif rand_ans == 3:
            bot.send_message(messege.chat.id,'Мой русский не понимать твоего язык')
            
        
    

bot.polling(none_stop=True)