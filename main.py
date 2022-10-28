# import sqlite3
import random
import telebot
from telebot import types
from telegram.ext import Filters, MessageHandler
from datetime import datetime

bot = telebot.TeleBot('5418327966:AAGxElFTKrdmp3xPZRtc7K2U_lM12k0aZ4w')
# work with bd(sqlite3)
# db=sqlite3.connect('bdfortelegrambot.db')
# sql=db.cursor()
#
# sql.execute("""CREATE TABLE IF NOT EXISTS users (
#     user TEXT,
#     activities TEXT,
#     timeeveryact TimeOnly,
#     usertime TimeOnly,
#     nowday DateOnly)
# """)
# db.commit()




# Раздел "Правки":
# everytime when user adresses to bot, bot ask what time is the user? Необходимо, один раз спросить и больше не спрашивать
# Если пользователь зашёл, не первый раз, то выводить ему уже другое меню.


listwithhistory = []
listwithtime = []
# Tuple с id стикерами приветствия
tupleidwithhi = ("CAACAgIAAxkBAAEFgsxi8jvdFzie2yebk6UtTpnl4t8VtgACNwADO2AkFJKJczNcKY76KQQ",
                 "CAACAgIAAxkBAAEFgspi8jvXwznpHZin12nhkFM1YIjA6gAC_AAD9wLID-JKwmellSruKQQ",
                 "CAACAgEAAxkBAAEFgshi8jvOfZFo8QABAWJyAzRKXIMmtusAAg8BAAI4DoIRtcxNf-IUkYIpBA"
                 , "CAACAgIAAxkBAAEFgsZi8jvHbwrlx3pS0ZBbAAH6FOnItF4AAp0AA-SgzgcAARSfeXjUPckpBA"
                 , "CAACAgIAAxkBAAEFgsRi8jvAXjqL6jwuzQbxYGpM74W5hgACxgEAAhZCawpKI9T0ydt5RykE"
                 , "CAACAgIAAxkBAAEFgsJi8ju4GdrrmyTmkN802kEfV9pyxQACHAAD9wLID3Acci1tkxh4KQQ"
                 , "CAACAgIAAxkBAAEFgsBi8juu06jbcQHe0BEE86JrGWCJMwACuQ0AAhRxwEvJIHUkgc_B3SkE"
                 , "CAACAgIAAxkBAAEFNeZixq7TKNMbZY6VHdndgHSvZM6RegACEhEAAj9w8Uo66W_N-9GmTykE")

# Когда наступает конец записи от Пользователя
endtuple = ('конец', 'rjytw', 'клнец', 'end', 'rjy', 'rjytw')
startbool = False
# choicekindrecord по умолчанию True - это значит запись дела + запись времени для этого дела
choicekindrecord = True
timeuser =''
# user's chance (today or tommorow).True-today, False-tommorow
choiceday=False
# Разнообразие от бота
# """Элементы zapis берутся в том случае, когда пользователь вводит свои дела(Тем самым бот с ним взаимодействует.)  """
zapis = (
    'так-так', 'Я записываю', 'Надеюсь это всё)Я шучу', 'Хорошо', 'Записал', 'Принял', 'Я запомнил', 'Так-с',
    'yes, sir',
    'Ого', 'Хорошое дело', 'Да ужжжжж', 'Вот те на', 'Интересненько', 'Прикольно')

"""Элементы endzapis берутся в том случае, когда пользователь закончил писать свои дела."""
endzapis = ('А ты хорош.', 'Вот это да!Наполеоновские планы у тебя. Так держать!', 'Хороший план!Так держать!',
            'Удачи тебе в выполнении!',
            'Не важно, какое у тебя настроение.\nСделай по максимуму из того, что запланировал,',
            ' и ты будешь гордиться собой.', '"Создай шедевр из сегодня".\n-Джон Вуден.\n'
            , 'Бдестящий у тебя план на день!\nСделай его по красоте.')


# Проверка на строку
def checkstr(string):
    return isinstance(string, str)


@bot.message_handler(commands=["/start"])
def start(m):
    global startbool
    startbool = True
    choicekindrecord = True
    chektime = False

    bot.send_message(m.chat.id, f'Привет, {m.chat.first_name} {m.chat.last_name}.\n'
                                f'Я бот-планировщик, если ты вдруг забыл(а).\n'
                                f'Можешь записать в меня список своих дел.')

    # TODO: 2-Программа должна спращивать сколько времени сейчас у пользователя +
    # TODO: 3-+ функцию которая проверяет: Если пользователь зарегистрирован(доб в бд), то не спрашивать, а просто отправ
    # ему его часовой пояс и снизу прикрепить кнопку изменения настроек.
    # TODO: 4-add change language beta (пока не нуждаюсь ) +
    # TODO: 1-Добавить выбор: вывести просто список дел в определённое время или каждое дело распределять по времени +
    # TODO: 5-Проработать удаление записи в бд
    # TODO: 6-Проработать изменение записи в бд
    # TODO: 8-Добавление записи в бд
    bot.send_sticker(m.chat.id, tupleidwithhi[random.randint(0, len(tupleidwithhi) - 1)])
    choice_how_record(m)

bot.dispatcher.add_handler(MessageHandler(Filters.text=="/start", start))

