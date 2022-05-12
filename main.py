from operator import le
import time
from webbrowser import get
from telebot import types
import random
import telebot
from tinydb import TinyDB, Query
import os
import string
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import easyocr
from termcolor import colored
import qrcode


bot = telebot.TeleBot('5311428361:AAHmz1afEFRPBjN6fSHeARvarmyeNzsWIOA')
admin_list = [999711677]

db = TinyDB('../db.json')
quv = Query()
def np(text: str):
    for i in text:
        print(i, end="", flush=True)
        time.sleep(.05)
    print('\n')
def new_job_id():
    prom_temp = ''
    alfab = string.ascii_uppercase + string.digits
    for i in range(8):
        prom_temp += random.choice(alfab)
    return prom_temp 
def get_sell_cost(id):
    list = db.search(quv.id == id)
    list = list[0]
    return list['cost']
def sell(text: str, creator:str, cost = 1):
    id_j = new_job_id()
    db.insert({'type': 'sell', 'text': text, 'creator': creator, 'cost': cost, 'id': id_j})
    return id_j
def new_job(text: str, creator:str, cost = 1):
    id_j = new_job_id()
    db.insert({'type': 'job', 'text': text, 'creator': creator, 'cost': cost, 'id': id_j})
def code_to_qr(code):
    img = qrcode.make(f'tg://msg_url?url={code}')
    img.save("pic/qr.png")

def log(messege):
    match messege.content_type:
        case 'dice':
            np(colored('[user {}] '.format(getdb(messege.from_user.id, 4)), 'red') + 'Em : {}| Result {}'.format(str(messege.dice.emoji), str(messege.dice.value)))
        case 'text':
            np(colored('[user {}] '.format(getdb(messege.from_user.id, 4)), 'red') + colored(messege.text, 'blue'))

def get_code_from_img(imP: str):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(imP)
    if not result:
        return ''
    else:
        result = result[0][1].replace("O","0")
        return result

def code_to_text(code: str, code_much: str):
    img = Image.open("pic/grad.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('Lato.ttf', 250)
    font2 = ImageFont.truetype('Lato.ttf', 200)
    draw.text((440, 460),code,(255,255,255),font=font) 
    draw.text((1560, 940),code_much,(255,255,255),font=font2)
    img.save('pic/out.png')

def new_user(id,username='anonim'):
    db.insert({'userid': id, 'prom': 0 , 'mon': 0, 'username': username,'next_win': False, 'type': 'user'})

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
def get_code_much(code: str):
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
    alfab = alfab.replace("O", "")
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
def photo(messege):
    #photo_ans = ['Ладно', '🤨📸', 'За такое в некоторых странах сажают...', 'Это не план захвата Польши.', 'План захвата Польши?!?!?!', 'Пожалуй это я сохраню']
    raw = messege.photo[2].file_id
    path = raw+".png"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path,'wb') as new_file:
        new_file.write(downloaded_file)
    code = get_code_from_img(path)
    print(code)
    if check_code(code):
        db.update({'prom': getdb(messege.from_user.id) + get_code_much(code)}, quv.userid == messege.from_user.id)
        bot.send_message(messege.chat.id, 'Код заюзан, +{} к твоим попыткам🎫'.format(get_code_much(code)))
        del_code(code)
    else:
        bot.reply_to(messege, """Код не использован по одной из причин:
1. Это не кодКарточка
2. Код не действителен 
3. Код не удалось распознать
============================
Попробуй ввести код в ручную либо проверь код /check_prom""")
    os.remove(path)



@bot.message_handler(func=lambda messege: True ,content_types=["voice", "audio"])
def voice(messege):
    audio_ans = ['Ну ок и что?', 'Что за стоны','Ты там не разборчиво говоришь да и мне пофиг', 'Зачем мне по твоему это?', 'Хз']
    bot.reply_to(messege, random.choice(audio_ans))

