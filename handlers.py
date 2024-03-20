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
import os
import sys

router = Router()
BD = bd.BDRequests()
RUNNING = True
STAT = False

#Функия для запуска парсинга с проверкой по времени
async def run_bot(msg: Message):
    now = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    all_week_days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    current_day = now.weekday()

    if all_week_days[current_day] in config.WORK_DAYS:
        current_time = now.strftime("%H:%M")
        print(current_time)
        if config.WORK_START_TIME <= current_time <= config.WORK_END_RIME:
            #Если включен параметр work_time сравниваем с текущим временем иначе просто запускаем
            if config.WORK_TIME != "off":
                if current_time in config.WORK_TIME:
                    await start_handler()
                    return
            #Запускаем парсинг только в случае периодического запуска
            if config.WORK_PERIOD != "off":
                await start_handler(msg)

#Бесконечный цикл с запуском функции парсинга каждую минуту либо через определенный период
async def scheduled(msg: Message):
    while True:
        await run_bot(msg)
        if config.WORK_PERIOD != "off":
            await asyncio.sleep(int(config.WORK_PERIOD)*60)
        else:
            await asyncio.sleep(60)

#Ограничение доступа пользователям, которых нет в списке
@router.message(lambda message:str(message.from_user.id) not in config.ADMINS)
async def check_user_id(msg: Message):
    await msg.answer("Нет доступа")
    return

#Функция парсинга запускается командой post либо по расписанию функцией run_bot
@router.message(Command("post"))
async def start_handler(msg: Message):
    global STAT
    if STAT:
        await msg.answer("Начат обход ссылок")
    #Переменная для остановки
    global RUNNING
    RUNNING = True
    #Обработка всех ссылок в конфиге
    for url in config.URL:
        #Получение ссылок из категории
        soup = parser_module.get_content(url)
        URLS = parser_module.get_href(soup)
        for URL in URLS:
            if not RUNNING:
                return 
            #Отсев дублей
            if BD.check_url_exist(URL):
                continue
            #Получение текста
            text = parser_module.get_page(URL)
            BD.insert_url(URL)
            try:
                #Отправка в канал
                channels_id = config.CHANELLS_ID
                for channel in channels_id:
                    await msg.bot.send_message(text=text, parse_mode='html', chat_id=channel)
            #В случае превышения лимита телеграма подождать указаное время
            except TelegramRetryAfter as e:
                sleep(e.retry_after)
                channels_id = config.CHANELLS_ID
                for channel in channels_id:
                    await msg.bot.send_message(text=text, parse_mode='html', chat_id=channel)
        if STAT:            
            await msg.answer("Все ссылки проверены")
        

#Запуск бота и вход в режим бесконечного цикла
@router.message(Command("start"))
async def cmd_start(msg: Message):
    global RUNNING
    RUNNING = True
    #Добавление кнопок
    kb = [
        [types.KeyboardButton(text='/post', callback_data='post'),
        types.KeyboardButton(text='/clean_bd', callback_data='clean_bd')],
        [types.KeyboardButton(text='/restart', callback_data='restart'),
        types.KeyboardButton(text='/stop', callback_data='stop')]
        [types.KeyboardButton(text='/stats', callback_data='stats')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await msg.answer("Бот запущен\nКоманды:\n/post - Единоразовый запуск парсера\n/clean_bd - Очистка базы данных с посещенными ссылками\n/restart - Перезапуск всего бота\n/stop - Остановка функции парсинга\n/stats - Включить\отключить отчетность", reply_markup=keyboard)
    await scheduled(msg)
    
#Очистка базы данных с ссылками
@router.message(Command("clean_bd"))
async def clear_database(msg: Message):
    BD.clear_database()
    await msg.answer("База данных очищена")

#Остановка функции парсинга
@router.message(Command("stop"))
async def process_callback_stop(msg: Message):
    global RUNNING
    RUNNING = False
    await msg.answer("Обход остановлен")

#Остановка функции парсинга
@router.message(Command("stats"))
async def process_callback_stop(msg: Message):
    global STAT
    if STAT:
        STAT = False
        await msg.answer("Статистика выключена")
    else:
        STAT = False
        await msg.answer("Статистика включена")

#Перезапуск бота
@router.message(Command("restart"))
async def restart(msg: Message):
    await msg.answer("Перезапуск бота...\n Для запуска функционала нажмите /start")
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
