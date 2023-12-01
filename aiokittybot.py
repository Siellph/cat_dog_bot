import asyncio
import sys
import os
import logging
import emoji
import httpx
import random
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, URLInputFile
from aiogram.utils.markdown import hbold


load_dotenv()
TOKEN = os.getenv('TOKEN')
URL_CATS = 'https://api.thecatapi.com/v1/images/search'
URL_DOGS = 'https://api.thedogapi.com/v1/images/search'
CAT = emoji.emojize(':cat_face:')
DOG = emoji.emojize(':dog_face:')

dp = Dispatcher()


async def get_new_image(URL):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(URL)
            response.raise_for_status()  # Check for errors in the response
            data = response.json()
            image_url = data[0].get('url')
            return image_url
    except httpx.RequestError as error:
        logging.error(f'Error during API request: {error}')


async def nikolya(message):
    if message.from_user.id == 1330898313 and random.random() < 0.5:
        await message.answer('Ну Коль...')
        return True


@dp.message(F.text.lower() == f'котики{CAT}')
async def new_cat(message: Message) -> None:
    if await nikolya(message):
        return
    image_url = await get_new_image(URL_CATS)
    image = URLInputFile(image_url, filename='cat.png')
    await message.answer_photo(image)


@dp.message(F.text.lower() == f'собачки{DOG}')
async def new_dog(message: Message) -> None:
    if await nikolya(message):
        return
    image_url = await get_new_image(URL_DOGS)
    image = URLInputFile(image_url, filename='cat.png')
    await message.answer_photo(image)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    key = [
        types.KeyboardButton(text=f'Котики{CAT}'),
        types.KeyboardButton(text=f'Собачки{DOG}')
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=[key], resize_keyboard=True)
    await message.answer(
        f'Привет, {hbold(message.from_user.full_name)}{CAT}{DOG}',
        reply_markup=keyboard)


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
