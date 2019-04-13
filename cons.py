import telebot
from telebot import types
import sqlite3
import pyrebase
config = {
    "apiKey": "AIzaSyBW8sALdhQZBdx1imWvqtK1NLDizNtpwB0",
    "authDomain": "clubevents-6d507.firebaseapp.com",
    "databaseURL": "https://clubevents-6d507.firebaseio.com",
    "projectId": "clubevents-6d507",
    "storageBucket": "clubevents-6d507.appspot.com",
    "messagingSenderId": "328916169448"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
bot = telebot.TeleBot("877386826:AAE4HsHNABanR9tTWniRREutzIqovgaWFdI")

user_db = {}
tags = {"1": "sport", "2": "concert", "3": "case competition", "4": "seniort talk",
    "5": "finance", "6": "acm", "7": "guest lecture", "8": "forum", "9": "master's application", "10": "company days"
}

@bot.message_handler(commands=['start', 'help'])
def start_function(message):
    id = str(message.from_user.id)
    bot.send_message(message.from_user.id, "Welcome to my Club Events bot!")
    if id in user_db:
        if user_db[id]['login']:
            markup = types.ReplyKeyboardMarkup(True, True)
            markup.row('Yes', 'No')
            bot.send_message(message.from_user.id, "Welcome to my Club Events bot!\nWhould you like to send new message?\n",reply_markup=markup)
            bot.register_next_step_handler(message, start_post)
        else:
            bot.send_message(message.from_user.id, "Welcome to my Club Events bot!\nPlease sign in first\n/login /cancel")
    else:
        bot.send_message(message.from_user.id, "Welcome to my Club Events bot!\nPlease sign in first\n/login /cancel")



@bot.message_handler(commands=['end', 'cancel'])
def end_function(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    id = str(message.from_user.id)
    if id in user_db:
        del user_db[id]
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "Good buy!", reply_markup=hide_markup)
    
@bot.message_handler(commands=['login'])
def sign_in(message):
    bot.send_message(message.from_user.id, "Write your email")
    bot.register_next_step_handler(message, get_password)

def get_password(message):
    id = str(message.from_user.id)
    user_db[id] = {'email': message.text}
    bot.send_message(message.from_user.id, "Write your password")
    bot.register_next_step_handler(message, handle_login)

def handle_login(message):
    id = str(message.from_user.id)
    try:
        user_db[id]['creds'] = auth.sign_in_with_email_and_password(user_db[id]['email'], message.text)
        user_db[id]['login'] = True
        markup = types.ReplyKeyboardMarkup(True, True)
        markup.row('Yes', 'No')
        bot.send_message(message.from_user.id, "Welcome to my Club Events bot!\nWhould you like to send new message?\n",reply_markup=markup)
        bot.register_next_step_handler(message, start_post)
    except:
        bot.send_message(message.from_user.id, "Login or password is incorrect. Try /login again")

def start_post(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    if message.text == 'Yes':
        bot.send_message(message.from_user.id, "Please enter a title", reply_markup=hide_markup)
        bot.register_next_step_handler(message, get_title)
    else:
        end_function(message)

def get_title(message):
    id = str(message.from_user.id)
    user_db[id]['post'] = {'title': message.text}
    bot.send_message(message.from_user.id, "Please enter a description")
    bot.register_next_step_handler(message, get_des)

def get_des(message):
    id = str(message.from_user.id)
    user_db[id]['post']['text'] = message.text
    tag = ""
    for k,v in tags.items():
        tag += str(k) + ": " + str(v) + "\n"
    bot.send_message(message.from_user.id, "Please choose tags, enter them using space\n" + tag)
    bot.register_next_step_handler(message, handle_post)

def handle_post(message):
    tmp = message.text.split()
    id = str(message.from_user.id)
    user_db[id]['post']['tags'] = [] 
    for k in tmp:
        try:
            user_db[id]['post']['tags'].append(tags[k])
        except:
            continue
    rep = ""
    for k,v in user_db[id]['post'].items():
        rep += str(k) + ": " + str(v) + "\n"
    
    db.child("users").child(user_db[id]['post'])
    bot.send_message(message.from_user.id, rep +'\n\n\n' + "This is your post. Would you like to /edit it or /end session")

@bot.message_handler(commands= ['edit'])
def select_post(message):
    all_users = db.child("users").get()
    for user in all_users.each():
        print(user.key()) # Morty
        print(user.val())

bot.polling(none_stop=True)