@bot.message_handler(func=lambda messege: True ,content_types=["video"])
def video(messege):
    video_ans = ['Я планирую польшу захватывать, это мне не поможет.', 'Илон маск покупает это видео', 'Ничего гениальнее я ещё не видел', '🦽?', 'Если бы я был живим то вызвал бы копов👨‍🦯']
    bot.reply_to(messege, random.choice(video_ans))

@bot.message_handler(func=lambda messege: True ,content_types=["animation"]) 
def gif(messege):
    animation_ans = ['Не грузит, это что-то важное?', 'У-у-у-у-у 🐒', 'Эмз, потому что только у нее есть телефон', '🙋‍♂️', 'Ульяна, вы?🧐']
    bot.reply_to(messege, random.choice(animation_ans))
@bot.message_handler(commands=['kill_codes'])
def kill_codes(messege):
    global admin_list
    if messege.from_user.id in admin_list:
        much_codes_remove = len(db.search(quv.type == 'code'))
        db.remove(quv.type == 'code')
        bot.send_message(messege.chat.id, f'Удачно удалил {much_codes_remove} кодов')

@bot.message_handler(commands=['code_to_qr'])
def code_to_qr_f(messege):
    global admin_list
    if messege.from_user.id in admin_list:
        sent = bot.send_message(messege.chat.id, 'Напиши код 👩🏻‍🦰')
        bot.register_next_step_handler(sent, ctqwhand)
def ctqwhand(messege):
    code_to_qr(messege.text)
    with open('pic/qr.png', 'rb') as qr:
        bot.send_photo(messege.chat.id, qr)

@bot.message_handler(commands=['next_win'])
def next_win_hand(messege):
    global admin_list
    if messege.from_user.id in admin_list:
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
    mes = "/kill_codes - Удалить все коды \n/next_win - В след раз игрок точно выиграет \n/code_to_text - Версия кода в картинке\n/code_to_qr - Код в QR.code"
    global admin_list
    if messege.from_user.id in admin_list:
        bot.send_message(messege.chat.id,mes)

@bot.message_handler(commands=['code_to_text'])
def ctt(messege):
    global admin_list
    if messege.from_user.id in admin_list:
        sent =  bot.send_message(messege.chat.id,'Код:')
        bot.register_next_step_handler(sent, ctth)
def ctth(messege):
    try:
        code_to_text(messege.text, str(get_code_much(messege.text)))
        with open('pic/out.png', 'rb') as out_pic:
            bot.send_photo(messege.chat.id, out_pic)
    except Exception:
        bot.send_message(messege.chat.id, 'Код не найден🌩')
@bot.message_handler(commands=['play'])
def play(messege):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton('🎯')
    markup.add(item1)
    bot.send_message(messege.chat.id, """
    *Отправь смайлик чтоб начать игру*\n
    🎯 - Шанс выиграть 1 к 3 *Выигрыш От 1 до 3 монет*

    🎲 - Шанс выиграть 1 к 6 *Выигрыш 6 монет*

    🎳 - Шанс выиграть 1 к 3 *Выигрыш От 1 до 3 монет*

    🏀 - Шанс выиграть 2 к 5 *Выигрыш 2 монеты*
    
    """
    , parse_mode= 'Markdown')

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
        elif messege.dice.emoji == '🎳':
            time.sleep(4)
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
        elif messege.dice.emoji == '🏀':
            time.sleep(4)
            if messege.dice.value == 4 or messege.dice.value == 5 or next_win_check(messege.from_user.id):
                db.update({'mon': getdb(messege.from_user.id, 3) + 2, 'prom': getdb(messege.from_user.id) - 1}, quv.userid == messege.from_user.id)
                next_win(messege.from_user.id, 0)
                bot.send_message(messege.chat.id, 'ты выиграл 2 монеты, теперь у тебя *{}* монет'.format(getdb(messege.from_user.id,3)),parse_mode='Markdown')
            else:
                db.update({'prom': getdb(messege.from_user.id) - 1}, quv.userid == messege.from_user.id)
                bot.send_message(messege.chat.id, random.choice(no_win_mes))
        else:
            bot.send_message(messege.chat.id, 'Эта игра пока что не поддерживается')
        log(messege)
