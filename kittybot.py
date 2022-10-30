import logging
import os
import random

import emoji
import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater

load_dotenv()
secret_token = os.getenv('TOKEN')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
URL_CATS = 'https://api.thecatapi.com/v1/images/search'
URL_DOGS = 'https://api.thedogapi.com/v1/images/search'

MESSAGE_LIST_CATS = [
    'Посмотри, какого котика я тебе нашёл:smiling_cat_with_heart-eyes:',
    ':smiling_cat_with_heart-eyes::smiling_cat_with_heart-eyes:'
    ':smiling_cat_with_heart-eyes:',
    'Посмотри какая прелесть:smiling_cat_with_heart-eyes:',
    'Котиков много не бывает, мяу:cat:',
    'Котики, КОТИКИ, КО-ТИ-КИ:cat::cat::cat::cat::cat::cat::cat:',
    'Когда-нибудь котики захватят мир, мяу:cat_face:',
    ':cat::cat::cat:']

MESSAGE_LIST_DOGS = [
    'Посмотри, какую собачку я тебе нашёл:dog_face:',
    ':dog_face::dog_face::dog_face:',
    'Посмотри какая прелесть:dog_face:',
    'Woofff:dog:',
    ':dog::dog::dog:']


def get_new_image(URL):
    if URL == URL_CATS:
        try:
            response = requests.get(URL)
        except Exception as error:
            logging.error(f'Ошибка при запросе к API Cats: {error}')
            response = requests.get(URL_DOGS)
    if URL == URL_DOGS:
        try:
            response = requests.get(URL)
        except Exception as error:
            logging.error(f'Ошибка при запросе к API Dogs: {error}')
            response = requests.get(URL_CATS)

    response = response.json()
    random_img = response[0].get('url')
    return random_img


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=emoji.emojize(random.choice(MESSAGE_LIST_CATS)),
    )
    context.bot.send_photo(chat.id, get_new_image(URL_CATS))


def new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=emoji.emojize(random.choice(MESSAGE_LIST_DOGS)),
    )
    context.bot.send_photo(chat.id, get_new_image(URL_DOGS))


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(
        [
            [emoji.emojize('/newcat:cat:'),
             emoji.emojize('/newdog:dog:')]
        ],
        resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text=emoji.emojize('Привет, {}. Посмотри, какого котика я тебе нашёл'
                           ':smiling_cat_with_heart-eyes:'.format(name)),
        reply_markup=button
    )
    context.bot.send_photo(chat.id, get_new_image(URL_CATS))


def main():
    updater = Updater(secret_token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('newdog', new_dog))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
