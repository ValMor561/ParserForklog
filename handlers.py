from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramRetryAfter
import parser_module
import config
import bd
from time import sleep
from telegram.error import RetryAfter
import datetime
import pytz
import schedule

router = Router()
BD = bd.BDRequests()

# Функция для проверки, должен ли бот отправить текущее время в данный момент
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

@router.message(Command("post"))
async def start_handler(msg: Message):
    for url in config.URL:
        soup = parser_module.get_content(url)
        URLS = parser_module.get_href(soup)
    for URL in URLS:
        if BD.check_url_exist(URL):
            continue
        text = parser_module.get_page(URL)
        BD.insert_url(URL)
        try:
            await msg.bot.send_message(text=text, parse_mode='html', chat_id=config.CHANELL_ID)
        except TelegramRetryAfter as e:
            sleep(e.retry_after)
            await msg.bot.send_message(text=text, parse_mode='html', chat_id=config.CHANELL_ID)

@router.message(Command("clean_bd"))
async def clear_database(msg: Message):
    BD.clear_database()
    await msg.answer("База данных очищена")

@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")