@bot.message_handler(commands=['info'])
def info(messege):
    mes = """
    *Информация по боту*
    Бот создан на языке Python3
    Просто по рофлу 
    *____________________________*
    Версия *1.2*
    
    Создатель *Klesberg*
    """
    bot.send_message(messege.chat.id,mes,parse_mode= 'Markdown')
#admin pannel
@bot.message_handler(commands=['adm'])
def adm(messege):
    global admin_list
    if messege.from_user.id in admin_list:
        markup = types.ReplyKeyboardMarkup()
        admitem1 = types.KeyboardButton('👛Новый код👛')
        admitem2 = types.KeyboardButton('📃Показать все коды📃')
        admitem3 = types.KeyboardButton('🧁Информация о пользователях🧁')
        admitem4 = types.KeyboardButton('💳🔨Изъять монеты')
        admitem5 = types.KeyboardButton('📥💵Добавить монеты')
        admitem6 = types.KeyboardButton('📨Отправить сообщение')
        admitem7 = types.KeyboardButton('Объявление💤')
        admitem8 = types.KeyboardButton('Редакция продаж🚰')
        markup.add(admitem1, admitem2, admitem3, admitem4, admitem5, admitem6, admitem7, admitem8)
        bot.send_message(messege.chat.id,'⚗️Что мне делать🪬', reply_markup=markup)
    else:
        bot.send_message(messege.chat.id,'Вам нельзя пользоваться этой функцией🔐')

#start
@bot.message_handler(commands=['start'])
def start(messege):
    user_id = messege.from_user.id
    username = messege.from_user.username
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Попытать удачу🎢')
    markup.add(itembtn1)
    try:
        
        bot.send_message(messege.chat.id, f'Добро пожаловать обратно {messege.from_user.username} 🖇,на текущий момент у вас {getdb(user_id)} попыток', reply_markup=markup)
    except:
        new_user(user_id, username)
        bot.send_message(messege.chat.id, f'Здравствуй {messege.from_user.username}, и добро пожаловать.',reply_markup=markup)
def ball_mark():
    markup_pl = types.ReplyKeyboardMarkup()
    itembtn_pl = types.KeyboardButton('⚾️')
    itembtn_pl1 = types.KeyboardButton('🥎')
    return markup_pl.add(itembtn_pl1, itembtn_pl)

def menu_mark():
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('🚧Кол-во моих попыток')
    itembtn2 = types.KeyboardButton('Попытать удачу🎢')
    itembtn3 = types.KeyboardButton('Кол-во моих монет🏦')
    itembtn4 = types.KeyboardButton('Монеты в попытки🪤')
    itembtn5 = types.KeyboardButton('Отправить попытки ☕️')
    #itembtn6 = types.KeyboardButton('Создать задание♻️')   
    itembtn7 = types.KeyboardButton('Список заданий💰')
    itembtn8 = types.KeyboardButton('Мои задания🚀')
    itembtn9 = types.KeyboardButton('Мои продажи🕯')
    itembtn10 = types.KeyboardButton('Рынок🛒')
    return markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn7, itembtn8, itembtn9, itembtn10)

@bot.message_handler(commands=['menu'])
def menu(messege):
    bot.send_message(messege.chat.id,'Чего хочешь:',reply_markup=menu_mark())