@bot.message_handler()
def user_message(message):
    if not (startbool):
        start(message)
    if checkstr(message.text):
        if message.text == "/start":
            start(message)
            return
        if message.text == "Сегодня 📖" or message.text == "Завтра 🕘":
            bot.send_message(message.chat.id, '🌵Супер.')
            listwithhistory.append(message.text)
            # TODO: здесь было удаление кнопки
            mes = bot.send_message(message.from_user.id, "Напиши построчно список дел (одно дело = одна строка):")
        else:
            mes = bot.send_message(message.chat.id, zapis[random.randint(0, len(zapis) - 1)])
        bot.register_next_step_handler(mes, userobrab)
    else:
        bot.send_message(message.chat.id, "Ошибка в ведённой вами строке!\nПроверьте, что вы ввели строку.")


# Функция, которая проверяет время
def chektimefunc(message):

    global chektime
    chektime = False
    timetemp = message.text
    timenow=datetime.now().strftime("%H/%M")

    if (len(timetemp) <= 5):
        if (timetemp[1:2] == "/" or timetemp[2:3] == "/"):
            if len(timetemp) == 4:
                if (int(timetemp[:1]) < 24 and int(timetemp[3:5]) < 60):
                    chektime = True
            else:
                if (int(timetemp[:2]) < 24 and int(timetemp[3:5]) < 60):
                    chektime = True
    thechoicedayuser(message)


# """Даёт пользователю две кнопки.(запись с времен/ без времени )"""
def choice_how_record(m):
    markup = types.InlineKeyboardMarkup()
    # TODO: Здесь не оч нравится как написан текст, нужно более красиво и понятно написать.
    text = "Выберете, пожалуйста, в какой форме вы бы хотели работать.\n" \
           "1. Распределить каждое дело по времени.\n" \
           "2. Вывести список дел в определённое время."
    item_with_time = types.InlineKeyboardButton(text="Хочу по времени.", callback_data='withtime')
    item_without_time = types.InlineKeyboardButton(text="Хочу списоком.", callback_data='notime')

    markup.add(item_with_time, item_without_time)
    bot.send_message(m.chat.id, text, reply_markup=markup)


# потом переходим в эту функцию и работаем здесь
@bot.callback_query_handler(func=lambda call: True)
# """Взаимодействие с функцие choice_how_record. Ниже представлен декоратор."""
def answerontimerecordandchoiceday(call):
    global choicekindrecord
    if call.data == "notime":
        choicekindrecord = False
    time = bot.send_message(call.message.chat.id, 'Круто👍Осталось совсем чуть-чуть.\n'
                                                  '\nНапишите, пожалуйста, сколько сейчас у вас времени.В формате HH/MM\n\n(кол-во часов/кол-во минут)\n(Пример: 8/01 или 11/19).')
    bot.register_next_step_handler(time, chektimefunc)


def thechoicedayuser(message):
    global timeuser
    if chektime:
        timeuser = message.text
        menumain = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        itemmaintoday = types.KeyboardButton('Сегодня 📖')
        itemmaintommorow = types.KeyboardButton('Завтра 🕘')
        menumain.add(itemmaintoday, itemmaintommorow)
        temm = bot.send_message(message.chat.id, "Выбери, на какой из дней, ты хочешь запланировать дела.",
                                reply_markup=menumain)
        bot.register_next_step_handler(temm, user_message)
    else:
        mes = bot.send_message(message.chat.id,
                               'Вы ввели время не в верном формате!\nВведите ещё раз, пожалуйста\n(кол-во часов/кол-во минут)')
        bot.register_next_step_handler(mes, chektimefunc)




def userobrabtime(message):
    listwithtime.append(message.text)
    mess = bot.send_message(message.chat.id, 'Хорошо! Записал.\nДавай следующее дело.')
    bot.register_next_step_handler(mess, userobrab)


# handler records
def userobrab(mesg):
    if checkstr(mesg.text):
        if not (mesg.text.lower() in endtuple):
            listwithhistory.append(mesg.text)
            if choicekindrecord:
                time = bot.send_message(mesg.chat.id, 'Напишите время(во сколько дело)')
                bot.register_next_step_handler(time, userobrabtime)
            else:
                user_message(mesg)
        else:
            bot.send_message(mesg.chat.id, 'Принято.\nЗапись окончена!')
            printhistory(mesg)
    else:
        bot.send_message(mesg.chat.id, 'Ошибка! Вы отправили не строку.')


def printhistory(re):
    if listwithhistory[0] == "Сегодня 📖":
        bot.send_message(re.chat.id, 'Список сегодняшних дел:')
    else:
        bot.send_message(re.chat.id, 'Ваши дела на завтра:')
    # Объединение текста в одно сообщение, + добавляем номера к каждому делу
    textmain = ''
    for el in range(1, len(listwithhistory)):
        textmain += f"{el})" + listwithhistory[el] + '\n'
    if len(listwithhistory) != 0:
        if not (choicekindrecord):
            mes = bot.send_message(re.chat.id,
                                   'Во сколько бы вы хотели, чтобы я отправил вам сообщение\n с вашими делами.')
            bot.register_next_step_handler(mes, )
        else:
            bot.send_message(re.chat.id, f" {textmain}")
            bot.send_sticker(re.chat.id, 'CAACAgIAAxkBAAEFRrVi0DdErwLlhVDmuUeTdGT-Ld0khQAC2w8AAjs_SUvTm6YwUBI-OCkE')
    else:
        bot.send_message(re.chat.id, "Список ваших дел пока пуст!")


if __name__ == "__main__":
    bot.polling()
