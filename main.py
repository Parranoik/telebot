from aiogram import Bot, Dispatcher, F  #Dispatceh - managing(handling and priority), F - content filters(Now not usable)
from aiogram.filters import Command     #Command - filtrating '/'-commands
from aiogram.types import (Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove)

import os  #support for dotenv lib and for save_inf func
from dotenv import load_dotenv, find_dotenv  #for virtual enviroment secret tokenholder-file
import random

load_dotenv(find_dotenv()) #подгружает данные из .env в программу (через поиск по корневому каталогу)

API_TOKEN: str = os.getenv('BOT_TOKEN') #os.getenv('BOT_TOKEN') //нужный нам ключ - токен бота

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

button0: KeyboardButton = KeyboardButton(text='start')
button01: KeyboardButton = KeyboardButton(text='help')
button1: KeyboardButton = KeyboardButton(text='menu')
button2: KeyboardButton = KeyboardButton(text='game')
button3: KeyboardButton = KeyboardButton(text='Повторяйка')
button21: KeyboardButton = KeyboardButton(text='')


keyboard_start: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button1]])
keyboard_menu: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button2, button3]], resize_keyboard=True, one_time_keyboard=True)
keyboard_game_menu: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button1]], resize_keyboard=True, one_time_keyboard=True)

def save_inf(message: Message):     #loging to file
    user_p = str(message.from_user.id)
    current_path = os.getcwd()

    if user_p not in os.listdir(current_path +'\logs'):  #check for not doubling folder
        os.mkdir(current_path + '\logs\\' + user_p)     #creating dirrectory into actual user folders
    actual_path = current_path + '\logs\\' + user_p + '\\'  #path with actual user
    path: str = actual_path + str(message.from_user.id) + '.json'   #message.from_user.id <-> message.chat.id

    with open(path, 'a', encoding='utf-8', newline='\n') as log:    #this variant saves logs into main catalog
        log.write(message.model_dump_json(indent=4, exclude_none=True))
        log.write('\n#\n')  #separating char for easy-reaing log

users: dict = {}


def get_random_number() -> int:
    return random.randint(1, 100)

ATTEMPTS: int = 5 #КОЛИЧЕСТВО ПОПЫТОК

@dp.message(Command(commands=['start'], ignore_case=True))
async def process_start_command(message: Message):
    await message.sendmessage('', reply_markup=ReplyKeyboardRemove())
    await message.answer('Игровой бот', reply_markup=keyboard_start)
    if message.from_user.id not in users:
        users[message.from_user.id] = {'user': message.from_user.id,
                                       'menu': 'menu', #menu logic:start -> menu -> [game, echo, translation]
                                       'game': {'in_game': False,
                                       'attempts': None,
                                       'wining_number': None,
                                       'current_nums': [],
                                       'total_games': 0,
                                       'wins': 1}}

    #print(type(users[616544593]['game']))
    #print(type(users))
    #print(users[616544593]['game'])

@dp.message(Command(commands=['menu']))
async def main_menu(message: Message):
    await message.answer(text='Это главное меню, куда дальше?', reply_markup=keyboard_game_menu)
    users[message.from_user_id]['menu'] = 'menu'

@dp.message(Command(commands=['game']))
async def game_menu(message: Message):
    await message.answer(text='Это меню игры: Выбери играть или вернуться в меню', reply_markup=keyboard_menu)
    users[message.from_user.id]['menu'] = 'game'
@dp.message(Command(commands=['help'], ignore_case=True))
async def process_help_command(message: Message):
    await message.answer('Игра угадай число от 1 до 100.'
                         f'у вас {ATTEMPTS} попыток.'
                         'Доступные команды \game чтобы начать'
                         '\cancel чтобы перестать играть'
                         '\stat статистика за всё время')

@dp.message(Command(commands=['cancel'], ignore_case=True))
async def process_cancel_game(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer('Вы вышли из игры. Сыграете ещё?')
    else:
        await message.answer('Вы и так не играете. Может сыграем?')

@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра', 'играть', 'хочу', '/s']))
async def process_agreeing(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['attempts'] = ATTEMPTS
        users[message.from_user.id]['winning_number'] = get_random_number()
        await message.answer('Я загадал число от 1 до 100, попробуй угадать')
    else:
        await message.answer('Игра уже идёт. На вход принимаются только числа от 1 до 100')

@dp.message(F.text.lower().in_(['нет', 'не хочу', 'не', 'отказ']))
async def process_rejecting(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Жаль, если захотите сыграть - напишите об этом')
    else:
        await message.answer('Игра идёт. На вход принимаются числа от отного до 100. для отмены игры напишите /cancel')


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def game_start(message: Message):
    await message.answer('УРА')
    pass



'''
ЭХО ФУНКЦИОНАЛ
@dp.message(Command(commands=['start', 'strat', 'strt', 'satrt'], ignore_case=True))
async def process_start_command(message: Message):
    await message.answer('Привет!\nТестовый-бот!\n')
    save_inf(message)

@dp.message(Command(commands=['info', 'inf', 'ifno', 'help', 'hlp', 'hlep'], ignore_case=True))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ я пришлю тебе твое сообщение')
    save_inf(message)

@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
        save_inf(message)
    except TypeError:
        await message.reply(text='Данный апдейт не поддерживается методом send_copy')
        
'''

if __name__ == '__main__':
    dp.run_polling(bot)
