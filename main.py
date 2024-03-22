import asyncio
import logging
import config
from handlers import bot, dp, router, scheduled

async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()  
    main_task = loop.create_task(main())
    loop.create_task(scheduled())
    loop.run_until_complete(main_task)