#text handler
@bot.message_handler(content_types=['text'])   
def text_input(messege):
    global admin_list
    #markup = menu_mark()
        
    if check_code(messege.text) and len(messege.text) == 5: 
        db.update({'prom': getdb(messege.from_user.id) + get_code_much(messege.text)}, quv.userid == messege.from_user.id)
        bot.send_message(messege.chat.id, 'Код заюзан, +{} к твоим попыткам🎫'.format(get_code_much(messege.text)))
        del_code(messege.text)
    
    elif messege.text == '🚧Кол-во моих попыток':
        bot.send_message(messege.chat.id, f'В данный момент у тебя {getdb(messege.from_user.id)} попыток')
    
    
    elif messege.text == 'Монеты в попытки🪤':
        if getdb(messege.from_user.id,3) <= 0:
            bot.send_message(messege.chat.id,'Нельзя отправить когда у тебя *0* попыток',parse_mode= 'Markdown')
        else:
            bot.send_message(messege.chat.id,'Доступно к обмену *{}*'.format(getdb(messege.from_user.id, 3)), 'Markdown')
            sent = bot.send_message(messege.chat.id,'Окей, сколько монет поменять?')
            bot.register_next_step_handler(sent, how_many_change)
    
    
    
    elif messege.text == 'Попытать удачу🎢':
        if getdb(messege.from_user.id) > 0 :
            sent = bot.send_message(messege.chat.id,'Ставка🥣')
            bot.register_next_step_handler(sent, get_bit)
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
    
    
    
    elif messege.text == 'Отправить попытки ☕️':
        if getdb(messege.from_user.id) <= 0:
            bot.send_message(messege.chat.id, '🫧Нельзя отправлять попытки когда у тебя баланс на нуле🫧')
        else:
            user_db = db.search(quv.type == 'user')
            user_list = ''
            for i in range(len(user_db)):
                user_list += str(user_db[i]['username']) + '\n'
            sent = bot.send_message(messege.chat.id, 'Кому 🍯')
            bot.register_next_step_handler(sent, who_to_sent_code)
            bot.send_message(messege.chat.id, user_list)
        



    elif messege.text == 'Список заданий💰':
        jobs = db.search(quv.type == 'job')
        if not jobs:
            stickers = ['CAACAgIAAxkBAAEEtS9ifBxZxyTt8oWl3LX2LrubTJw56wACcAEAAgeGFQcK02XiqsOA_iQE','CAACAgIAAxkBAAEEtR1ifBpiliaXWc092y3ZOO1g3lKk2AACPhYAAvBTQUlpEWrlxJ6_-CQE', 'CAACAgIAAxkBAAEEtStifBxSf_jESFnQwaHkQZV9Nwk70gACeAEAAgeGFQf_I5bs8gjuziQE','CAACAgIAAxkBAAEEtSdifBwwqMS8GHpgDNBKY6yEE9ZcJQACfQEAAgeGFQeBvq55j6-apCQE','CAACAgIAAxkBAAEEtSVifBwmeTfN5LCklLL7gJ2QLA7_ugACbQEAAgeGFQfadHKlB3PdJCQE']
            bot.send_message(messege.chat.id,'Заданий нет, отдыхай🏖')
            bot.send_sticker(messege.chat.id, random.choice(stickers))
        else:
            for i in range(len(jobs)):
                bot.send_message(messege.chat.id, '{}\nНаграда: {}\n{}'.format(jobs[i]['creator'], jobs[i]['cost'], jobs[i]['text']))
        
    elif messege.text == 'Мои задания🚀':
        temp_var = 0
        my_jobs = db.search(quv.type == 'job')
        if my_jobs:
            for i in range(len(my_jobs)):
                if my_jobs[i]['creator'] == getdb(messege.from_user.id, 4):
                    temp_var += 1
                    mj_markup = types.InlineKeyboardMarkup()
                    m1 = types.InlineKeyboardButton('✅Выполнено', callback_data='y' + my_jobs[i]['id'])
                    m2 = types.InlineKeyboardButton('❌Удалить', callback_data='n' + my_jobs[i]['id'])
                    mj_markup.add(m1,m2)
                    bot.send_message(messege.chat.id, 'Награда: {}\n———————————\n{}'.format(my_jobs[i]['cost'], my_jobs[i]['text']), reply_markup=mj_markup)         
            if temp_var == 0:
                bot.send_message(messege.chat.id, 'У тебя нет заданий🧼')
        else:
            bot.send_message(messege.chat.id, 'У тебя нет заданий🧼')
        markup_addjob = types.InlineKeyboardMarkup()
        m1 = types.InlineKeyboardButton('Создать задание♻️', callback_data='j')
        markup_addjob.add(m1)
        bot.send_message(messege.chat.id, 'Опиши свое задание🍯', reply_markup=markup_addjob)
            
    
    elif messege.text == 'Мои продажи🕯':
        temp_var = 0
        my_sells = db.search(quv.type == 'sell') 
        if my_sells:
            for i in range(len(my_sells)):
                if my_sells[i]['creator'] == getdb(messege.from_user.id, 4):
                    temp_var += 1
                    mj_markup = types.InlineKeyboardMarkup()
                    m1 = types.InlineKeyboardButton('❌Удалить', callback_data='0' + my_sells[i]['id'])
                    mj_markup.add(m1)
                    bot.send_message(messege.chat.id, '{}\n———————————\nСтоимость🍰: {}'.format(my_sells[i]['text'], my_sells[i]['cost']), reply_markup=mj_markup)
            if temp_var == 0:
                bot.send_message(messege.chat.id, 'У тебя нет продаж🧋')
        else:
            bot.send_message(messege.chat.id, 'У тебя нет продаж🧋')
        markup_sell = types.InlineKeyboardMarkup()
        m1 = types.InlineKeyboardButton('Продать🍸', callback_data='s')
        markup_sell.add(m1)
        bot.send_message(messege.chat.id, 'Создать обьявление о продаже💶', reply_markup=markup_sell)



    elif messege.text == 'Рынок🛒':
        buy_list = db.search(quv.type == 'sell')
        if not buy_list:
            bot.send_message(messege.chat.id, 'Пока что ничего не продаеться🛌')
        else:
            for i in range(len(buy_list)):
                if buy_list[i]['creator'] != getdb(messege.from_user.id, 4):
                    mj_markup = types.InlineKeyboardMarkup()
                    m1 = types.InlineKeyboardButton('Купить💳', callback_data='b' + buy_list[i]['id'])
                    mj_markup.add(m1)
                    bot.send_message(messege.chat.id, '{}\n———————————\nСтоимость🍰: {}\nВладелец обьявления {}'.format(buy_list[i]['text'], buy_list[i]['cost'], buy_list[i]['creator']), reply_markup=mj_markup)
                
    
    
    #admin pan inside
    elif messege.from_user.id in admin_list:
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
        elif messege.text == 'Объявление💤':
            send = bot.send_message(messege.chat.id, 'Карякай Объявление') 
            bot.register_next_step_handler(send, anons)
        elif messege.text == 'Редакция продаж🚰':
            adm_sells = db.search(quv.type == 'sell') 
            if adm_sells:
                for i in range(len(adm_sells)):
                    mj_markup = types.InlineKeyboardMarkup()
                    m1 = types.InlineKeyboardButton('❌Удалить', callback_data='0' + adm_sells[i]['id'])
                    mj_markup.add(m1)
                    bot.send_message(messege.chat.id, '{}\n———————————\nСтоимость🍰: {}\nВладелец обьявления {}'.format(adm_sells[i]['text'], adm_sells[i]['cost'], adm_sells[i]['creator']), reply_markup=mj_markup)
            else:
                bot.send_message(messege.chat.id, 'У тебя нет продаж🧋')
    else:
        strpon = messege.text
        if 'пон' in strpon.lower():
            notoz = ['Не быкуй а?', 'А вот я тебя не понял', 'Ок…']
            bot.reply_to(messege,random.choice(notoz))
        else:
            not_und = ['Не пон че ты шпрехаеш', 'Я тебя не понимать блин', 'Нефига не понял, Миша давай все по новой','Мой русский не понимать твоего язык']
            bot.send_message(messege.chat.id,random.choice(not_und))
    log(messege)
