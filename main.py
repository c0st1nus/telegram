from database import *
import datetime
from config import *
import telebot

class Wish:
    def __init__(self, category, name='', description='', author='', is_active=True, is_answered=False, data=datetime.datetime.now()):
        self.name = name
        self.category = category
        self.description = description
        self.author = author
        self.is_active = is_active
        self.is_answered = is_answered
        self.data = data

    def __str__(self):
        return "Wish(description = {}, author = {}, data of publication = {})".format(self.author, self.is_active, self.data)

    def description(self):
        return self.description

    def author(self):
        return self.author

    def is_active(self):
        return self.is_active

    def data(self):
        return self.data

    def change_name(self, name):
        self.name = name

    def change_description(self, description):
        self.description = description

class User:
    def __init__(self, id=0, name='', wishes=[]):
        self.id = id
        self.name = name
        self.wishes = wishes

    def __str__(self):
        return "User(id = {}, name = {}, wishes = {})".format(self.id, self.name, self.wishes)

    def wishes(self):
        return self.wishes

    def add_wish(self, wish):
        self.wishes.append(wish)

    def remove_wish(self, wish):
        self.wishes.remove(wish)


bot = telebot.TeleBot(token)
global i

@bot.message_handler(commands=['start'])
def start(message):
    create_table('wishes', 'id SERIAL PRIMARY KEY auto_increment, category VARCHAR(255), name VARCHAR(255), description VARCHAR(255), author VARCHAR(255), is_active BOOLEAN, data DATETIME')
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Исполнить желание', 'Опубликовать желание')
    keyboard.row('Мои желания')
    bot.send_message(message.chat.id,
                     'Привет!\nМы - команда "Твой Алладин", приложение, готовое превратить ваши желания в реальность!\nДля начала определитесь, обращаетесь ли вы к нам как к исполнителю желаний или как Аладин (исполнитель желаний).\nВы также можете опубликовать своё желание или исполнить чужое. Просто нажмите соответствующую кнопку:\n- "Опубликовать желание"\n- "Исполнить желание\nАвтор - https://t.me/+77770222644"',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message, second_step)

def second_step(message):
    if message.text == 'Опубликовать желание':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row('Бар/ресторан/кафе', 'Развлечения', 'Активный отдых')
        bot.send_message(message.chat.id, 'Выбери категорию', reply_markup=keyboard)
        bot.register_next_step_handler(message, create_wish)
    if message.text == 'Исполнить желание':
        global i
        i = 0
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row('Бар/ресторан/кафе', 'Развлечения')
        keyboard.row('Активный отдых', 'Все желания')
        bot.send_message(message.chat.id, 'Выбери категорию', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_wish)
    if message.text == 'Мои желания':
        wishes = select('wishes', '*', f'author = "{message.from_user.id}"')
        if len(wishes) == 0:
            bot.send_message(message.chat.id, 'У вас нет желаний')
            start(message)
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            for wish in wishes:
                keyboard.row(wish["name"])
            bot.send_message(message.chat.id, 'Выбери желание', reply_markup=keyboard)
            bot.register_next_step_handler(message, get_my_wish)
def get_my_wish(message):
    wish = select('wishes', '*', f'name = "{message.text}"')
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Изменить название', 'Изменить описание')
    keyboard.row('Удалить желание', 'Выйти')
    bot.send_message(message.chat.id, text=wish[0]["name"] + '\n' + wish[0]["description"], reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_my_wish, wish)

def handle_my_wish(message, wish):
    if message.text == 'Изменить название':
        bot.send_message(message.chat.id, 'Напиши новое название')
        bot.register_next_step_handler(message, change_name, wish[0])
    elif message.text == 'Изменить описание':
        bot.send_message(message.chat.id, 'Напиши новое описание')
        bot.register_next_step_handler(message, change_description, wish[0])
    elif message.text == 'Удалить желание':
        delete('wishes', f'name = "{wish[0]["name"]}"')
        bot.send_message(message.chat.id, 'Желание удалено')
        start(message)
    elif message.text == 'Выйти':
        start(message)

def change_name(message, wish):
    update('wishes', f'name = "{message.text}"', f'id = {wish["id"]}')
    bot.send_message(message.chat.id, 'Название изменено')
    start(message)

