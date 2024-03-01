from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
import parser_module

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(parser_module.get_all())
    print(parser_module.get_all())


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")