job_text_var = ''
def job_text(messege):
    global job_text_var 
    job_text_var = messege.text
    sent = bot.send_message(messege.chat.id, 'Какое вознаграждение?')
    bot.register_next_step_handler(sent, job_cost)
def job_cost(messege):
    global job_text_var
    try:
        if int(messege.text) <= 0:
            bot.send_message(messege.chat.id, 'Нельзя ставить отрицательные число🔧')
        elif getdb(messege.from_user.id) - int(messege.text) >= 0:
            db.update({'prom': getdb(messege.from_user.id) - int(messege.text)}, quv.userid == int(messege.from_user.id))
            new_job(job_text_var,getdb(messege.from_user.id,4), int(messege.text))
            bot.send_message(messege.chat.id, 'Задание успешно создано📝')
            bot.send_sticker(messege.chat.id, 'CAACAgIAAxkBAAEEtT5ifB2cOysQNL7ekNpwMn683G_QlgACbwEAAgeGFQeqOYyl3u2YdiQE')
        else:
            bot.send_message(messege.chat.id, 'Не хватит денег 💸')
    except:
        sent = bot.send_message(messege.chat.id, 'Напиши число')
        bot.register_next_step_handler(sent,job_cost)
def anons(messege):
    job_d = messege.text
    users = db.search(quv.type == 'user')
    for i in range(len(users)):
        if users[i]['userid'] in admin_list:
            pass
        else:
            bot.send_message(users[i]['userid'], 'Объявление: ' + job_d)

