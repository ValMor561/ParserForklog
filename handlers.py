from aiogram import types,  Router, Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramRetryAfter
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio
import parser_module
import config
import bd
from time import sleep
import datetime
import pytz
import os
import sys

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
BD = bd.BDRequests()
RUNNING = True

#Функия для запуска парсинга с проверкой по времени
async def run_bot():
    now = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    all_week_days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    current_day = now.weekday()

    if all_week_days[current_day] in config.WORK_DAYS:
        current_time = now.strftime("%H:%M")
        if config.WORK_START_TIME <= current_time <= config.WORK_END_RIME:
            #Если включен параметр work_time сравниваем с текущим временем иначе просто запускаем
            if config.WORK_TIME != "off":
                if current_time in config.WORK_TIME:
                    await check_urls()
                    return
            #Запускаем парсинг только в случае периодического запуска
            if config.WORK_PERIOD != "off":
                await check_urls()

#Бесконечный цикл с запуском функции парсинга каждую минуту либо через определенный период
async def scheduled():
    while True:
        await run_bot()
        if config.WORK_PERIOD != "off":
            await asyncio.sleep(int(config.WORK_PERIOD)*60)
        else:
            await asyncio.sleep(60)

def save_current_time_to_file():
    with open("/var/www/crypto/news_forklog/time.txt", 'w') as file:
        current_time = datetime.datetime.now().strftime("%H:%M:%S %Y-%m-%d")
        file.write(current_time)

#Ограничение доступа пользователям, которых нет в списке
@router.message(lambda message:str(message.from_user.id) not in config.ADMINS)
async def check_user_id(msg: Message):
    await msg.answer("Нет доступа")
    return

async def check_urls():
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
                return False
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
                    await bot.send_message(text=text, parse_mode='html', chat_id=channel)
            #В случае превышения лимита телеграма подождать указаное время
            except TelegramRetryAfter as e:
                sleep(e.retry_after)
                channels_id = config.CHANELLS_ID
                for channel in channels_id:
                    await bot.send_message(text=text, parse_mode='html', chat_id=channel)
            save_current_time_to_file()
        return True
    
#Функция парсинга запускается командой post либо по расписанию функцией run_bot
@router.message(Command("post"))
async def start_handler(msg: Message):
    await msg.answer("Начат обход ссылок")
    if await check_urls():
        await msg.answer("Все ссылки проверены")
        

#Запуск бота и вход в режим бесконечного цикла
@router.message(Command("start"))
async def cmd_start(msg: Message):
    global RUNNING
    RUNNING = True
    #Добавление кнопок
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='/post', callback_data='post'), types.KeyboardButton(text='/stop', callback_data='stop'))
    builder.row(types.KeyboardButton(text='/clean_bd', callback_data='clean_bd'), types.KeyboardButton(text='/restart', callback_data='restart'))
    builder.row(types.KeyboardButton(text='/stats', callback_data='stats'))

    keyboard = builder.as_markup(resize_keyboard=True)
    await msg.answer("Бот запущен\nКоманды:\n/post - Единоразовый запуск парсера\n/clean_bd - Очистка базы данных с посещенными ссылками\n/restart - Перезапуск всего бота\n/stop - Остановка функции парсинга\n/stats - Состояние бота", reply_markup=keyboard)

    
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

async def get_last_bot_message_time():
    res = "Время последнего сообщения: "
    with open("/var/www/crypto/news_forklog/time.txt", 'r') as file:
        time_str = file.read().strip()
        res += time_str + "\n"
    return res

#Текущее состояние
@router.message(Command("stats"))
async def process_callback_stop(msg: Message):
    news_time = parser_module.get_time()
    post_time = await get_last_bot_message_time()
    await msg.answer(f"Бот запущен:\n{post_time}{news_time}")

#Перезапуск бота
@router.message(Command("restart"))
async def restart(msg: Message):
    await msg.answer("Перезапуск бота...\n")
    python = sys.executable
    os.execl(python, python, *sys.argv)

