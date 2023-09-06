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
import json
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message


import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) #подгружает данные из .env в программу (через поиск по корневому каталогу)


API_TOKEN: str = os.getenv('BOT_TOKEN') #os.getenv('BOT_TOKEN') //нужный нам ключ - токен бота

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

def save_inf(message: Message): #logging to file
    with open('log.json', 'a', encoding='utf-8', newline='\n') as log:
        log.write(message.model_dump_json(indent=4, exclude_none=True))

async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')

async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ я пришлю тебе твое сообщение')

async def send_echo_text(message: Message):
    await message.reply(text=message.text)
    save_inf(message)

async def send_echo_photo(message: Message):
    await message.reply_photo(message.photo[0].file_id)

async def send_echo_video(message: Message):
    await message.reply_video(message.video.file_id)


async def send_echo_sticker(message: Message):
    await message.reply_sticker(message.sticker.file_id)

async def send_echo_audio(message: Message):
    await message.reply_audio(message.audio.file_id)

async def send_echo_voice(message: Message):
    await message.reply_voice(message.voice.file_id)

async def send_echo_document(message: Message):
    await message.reply_document(message.document.file_id)






dp.message.register(process_start_command, Command(commands=['start', 'strat', 'strt', 'satrt'], ignore_case=True))
dp.message.register(process_help_command, Command(commands=['info', 'inf', 'ifno', 'help', 'hlp', 'hlep'], ignore_case=True))
dp.message.register(send_echo_photo, F.photo)
dp.message.register(send_echo_video, F.video)
dp.message.register(send_echo_audio, F.audio)
dp.message.register(send_echo_voice, F.voice)
dp.message.register(send_echo_sticker, F.sticker)
dp.message.register(send_echo_document, F.document)
dp.message.register(send_echo_text, F.text)
def fff(message: Message):
    print(message.model_dump_json(indent=4, exclude_none=True))

if __name__ == '__main__':
    dp.run_polling(bot)
