from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
import parser_module
import config

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    texts = parser_module.get_all()
    for text in texts:
        await msg.bot.send_message(text=text, parse_mode='html', chat_id=config.CHANELL_ID)
    


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")