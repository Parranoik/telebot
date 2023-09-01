'''
import telebot


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я переводчик на основе ChatGPT')

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

def hello(message):
    bot.send_message(message.chat.id, 'Привет, {name}. Рад тебя видеть.'.format(name=message.text))

bot.infinity_polling()
'''

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message


import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) #подгружает данные из .env в программу (через поиск по корневому каталогу)


API_TOKEN: str = os.getenv('BOT_TOKEN') #os.getenv('BOT_TOKEN') //нужный нам ключ - токен бота

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')
    print(message) #отладка
    print(message.date)  #отладка
    print(message.chat.username) #отладка

# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение')
    print(message.text) #отладка
    print(message.date) #отладка
    print(message.chat.username) #отладка


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)
    print(message) #отладка
    print(message.date) #отладка
    print(message.chat.username) #отладка

if __name__ == '__main__':
    dp.run_polling(bot)
