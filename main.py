import code
from curses.ascii import isdigit
import time
from telebot import types
import random
import telebot
from tinydb import TinyDB, Query
import os
import string

bot = telebot.TeleBot('5311428361:AAHmz1afEFRPBjN6fSHeARvarmyeNzsWIOA')

db = TinyDB('db.json')
quv = Query()

def new_user(id,username='none'):
    db.insert({'userid': id, 'prom': 0, 'wait': False, 'mon': 0, 'username': username,'next_win': False, 'type': 'user'})
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
def get_code_much(code):
    code_l = db.search(quv.code == code)
    return int(code_l[0]['much'])

def del_code(code):
    db.remove(quv.code == code)
def check_code(code):
    check_l = db.search(quv.code == code)
    if not check_l:
        return False
    else:
        return True
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
def next_win(id,ans):
    if ans == 1:
        db.update({'next_win': True}, quv.userid == id)
    elif ans == 0:
        db.update({'next_win': False}, quv.userid == id)

def next_win_check(id:int):
    list = db.search(quv.userid == id)
    if not list:
        return False
    elif list[0]['next_win'] == True :
        return True
#shity responsez
@bot.message_handler(func=lambda messege: True ,content_types=["sticker"]) 
def stiker(messege):
    sticker_ans = ['Офигел/а чи шо?','Нафиг ты мне свои стикеры кидаешь а?', 'Жалко твоих родителей….', 'Фактиш', 'Гвоздь мне в кеды', 'Император тобой не доволен', 'Имератор забрать твоя жена за такое', 'Ульяна, вы?🧐']
    bot.reply_to(messege, random.choice(sticker_ans))

@bot.message_handler(func=lambda messege: True ,content_types=["photo"])
def stiker(messege):
    photo_ans = ['Ладно', '🤨📸', 'За такое в некоторых странах сажают...', 'Это не план захвата Польши.', 'План захвата Польши?!?!?!', 'Пожалуй это я сохраню']
    bot.reply_to(messege, random.choice(photo_ans))

@bot.message_handler(func=lambda messege: True ,content_types=["voice", "audio"])
def stiker(messege):
    audio_ans = ['Ну ок и что?', 'Что за стоны','Ты там не разборчиво говоришь да и мне пофиг', 'Зачем мне по твоему это?', 'Хз']
    bot.reply_to(messege, random.choice(audio_ans))

@bot.message_handler(func=lambda messege: True ,content_types=["video"])
def stiker(messege):
    video_ans = ['Я планирую польшу захватывать, это мне не поможет.', 'Илон маск покупает это видео', 'Ничего гениальнее я ещё не видел', '🦽?', 'Если бы я был живим то вызвал бы копов👨‍🦯']
    bot.reply_to(messege, random.choice(video_ans))

@bot.message_handler(func=lambda messege: True ,content_types=["animation"]) 
def stiker(messege):
    animation_ans = ['Не грузит, это что-то важное?', 'У-у-у-у-у 🐒', 'Эмз, потому что только у нее есть телефон', '🙋‍♂️', 'Ульяна, вы?🧐']
    bot.reply_to(messege, random.choice(animation_ans))
@bot.message_handler(commands=['kill_codes'])
def kill_codes(messege):
    if messege.from_user.id == 999711677:
        much_codes_remove = len(db.search(quv.type == 'code'))
        db.remove(quv.type == 'code')
        bot.send_message(messege.chat.id, f'Удачно удалил {much_codes_remove} кодов')

@bot.message_handler(commands=['next_win'])
def next_win_hand(messege):
    if messege.from_user.id == 999711677:
        sent = bot.send_message(messege.chat.id, 'id')
        bot.register_next_step_handler(sent, next_win_get)
def next_win_get(messege):
    try:
        next_win(int(messege.text), 1)
        bot.send_message(messege.chat.id, 'Успешно по отношению к {}'.format(getdb(int(messege.text),4)))
    except Exception as e:
        bot.send_message(messege.chat.id, e)

