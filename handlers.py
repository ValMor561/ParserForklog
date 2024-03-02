from aiogram import types, F, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramRetryAfter
import asyncio
import parser_module
import config
import bd
from time import sleep
import datetime
import pytz
import schedule

router = Router()
BD = bd.BDRequests()
RUNNING = True

async def check_schedule(chat_id):
    now = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    current_day = now.strftime("%A").lower()

    if current_day in config.WORK_DAYS:
        current_time = now.strftime("%H:%M")
        if config.WORK_START_TIME <= current_time <= config.WORK_END_RIME:
            if  current_time in config.WORK_TIME:
                await start_handler()
            elif config.WORK_PERIOD != "off" and now.minute % config.WORK_PERIOD == 0:
                await start_handler()

@router.message()
async def check_user_id(msg: Message):
    if str(msg.from_user.id) not in config.ADMINS:
        await msg.answer("Нет доступа")
        return


@router.message(Command("post"))
async def start_handler(msg: Message):
    global RUNNING
    RUNNING = True
    for url in config.URL:
        soup = parser_module.get_content(url)
        URLS = parser_module.get_href(soup)
        for URL in URLS:
            if not RUNNING:
                return 
            if BD.check_url_exist(URL):
                continue
            text = parser_module.get_page(URL)
            BD.insert_url(URL)
            try:
                await msg.bot.send_message(text=text, parse_mode='html', chat_id=config.CHANELL_ID)
            except TelegramRetryAfter as e:
                sleep(e.retry_after)
                await msg.bot.send_message(text=text, parse_mode='html', chat_id=config.CHANELL_ID)

@router.message(Command("start"))
async def cmd_start(msg: Message):
    global RUNNING
    RUNNING = True
    kb = [
        [types.KeyboardButton(text='/post', callback_data='post'),
        types.KeyboardButton(text='/clean_bd', callback_data='clean_bd')],
        [types.KeyboardButton(text='/restart', callback_data='restart'),
        types.KeyboardButton(text='/stop', callback_data='stop')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await msg.answer("Бот запущен", reply_markup=keyboard)

@router.message(Command("clean_bd"))
async def clear_database(msg: Message):
    BD.clear_database()
    await msg.answer("База данных очищена")

@router.message(Command("stop"))
async def process_callback_stop(callback_query: types.CallbackQuery):
    global RUNNING
    RUNNING = False



    