def how_many_change(messege):
    try:
        if int(getdb(messege.from_user.id, 3)) - int(messege.text) < 0:
            bot.send_message(messege.chat.id,'Поменять больше чем есть, *нельзя*', 'Markdown')
        else:
            db.update({'mon': getdb(messege.from_user.id, 3) - int(messege.text), 'prom': getdb(messege.from_user.id) + int(messege.text)}, quv.userid == messege.from_user.id)
            bot.send_message(messege.chat.id,'Теперь у тебя Монет: {} Попыток: {}'.format(getdb(messege.from_user.id, 3), getdb(messege.from_user.id)))
    except Exception:
        bot.send_message(messege.chat.id,'Упс что то пошло не так🫢')
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
            code_to_text(str(ncode), messege.text)
            with open('pic/out.png', 'rb') as img_send:
                bot.send_photo(messege.chat.id, img_send)
            bot.send_message(messege.chat.id, f'Новый код {ncode} : {messege.text}')

    except Exception as e:
        bot.send_message(messege.chat.id, e)
name_to_send_code = ''
def who_to_sent_code(messege):
    if getdb(messege.from_user.id) <= 0:
        bot.send_message(messege.chat.id, '🫧Нельзя отправлять попытки когда у тебя баланс на нуле🫧')
    else:
        global name_to_send_code
        name_to_send_code = messege.text
        name = db.search(quv.username == name_to_send_code)
        try:
            sent = bot.send_message(messege.chat.id, 'Сколько отправить {}🍻'.format(name[0]['username']))
            bot.register_next_step_handler(sent, how_much_code_sent)
        except Exception:
            bot.send_message(messege.chat.id,'Такого имени не существует 🥤')

def how_much_code_sent(messege):
    global name_to_send_code
    if int(messege.text) < 0:
        bot.send_message(messege.chat.id, 'Такой трюк не прокатит🚔')
    else:
        try:
            id_user = db.search(quv.username == name_to_send_code)
            if getdb(messege.from_user.id) - int(messege.text) >= 0:
                db.update({'prom': getdb(messege.from_user.id) - int(messege.text)}, quv.userid == int(messege.from_user.id))
                db.update({'prom': getdb(id_user[0]['userid']) + int(messege.text)}, quv.username == name_to_send_code)
                bot.send_message(messege.chat.id, 'Успешно перечислил {} {} 🥣'.format(name_to_send_code, messege.text))
                bot.send_sticker(messege.chat.id, 'CAACAgIAAxkBAAEEtU1ifB4YdekfqdxMD8OuNmYb6KXnwwACgwEAAgeGFQdsHwABu9sMwMgkBA')
                bot.send_message(id_user[0]['userid'], 'Вам пришло {} попыток от {}🎁'.format(messege.text, getdb(messege.from_user.id,4)))
                bot.send_sticker(id_user[0]['userid'], 'CAACAgIAAxkBAAEEtU9ifB4rhb9xwHmxBgOJPyYfNReRbwACjgEAAgeGFQduJUVzTsacOiQE')
            else:
                bot.send_message(messege.chat.id, '🫧Нельзя отправлять попытки когда у тебя баланс на нуле🫧')
        except:
            bot.send_message(messege.chat.id, 'Ошибка при отправке🍪🥛')
