import datetime
import time
import sqlite3
import telebot
import random
from telebot import types

bot = telebot.TeleBot('5418327966:AAGxElFTKrdmp3xPZRtc7K2U_lM12k0aZ4w')

# Стикеры и их id
"""
Фитнес, бег и прочая активность -  CAACAgIAAxkBAAEFNfVixrAjLZEIpSK5IwNVMjvR4EE66gACEhIAAkyR6EqiNLr5NJAJyCkE
дбж, кушать -CAACAgIAAxkBAAEFNfFixq9_T2T676HQ6HgzrBEQ4HN4fQACgRAAAn-cEUhlrV6kjetHSikE
Танцы - CAACAgIAAxkBAAEFNfNixq-mt_GdevueXAQDuh2vzOZrmQACmBcAAtIM6Es6Gdj5wk3wcykE
Душ - CAACAgIAAxkBAAEFNexixq9pRCmSnYoS-p_v3BWks15wzAACeBcAAl5e6Uua4FtQMS7rZikE
Праздник - CAACAgIAAxkBAAEFNfdixrA2b-9qgVtTcCI5ZeNOkH_ASwACwh MAAkFX6Epci86hwebrnSkE
Темп - CAACAgIAAxkBAAEFNf1ixrBvhirnTBs_qgl0fPDKKKQ8HgACVQUAAiMFDQAB-g1yS8IOivIpBA(Собака с пузырём в носу)
CAACAgIAAxkBAAEFNf9ixrBwv8eu_-JvhI5S_5Jm02ZEcgACXgUAAiMFDQABtT6G57w5L4MpBA
"""

db=sqlite3.connect('telegbot.db')
sqlcurs=db.cursor()
sqlcurs.execute("""CREATE TABLE IF NOT EXISTS users( 
  id INT,
  Activitys  TEXT,
  TIME TEXT
)""")
db.commit()

bot = telebot.TeleBot('5418327966:AAGxElFTKrdmp3xPZRtc7K2U_lM12k0aZ4w')
# Функция, обрабатывающая команду /start
listwithhistory=[]
# Tuple с id стикерами приветствия
tupleidwithhi=("CAACAgIAAxkBAAEFgsxi8jvdFzie2yebk6UtTpnl4t8VtgACNwADO2AkFJKJczNcKY76KQQ","CAACAgIAAxkBAAEFgspi8jvXwznpHZin12nhkFM1YIjA6gAC_AAD9wLID-JKwmellSruKQQ","CAACAgEAAxkBAAEFgshi8jvOfZFo8QABAWJyAzRKXIMmtusAAg8BAAI4DoIRtcxNf-IUkYIpBA"
               ,"CAACAgIAAxkBAAEFgsZi8jvHbwrlx3pS0ZBbAAH6FOnItF4AAp0AA-SgzgcAARSfeXjUPckpBA"
               ,"CAACAgIAAxkBAAEFgsRi8jvAXjqL6jwuzQbxYGpM74W5hgACxgEAAhZCawpKI9T0ydt5RykE"
               ,"CAACAgIAAxkBAAEFgsJi8ju4GdrrmyTmkN802kEfV9pyxQACHAAD9wLID3Acci1tkxh4KQQ"
               ,"CAACAgIAAxkBAAEFgsBi8juu06jbcQHe0BEE86JrGWCJMwACuQ0AAhRxwEvJIHUkgc_B3SkE"
               ,"CAACAgIAAxkBAAEFNeZixq7TKNMbZY6VHdndgHSvZM6RegACEhEAAj9w8Uo66W_N-9GmTykE")
#Когда наступает конец записи от Пользователя
endtuple=('конец','rjytw','клнец','end','rjy','rjytw')
# Разнообразие от бота
zapis=('так-так','Я записываю','Надеюсь это всё)Я шучу','Хорошо','Записал','Принял','Я запомнил','Так-с','yes, sir','Ого','Хорошое дело','Да ужжжжж','Вот те на','Интересненько','Прикольно')
endzapis=('А ты хорош.','Вот это да!Наполеоновские планы у тебя. Так держать!','Хороший план!Так держать!','Удачи тебе в выполнении!','Не важно, какое у тебя настроение.\nСделай по максимуму из того, что запланировал, и ты будешь гордиться собой.','"Создай шедевр из сегодня".\n-Джон Вуден.\n','Бдестящий у тебя план на день!\nСделай его по красоте.')
# TODO добавить, чтобы вместе с функцией выводились ещё и стикеры с отдыхом
# То есть 1) Дописываем tuple, 2)Прописываем логику вызова этого тапла, 3) Добавляем вывод стикеров.
# ПОСЛЕ Сделать тапл с разными стикерами приветствия
# Прописать приветсвие. (Пользователь будет это видеть, каждый раз, когда заходит записать новые дела.)
# Todo: доделать -->может добавить комманду конец, чтобы он моментально прерывал работу
vacationrest=('Хорошо, конечно, что ты так много напланировал себе. Но про отдых-то не забывай.)')
# Проверка на строку
def checkstr(string):
    return isinstance(string,str)