@bot.message_handler(commands=['check_prom'])
def check_prom(messege):
    sent = bot.send_message(messege.chat.id, 'Введи промокод')
    bot.register_next_step_handler(sent, check_prom_hand)

def check_prom_hand(messege):
    prom_list = db.search(quv.code == messege.text)
    if not prom_list:
        bot.send_message(messege.chat.id, 'Промокод не найден')
    else:
        bot.send_message(messege.chat.id, 'Этот промокод на {} попыток'.format(prom_list[0]['much']))
@bot.message_handler(commands=['la'])
def la(messege):
    mes = "/kill_codes - Удалить все коды \n/next_win - В след раз игрок точно выиграет"
    if messege.from_user.id == 999711677:
        bot.send_message(messege.chat.id,mes)

@bot.message_handler(commands=['play'])
def play(messege):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton('🎯')
    markup.add(item1)
    bot.send_message(messege.chat.id, """
    *Отправь смайлик чтоб начать игру*\n
    🎯 - Шанс выиграть 1 к 3 *Выигрыш От 1 до 3 монет*
    🎲 - Шанс выиграть 1 к 6 *Выигрыш 6 монет*
    """
    , parse_mode= 'Markdown') #, reply_markup=markup)

#dice games
@bot.message_handler(content_types=['dice'])
def dice(messege):
    if messege.forward_from:
        no_forward =  ['Думал(а) самый умный(ая) а?', 'Так нельзя делать']
        bot.send_message(messege.chat.id, random.choice(no_forward))
    elif getdb(messege.chat.id) == 0:
        bot.send_message(messege.chat.id,'Нельзя играть когда у тебя *0* попыток',parse_mode='Markdown')
    else:
        no_win_mes = ['Увы ты проиграл а промик ушел в небытие', 'Проигрыш', 'Попробуй в другой раз', 'Не сегодня', 'Можешь считать что промик потрачен в пустую', 'Повезет в другой раз']
        print(str(messege.dice) + 'from ' + str(getdb(messege.from_user.id, 4)))
        if messege.dice.emoji == '🎯':
            time.sleep(2.36)
            if messege.dice.value == 6 or next_win_check(messege.from_user.id):
                db.update({'mon': getdb(messege.from_user.id, 3) + 3, 'prom': getdb(messege.from_user.id) - 1}, quv.userid == messege.from_user.id)
                next_win(messege.from_user.id, 0)
                bot.send_message(messege.chat.id, 'ты выиграл 3 монеты, теперь у тебя *{}* монет'.format(getdb(messege.from_user.id,3)),parse_mode='Markdown')
            elif messege.dice.value == 5:
                db.update({'mon': getdb(messege.from_user.id, 3) + 1, 'prom': getdb(messege.from_user.id) - 1}, quv.userid == messege.from_user.id)
                bot.send_message(messege.chat.id, 'ты выиграл 1 монетy, теперь у тебя *{}* монет'.format(getdb(messege.from_user.id,3)),parse_mode='Markdown')
            else:
                db.update({'prom': getdb(messege.from_user.id) - 1}, quv.userid == messege.from_user.id)
                bot.send_message(messege.chat.id, random.choice(no_win_mes))
        elif messege.dice.emoji == '🎲':
            time.sleep(3)
            if messege.dice.value == 1 or next_win_check(messege.from_user.id):
                db.update({'mon': getdb(messege.from_user.id, 3) + 6, 'prom': getdb(messege.from_user.id) - 1}, quv.userid == messege.from_user.id)
                next_win(messege.from_user.id, 0)
                bot.send_message(messege.chat.id, 'ты выиграл 6 монет, теперь у тебя *{}* монет'.format(getdb(messege.from_user.id,3)),parse_mode='Markdown')
            else:
                db.update({'prom': getdb(messege.from_user.id) - 1}, quv.userid == messege.from_user.id)
                bot.send_message(messege.chat.id, random.choice(no_win_mes))
        else:
            bot.send_message(messege.chat.id, 'Эта игра пока что не поддерживается')