user_bit = 0
def get_bit(messege):
    global user_bit
    try:
        user_bit = int(messege.text)
        if getdb(messege.from_user.id) - int(messege.text) >= 0 and int(messege.text) != 0:
            sent = bot.send_message(messege.chat.id, '🥎 или ⚾️?', reply_markup=ball_mark())
            bot.register_next_step_handler(sent, throw_ball)
        else:
            bot.send_message(messege.chat.id, 'Ошибка🚭')
    except Exception as e:
        print(e)
        bot.send_message(messege.chat.id, 'Ошибка🚭')

def throw_ball(messege):
    global user_bit
    rend_cal = {'🥎': 0, '⚾️': 1}
    rend = random.randrange(0,2)
    try:
        if rend_cal[messege.text] == rend or next_win_check(messege.from_user.id):
            db.update({'mon': getdb(messege.from_user.id, 3) + user_bit * 2, 'prom': getdb(messege.from_user.id) - user_bit}, quv.userid == messege.from_user.id)
            next_win(messege.from_user.id, 0)
            bot.send_message(messege.chat.id,f'Кросс, добавляю +{user_bit * 2} к твоему текущему балансу🥂',reply_markup=menu_mark())
        else:
            ans = ['Если коротко, то ты проиграл', 'Ну что я могу тебе сказать, ты лох']
            db.update({'prom': getdb(messege.from_user.id) - user_bit}, quv.userid == messege.from_user.id)
            bot.send_message(messege.chat.id,random.choice(ans),reply_markup=menu_mark())       
                        
    except:
        sent = bot.send_message(messege.chat.id, 'Пж выбери мячик и не пиши мне пургу', reply_markup=ball_mark())
        bot.register_next_step_handler(sent, throw_ball)