def change_description(message, wish):
    wish.change_description(message.text)
    update('wishes', f'description = "{wish.description}"', f'id = {wish["id"]}')
    bot.send_message(message.chat.id, 'Описание изменено')
    start(message)
def get_wish(message):
    if message.text == 'Бар/ресторан/кафе':
        bot.send_message(message.chat.id,
                         'Нажми "➡️" для перехода следующему желанию, "⬅️" к предыдущему, "✅" для выбора желания')
        cafes(message)
    elif message.text == 'Развлечения':
        bot.send_message(message.chat.id,
                         'Нажми "➡️" для перехода следующему желанию, "⬅️" к предыдущему, "✅" для выбора желания')
        entertainment(message)
    elif message.text == 'Активный отдых':
        bot.send_message(message.chat.id,
                         'Нажми "➡️" для перехода следующему желанию, "⬅️" к предыдущему, "✅" для выбора желания')
        active(message)
    elif message.text == 'Все желания':
        bot.send_message(message.chat.id,
                         'Нажми "➡️" для перехода следующему желанию, "⬅️" к предыдущему, "✅" для выбора желания')
        all_wishes(message)
    elif message.text == 'Выйти':
        start(message)

def cafes(message):
    wishes = select('wishes', '*', f'category = "Бар/ресторан/кафе"')
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('⬅️', '✅', '➡️')
    text = wishes[i]["name"] + '\n' + wishes[i]["description"]
    bot.send_message(message.chat.id, text, reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_button_press, 0, wishes)

def entertainment(message):
    wishes = select('wishes', '*', f'category = "Развлечения"')
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('⬅️', '✅', '➡️')
    text = wishes[i]["name"] + '\n' + wishes[i]["description"]
    bot.send_message(message.chat.id, text, reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_button_press, 1, wishes)

def active(message):
    wishes = select('wishes', '*', f'category = "Активный отдых"')
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('⬅️', '✅', '➡️')
    text = wishes[i]["name"] + '\n' + wishes[i]["description"]
    bot.send_message(message.chat.id, text, reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_button_press, 2, wishes)

def all_wishes(message):
    wishes = select_all('wishes')
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('⬅️', '✅', '➡️')
    text = wishes[i]["name"] + '\n' + wishes[i]["description"]
    bot.send_message(message.chat.id, text, reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_button_press, 3, wishes)

def handle_button_press(message, type, ListOfWishes):
    global i
    if message.text != '✅':
        if message.text == '➡️':
            if i == len(ListOfWishes) - 1:
                i = 0
            else:
                i += 1
        elif message.text == '⬅️':
            if i == 1:
                i = len(ListOfWishes) - 1
            else:
                i -= 1
        if type == 0:
            cafes(message)
        elif type == 1:
            entertainment(message)
        elif type == 2:
            active(message)
        elif type == 3:
            all_wishes(message)
    elif message.text == '✅':
        i = 0
        bot.send_message(message.chat.id, f'@{ListOfWishes[i]["author"]} - автор оповещен, ждите от него сообщения или напишите ему/ей сам(а). Удачного отдыха!')
        bot.send_message(ListOfWishes[i]["author"], f'Ваше желание "{ListOfWishes[i]["name"]}" было выбрано. Свяжитесь с исполнителем по ссылке - @{message.from_user.username}')
        start(message)

def create_wish(message):
    keyboard = telebot.types.ReplyKeyboardRemove()
    wish = Wish(category=message.text, author=message.from_user.id, data=datetime.datetime.now())
    bot.send_message(message.chat.id, 'Напиши заголовок для своего желания', reply_markup=keyboard)
    bot.register_next_step_handler(message, create_wish_name, wish)

def create_wish_name(message, wish):
    wish.change_name(message.text)
    bot.send_message(message.chat.id, 'Опиши своё желание')
    bot.register_next_step_handler(message, create_wish_description, wish)

def create_wish_description(message, wish):
    wish.change_description(message.text)
    print(wish.description)
    insert('wishes', 'category, name, description, author, is_active, data', f"'{wish.category}', '{wish.name}', '{wish.description}', '{wish.author}', {True}, '{wish.data}'")
    bot.send_message(message.chat.id, 'Желание успешно опубликовано')
    start(message)

bot.polling(none_stop=True)