@bot.message_handler(commands=['info'])
def info(messege):
    mes = """
    *Информация по боту*
    Бот создан на языке Python3
    Просто по рофлу 
    *____________________________*
    Версия *0.2*
    
    Создатель *Klesberg*
    """
    bot.send_message(messege.chat.id,mes,parse_mode= 'Markdown')
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
    itembtn4 = types.KeyboardButton('Монеты в попытки🪤')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(messege.chat.id,'Чего хочешь:',reply_markup=markup)



#text handler
@bot.message_handler(content_types=['text'])   
def text_input(messege):
    print(str(messege.text) + ' |  from ' + str(messege.from_user.username))
    if getdb(messege.from_user.id,2) == True:
            markup = types.ReplyKeyboardMarkup(row_width=2)
            itembtn1 = types.KeyboardButton('🚧Кол-во моих попыток')
            itembtn2 = types.KeyboardButton('Попытать удачу🎢')
            itembtn3 = types.KeyboardButton('Кол-во моих монет🏦')
            itembtn4 = types.KeyboardButton('Монеты в попытки🪤')
            markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
            rend_cal = {'🥎': 0, '⚾️': 1}
            rend = random.randrange(0,2)
            try:
                db.update({'wait': False}, quv.userid == messege.from_user.id)
                if rend_cal[messege.text] == rend or next_win_check(messege.from_user.id):
                    db.update({'mon': getdb(messege.from_user.id, 3) + 1}, quv.userid == messege.from_user.id)
                    next_win(messege.from_user.id, 0)
                    bot.send_message(messege.chat.id,'Кросс, добавляю +1 к твоему текущему балансу🥂',reply_markup=markup)
                else:
                    rand_ans = random.randint(0,4)
                    if rand_ans >= 0 and rand_ans < 4:
                        bot.send_message(messege.chat.id,'Если коротко, то ты проиграл',reply_markup=markup)
                    else:
                        bot.send_message(messege.chat.id,'Ну что я могу тебе сказать, ты лох',reply_markup=markup)
            except:
                markup_ppl = types.ReplyKeyboardMarkup()
                itembtn_ppl = types.KeyboardButton('⚾️')
                itembtn_ppl1 = types.KeyboardButton('🥎')
                markup_ppl.add(itembtn_ppl1, itembtn_ppl)
                bot.send_message(messege.chat.id, 'Пж выбери мячик и не пиши мне пургу', reply_markup=markup_ppl)
        
    elif check_code(messege.text) and len(messege.text) == 5: 
        db.update({'prom': getdb(messege.from_user.id) + get_code_much(messege.text)}, quv.userid == messege.from_user.id)
        bot.send_message(messege.chat.id, 'Код заюзан, +{} к твоим попыткам🎫'.format(get_code_much(messege.text)))
        del_code(messege.text)
    
    elif messege.text == '🚧Кол-во моих попыток':
        bot.send_message(messege.chat.id, f'В данный момент у тебя {getdb(messege.from_user.id)} попыток')
    elif messege.text == 'Монеты в попытки🪤':
        if getdb(messege.from_user.id, 3) <= 0:
            bot.send_message(messege.chat.id,'Нельзя играть когда у тебя *0* попыток',parse_mode= 'Markdown')
        else:
            bot.send_message(messege.chat.id,'Курс: *1* к *1*', 'Markdown')
            sent = bot.send_message(messege.chat.id,'Окей, сколько монет поменять?')
            bot.register_next_step_handler(sent, how_many_change)
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
            bot.send_message(messege.chat.id,'Нельзя играть когда у тебя *0* попыток',parse_mode= 'Markdown')
    elif messege.text == 'Кол-во моих монет🏦':
        rand_ans = random.randint(0,4)
        if rand_ans >= 0 and rand_ans < 3:
            bot.send_message(messege.chat.id,f'У тебя {getdb(messege.from_user.id, 3)} монет.')
        elif rand_ans == 3:
            bot.send_message(messege.chat.id,f'У тебя {getdb(messege.from_user.id, 3)} монет, ну ты и бомж конечно.')
        else:
            bot.send_message(messege.chat.id,f'У тебя {getdb(messege.from_user.id, 3)} монет, ШИКУЕМ 🥁🎉🎉.')
            
    #admin pan inside
    elif messege.from_user.id == 999711677:
        with open('tmp/tmp_del', 'r') as del_check:
            del_check = int(del_check.read())
        if del_check == 1:
            with open('tmp/tmp_user_del', 'w') as tmp_user_del:
                tmp_user_del.write(messege.text)
                with open('tmp/tmp_del','w') as del_write:
                    del_write.write('2')
                bot.send_message(messege.chat.id, 'Сколько монет изъять??🙃')
        elif del_check == 2:
            with open('tmp/tmp_user_del', 'a') as tmp_user_del:
                tmp_user_del.write('\n' + messege.text)
                with open('tmp/tmp_del','w') as del_write:
                    del_write.write('0')
            with open('tmp/tmp_user_del','r')as tmp_user_del:
                del_list = list(tmp_user_del.read().split('\n'))
            try:
                del_mon(int(del_list[0]),int(del_list[1]))
                tem_user_var = getdb(int(del_list[0]), 4)
                how_much_has = getdb(int(del_list[0]), 3)
                bot.send_message(messege.chat.id,f'Только что изъял {del_list[1]} от {tem_user_var}🍜🍜, теперь у него/нее на счету монет {how_much_has}')

            except:
                bot.send_message(messege.chat.id,'Ошибонька при изъятии 🤯')
        
        with open('tmp/tmp_add', 'r') as del_check:
            del_check = int(del_check.read())
        if del_check == 1:
            with open('tmp/tmp_user_add', 'w') as tmp_user_del:
                tmp_user_del.write(messege.text)
                with open('tmp/tmp_add','w') as del_write:
                    del_write.write('2')
                bot.send_message(messege.chat.id, 'Скок добавить?🤔')
        elif del_check == 2:
            with open('tmp/tmp_user_add', 'a') as tmp_user_del:
                tmp_user_del.write('\n' + messege.text)
                with open('tmp/tmp_add','w') as del_write:
                    del_write.write('0')
            with open('tmp/tmp_user_add','r')as tmp_user_del:
                del_list = list(tmp_user_del.read().split('\n'))
            try:
                add_mon(int(del_list[0]),int(del_list[1]))
                tem_user_var = getdb(int(del_list[0]), 4)
                how_much_has = getdb(int(del_list[0]), 3)
                bot.send_message(messege.chat.id,f'Только что добавил {del_list[1]} к балансу {tem_user_var}🥱, теперь у него/нее на счету монет {how_much_has}.')

            except:
                bot.send_message(messege.chat.id,'Ошибонька при добавлении 🫢')
        
        with open('tmp/tmp_send', 'r') as del_check:
            del_check = int(del_check.read())
        if del_check == 1:
            with open('tmp/tmp_user_send', 'w') as tmp_user_del:
                tmp_user_del.write(messege.text)
            with open('tmp/tmp_send','w') as del_write:  #posib error
                    del_write.write('2')
            with open('tmp/tmp_user_send', 'r') as tmp_user_del:
                user_id_send_for_db = tmp_user_del.read()
            try:
                bot.send_message(messege.chat.id, 'Что отправить {}?🛍'.format(getdb(int(user_id_send_for_db),4)))
            except:
                bot.send_message(messege.chat.id,'Ошибонька при отправлении📭')
                with open('tmp/tmp_send','w') as del_write:
                    del_write.write('0')
        elif del_check == 2:
            with open('tmp/tmp_user_send', 'a') as tmp_user_del:
                tmp_user_del.write('\n' + messege.text)
                with open('tmp/tmp_send','w') as del_write:
                    del_write.write('0')
            with open('tmp/tmp_user_send','r')as tmp_user_del:
                del_list = list(tmp_user_del.read().split('\n'))
            try:
                tem_user_var = getdb(int(del_list[0]), 4)
                bot.send_message(int(del_list[0]), str(del_list[1]))
                bot.send_message(messege.chat.id, 'Только что отправил # {} # кому: {} 📬'.format(del_list[1], tem_user_var))

            except:
                bot.send_message(messege.chat.id,'Ошибонька при отправлении📭')
        
        if messege.text == '👛Новый код👛':
            send = bot.send_message(messege.chat.id, 'Количество')
            bot.register_next_step_handler(send, new_code_after_much)
        elif messege.text == '📃Показать все коды📃':
            code_list = db.search(quv.type == 'code')
            if not code_list:
                bot.send_message(messege.chat.id,'Кодов больше нет👨‍🦯👨‍🦯')
            else:
                code_str = ''
                for i in range(len(code_list)):
                    code_str += 'Код {} Дает {}\n'.format(code_list[i]['code'],code_list[i]['much'])
                bot.send_message(messege.chat.id, code_str)        
        elif messege.text == '🧁Информация о пользователях🧁':
            tmp_list = db.search(quv.type == 'user')
            for i in range(len(tmp_list)):
                temp_ran = tmp_list[i]
                with open('tmp/tmp_list.txt', 'a') as ttmp:
                    user = temp_ran['userid']
                    mon = temp_ran['mon']
                    prom = temp_ran['prom']
                    username = temp_ran['username']
                    ttmp.write(f'\nИдшка.  {user} Нейм.  {username} Монетки.  {mon} Попытки.  {prom}')
            with open('tmp/tmp_list.txt', 'rb') as last_use_tmlist:
                bot.send_message(messege.chat.id,last_use_tmlist.read())
                os.remove("tmp/tmp_list.txt")
        elif messege.text == '💳🔨Изъять монеты':
            with open('tmp/tmp_del', 'w') as tmp_del:
                tmp_del.write('1')
            bot.send_message(messege.chat.id,'Кинь idшку')
        elif messege.text == '📥💵Добавить монеты':
            with open('tmp/tmp_add', 'w') as tmp_del:
                tmp_del.write('1')
                bot.send_message(messege.chat.id,'Кинь idшку')
        elif messege.text == '📨Отправить сообщение':
            with open('tmp/tmp_send', 'w') as tmp_del:
                tmp_del.write('1')
                bot.send_message(messege.chat.id,'Кинь idшку')
    else:
        strpon = messege.text
        if 'пон' in strpon.lower():
            notoz = ['Не быкуй а?', 'А вот я тебя не понял', 'Ок…']
            bot.reply_to(messege,random.choice(notoz))
        else:
            not_und = ['Не пон че ты шпрехаеш', 'Я тебя не понимать блин', 'Нефига не понял, Миша давай все по новой','Мой русский не понимать твоего язык']
            bot.send_message(messege.chat.id,random.choice(not_und))
