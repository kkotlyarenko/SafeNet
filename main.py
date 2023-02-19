import analyse
import telebot
import os
from telebot import types

bot = telebot.TeleBot('5849594357:AAFrSwFROSfIrmMQ46X_rwu6sPkpFea3OvI')


@bot.message_handler(commands=['start', 'help'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.chat.id,f'Привет! \nУстал от сомнительных ссылок в интернете?\nЯ знаю как тебе помочь!\nОтправь мне ссылку или QR-код, а я расскажу всё об этом сайте!)');

    else:
        bot.send_message(message.chat.id, "Отправь ссылку c http://  или QR-код")

@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if 'http' in message.text:
        bot.reply_to(message, analyse.checkURL(message.text))
    else:
        bot.reply_to(message, "Неверный формат ссылки. Напиши /help.")


@bot.message_handler(content_types=['photo'])
def get_photo_messages(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = 'C:/Users/kiril/Documents/DevHack/' + message.photo[1].file_id + '.png'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, analyse.checkQR(message.photo[1].file_id + '.png'))
    os.remove(message.photo[1].file_id + '.png')


bot.polling(none_stop=True, interval=0)


