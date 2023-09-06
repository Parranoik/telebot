from aiogram import Bot, Dispatcher, F  #Dispatceh - managing(handling and priority), F - content filters(Now not usable)
from aiogram.filters import Command     #Command - filtrating '/'-commands
from aiogram.types import Message

import os  #support for dotenv lib and for save_inf func
from dotenv import load_dotenv, find_dotenv  #for virtual enviroment secret tokenholder-file

load_dotenv(find_dotenv()) #подгружает данные из .env в программу (через поиск по корневому каталогу)

API_TOKEN: str = os.getenv('BOT_TOKEN') #os.getenv('BOT_TOKEN') //нужный нам ключ - токен бота

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

def save_inf(message: Message):     #loging to file
    date_p = str(message.date)[:10]
    current_path = os.getcwd()

    if date_p not in os.listdir(current_path +'\logs'):  #check for not doubling folder
        os.mkdir(current_path + '\logs\\' + date_p)     #creating dirrectory into actual date folders
    actual_path = current_path + '\logs\\' + date_p + '\\'  #path with actual date
    path: str = actual_path + str(message.from_user.id) + '.json'   #message.from_user.id <-> message.chat.id

    with open(path, 'a', encoding='utf-8', newline='\n') as log:    #this variant saves logs into main catalog
        log.write(message.model_dump_json(indent=4, exclude_none=True))
        log.write('\n#\n')  #separating char for easy-reaing log

@dp.message(Command(commands=['start', 'strat', 'strt', 'satrt'], ignore_case=True))
async def process_start_command(message: Message):
    await message.answer('Привет!\nЭто Эхо-бот!\nНапиши мне что-нибудь')

@dp.message(Command(commands=['info', 'inf', 'ifno', 'help', 'hlp', 'hlep'], ignore_case=True))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ я пришлю тебе твое сообщение')

@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
        save_inf(message)
    except TypeError:
        await message.reply(text='Данный апдейт не поддерживается методом send_copy')

if __name__ == '__main__':
    dp.run_polling(bot)