def how_many_change(messege):
    if isdigit(messege.text):
        try:
            if int(getdb(messege.from_user.id, 3)) - int(messege.text) < 0:
                bot.send_message(messege.chat.id,'Поменять больше чем есть, *нельзя*', 'Markdown')
            else:
                db.update({'mon': getdb(messege.from_user.id, 3) - int(messege.text), 'prom': getdb(messege.from_user.id) + int(messege.text)}, quv.userid == messege.from_user.id)
                bot.send_message(messege.chat.id,'Теперь у тебя Монет: {} Попыток: {}'.format(getdb(messege.from_user.id, 3), getdb(messege.from_user.id)))
        except Exception as e:
            bot.send_message(messege.chat.id,e)
    else:
        bot.send_message(messege.chat.id,'Введи число гений')
much_prom_temp = 1
def new_code_after_much(messege):
    global much_prom_temp 
    much_prom_temp = int(messege.text)
    sent = bot.send_message(messege.chat.id, 'На сколько?')
    bot.register_next_step_handler(sent, new_code_after_cost)
def new_code_after_cost(messege):
    try:
        for i in range(much_prom_temp):
            ncode = new_code()
            db.insert({'code': ncode, 'much': int(messege.text), 'type': 'code'})
            bot.send_message(messege.chat.id, f'Новый код {ncode} : {messege.text}')
    except Exception as e:
        bot.send_message(messege.chat.id, e)
bot.polling(none_stop=True)