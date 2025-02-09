from sovet import sovets
import os
import random
import telebot
from model import get_class
token='TOKEN'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_bye(message):
    bot.reply_to(message, "Привет! Тут я расскажу про загрязнение окружающей среды и дам тебе советов которые помогут сохранить природу.Напаиши /Help чтоюы увидеть список команд")
    
@bot.message_handler(commands=['Help'])
def send_bye(message):
    bot.reply_to(message,
                 '''1./sovet:эта команда даст тебе рандомный совет что надо делать с твоим мусором \n 
2./itog:эта команда пришлет тебе фото последствий не правильного обращения с мусором
3./bye:ты прощаещся с ботом
                ''')
    
@bot.message_handler(commands=['sovet'])
def send_welcome(message):
    bot.reply_to(message, random.choice(sovets))
    
@bot.message_handler(commands=['itog'])
def send_mem(message):
    image_name=random.choice(os.listdir('images_sreda'))

    with open(f'images_sreda/{image_name}', 'rb') as f:  
        bot.send_photo(message.chat.id, f)
    
@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "пока")
    
@bot.message_handler(content_types=['photo'])
def send_photo(message):
    if not message.photo:
        return bot.send_message(message.chat.id,"Ты свин,загрузи фото")
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1] 
    downloaded_file = bot.download_file(file_info.file_path) 
    with open(file_name, 'wb') as new_file: 
        new_file.write(downloaded_file)
    bot.send_message(message.chat.id,"Молодец,идет обработка")
    result = get_class("keras_model.h5","labels.txt",file_name)
    bot.send_message(message.chat.id,result)
    
#последняя функция
print('бот запущен') 
bot.polling()