@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, f'Привет, {m.chat.first_name} {m.chat.last_name}.\n')
    bot.send_message(m.chat.id, 'Я бот-планировщик, если ты вдруг забыл(а).\nМожешь записать в меня список своих дел.')
    bot.send_sticker(m.chat.id, tupleidwithhi[random.randint(0,len(tupleidwithhi))])

    menumain=types.ReplyKeyboardMarkup(row_width=2)
    itemmaintoday=types.KeyboardButton('Сегодня 📖')
    itemmaintommorow=types.KeyboardButton('Завтра 🕘')
    menumain.add(itemmaintoday, itemmaintommorow)
    temm=bot.send_message(m.chat.id,"Выбери, на какой из дней, ты хочешь запланировать дела.",reply_markup=menumain)

#Функция, отвечающая за изменение списка дел
@bot.message_handler(commands=["changelist"])
def changelistuser(m):
    pass

#Функция, отвечающая за вывод списка листа
@bot.message_handler(commands=["printlist"])
def printlistuser(m):
    pass

@bot.message_handler(commands=["del"])
def deletelist(m):
    tempdel=None
    if len(listwithhistory)==0:
        bot.send_message(m.chat.id,"У вас пока нет записей, поэтому вам нечего удалять.\nМожете добавить свои записи выбрав в меню комманду /start")
    else:
        menudel = types.ReplyKeyboardMarkup(row_width=2)
        itemmadelall = types.KeyboardButton('Удалить все записи.')
        itemmadelnumber = types.KeyboardButton('Удалить запись по номеру.')
        menudel.add(itemmadelall, itemmadelnumber)
        tempdel = bot.send_message(m.chat.id, "Что именно вы хотите удалить.", reply_markup=menudel)
    delete_handler_list(m)

def delete_handler_list(m):
    if m.text=="Удалить все записи.":
        listwithhistory=[]
        bot.send_message(m.chat.id,'Ваш список дел очищен!')
    elif m.text=="Удалить запись по номеру.":
        numberdel=bot.send_message(m.chat.id,"Напишите через пробел номера, тех дел, которые хотите удалить.")
        bot.register_next_step_handler(numberdel,userdeletenumber())
        bot.send_message(m.chat.id,'Дела под номерами ')
    elif m.text=="/start":
        start(m)

@bot.message_handler()
def user_message(message):
    if checkstr(message.text):
        if message.text=="/start":
            start(message)
        if message.text=="Сегодня 📖" or message.text=="Завтра 🕘":
            listwithhistory.append(message.text)
            # Удаление кнопок происходит
            a = telebot.types.ReplyKeyboardRemove()
            mes = bot.send_message(message.from_user.id, "Напиши построчно список дел (одно дело = одна строка):", reply_markup=a)
        else:
            mes=bot.send_message(message.chat.id,zapis[random.randrange(len(zapis))])
        if  not(message.text.lower() in endtuple):
            bot.register_next_step_handler(mes,userobrab)
    else:
        bot.send_message(message.chat.id,"Ошибка в ведённой вами строке!\nПроверьте, что вы ввели строку.")

# Здесь записываются сообщения в list--TODO Переделать в бд
def userobrab(mesg):
    if checkstr(message.text):
        if not(mesg.text.lower() in endtuple):
            listwithhistory.append(mesg.text)
            user_message(mesg)
        else:
            bot.send_message(mesg.chat.id, 'Принято.\nЗапись окончена!')
            printhistory(mesg)
    else:
        bot.send_message(mesg.chat.id, 'Ошибка! Вы отправили не строку.')

def printhistory(re):
    if listwithhistory[0]=="Сегодня 📖":
        bot.send_message(re.chat.id,'Список сегодняшних дел:')
    else:
        bot.send_message(re.chat.id,'Ваши дела на завтра:')
    # Объединение текста в одно сообщение, + добавляем номера к каждому делу
    textmain=''
    for el in range(1,len(listwithhistory)):
        textmain+=f"{el})"+listwithhistory[el]+'\n'
    if len(listwithhistory)!=0:
        bot.send_message(re.chat.id,f" {textmain}")
        bot.send_sticker(re.chat.id, 'CAACAgIAAxkBAAEFRrVi0DdErwLlhVDmuUeTdGT-Ld0khQAC2w8AAjs_SUvTm6YwUBI-OCkE')
    else:
        bot.send_message(re.chat.id, "Список ваших дел пока пуст!")
#     markup = types.InlineKeyboardMarkup()
#     button1 = types.InlineKeyboardButton("Сайт Хабр",tempfunck(re))
#     markup.add(button1)
#     bot.send_message(re.chat.id,"Привет, {0.first_name}! Нажми на кнопку и перейди на сайт)".format(re.from_user),reply_markup=markup)
#
# # Темповская функция, которая не имеет ни какой логики пока что
# def tempfunck(m):
#     bot.send_message(m.chat.id,"Вы находитесь в темповской функции.")

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)