job_cost_var = 0
glob_job_var_id = ''
@bot.callback_query_handler(lambda query: query.data)
def call_back(data):
    try:
        job_id = data.data[1:]
        match data.data[0]:
            case 'j':
                if getdb(data.from_user.id) > 0 :
                    sent = bot.send_message(data.from_user.id, 'Опиши свое задание🍯')
                    bot.register_next_step_handler(sent, job_text)
                else:
                    bot.send_message(data.from_user.id,'Нельзя давать задание когда у тебя *{}* попыток'.format(getdb(data.from_user.id)),parse_mode= 'Markdown')
        
            case 's':
                sent = bot.send_message(data.from_user.id, 'Что вы продаете?🎙')
                bot.register_next_step_handler(sent, get_sell_text)
            case '0':
                bot.delete_message(data.from_user.id,data.message.id)
                db.remove(quv.id == job_id)
                bot.send_message(data.from_user.id, 'Успешно удалил обьявление📦❌')
            case 'b':
                can_buy_check = getdb(data.from_user.id) - get_sell_cost(job_id)
                if can_buy_check >= 0:
                    job_desc = db.search(quv.id == job_id)
                    creator_tmp = db.search(quv.id == job_id)
                    creator = db.search(quv.username == creator_tmp[0]['creator'])
                    bot.delete_message(data.from_user.id,data.message.id)
                    db.update({'prom': getdb(data.from_user.id) - get_sell_cost(job_id)}, quv.userid == data.from_user.id)
                    db.update({'prom': getdb(creator[0]['userid']) + get_sell_cost(job_id)}, quv.userid == creator[0]['userid'])
                    bot.send_message(data.from_user.id, 'Покупка успешна📦\nКод: {}🔑'.format(job_id))
                    bot.send_message(creator[0]['userid'], 'У вас купили\n~~~~~~~~\n{}\n~~~~~~~~\nПокупатель: {}🎈\nКлюч: {}🔑'.format(job_desc[0]['text'],getdb(data.from_user.id, 4), job_id))
                    db.remove(quv.id == job_id)
                else:
                    bot.send_message(data.from_user.id, 'Вам нехватает {} попыток🪙'.format(-can_buy_check))
            case _:    
                global job_cost_var, glob_job_var_id
                get_cost = db.search(quv.id == job_id)
                get_cost = get_cost[0]['cost']
                job_cost_var = get_cost
                glob_job_var_id = job_id
                user_db = db.search(quv.type == 'user')
                user_list = ''
                match data.data[0]:
                    case 'y':
                        sent = bot.send_message(data.from_user.id, 'Кто выполнил задание?🪙')
                        bot.delete_message(data.from_user.id,data.message.id)
                        for i in range(len(user_db)):
                            user_list += str(user_db[i]['username']) + '\n'
                        bot.send_message(data.from_user.id, user_list)
                        bot.register_next_step_handler(sent,who_do_job)
                    case 'n':
                        db.update({'prom': getdb(data.from_user.id) + get_cost}, quv.userid == data.from_user.id)
                        bot.delete_message(data.from_user.id,data.message.id)
                        db.remove(quv.id == job_id)
                        bot.send_message(data.from_user.id, 'Успешно удалил задание✅\nПопытки вернулись на счёт💡')
    except Exception as e:
        print(e)
get_sell_text_var = ''
def get_sell_text(messege):
    global get_sell_text_var
    get_sell_text_var = messege.text
    sent = bot.send_message(messege.chat.id, 'Укажите стоимость📡')
    bot.register_next_step_handler(sent, get_sell_cost_hand)
def get_sell_cost_hand(messege):
    global get_sell_text_var 
    try:
        if int(messege.text) > 0:
            sell_id = sell(get_sell_text_var,getdb(messege.from_user.id,4), int(messege.text))
            bot.send_message(messege.chat.id, 'Успешно🧉')
            my_sells = db.search(quv.id == sell_id)
            mj_markup = types.InlineKeyboardMarkup()
            m1 = types.InlineKeyboardButton('❌Удалить', callback_data='0' + my_sells[0]['id'])
            mj_markup.add(m1)
            bot.send_message(messege.chat.id, '{}\n———————————\nСтоимость🍰: {}'.format(my_sells[0]['text'], my_sells[0]['cost']), reply_markup=mj_markup)
        else:
            bot.send_message(messege.chat.id,'Увы меньше нуля нульзя указывать цену🧯')
    except:
        sent = bot.send_message(messege.from_user.id,'Введите число🔢')
        bot.register_next_step_handler(sent, get_sell_cost_hand)

def who_do_job(messege):
    global job_cost_var, glob_job_var_id
    try:
        user = db.search(quv.username == messege.text)
        if not user:
            bot.send_message(messege.chat.id, 'Пользователь не найден🪫')
        else:
            db.update({'prom': getdb(user[0]['userid']) + job_cost_var}, quv.userid == user[0]['userid'])
            bot.send_message(messege.chat.id,'Успешно💸')
            bot.send_message(user[0]['userid'],'Вам пришло {} попыток за выполнение задания💎'.format(job_cost_var))
            bot.send_sticker(user[0]['userid'], 'CAACAgIAAxkBAAEEtTtifB0afxXPMHM3KnufNClsNDpt0gACygEAAmJlAwABjtu6cwvGh2QkBA')
            db.remove(quv.id == glob_job_var_id)
    except Exception as e:
        bot.send_message(messege.chat.id, str(e) + ' 💊')


bot.polling(none_stop=True)
