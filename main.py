import uvicorn
import asyncio
import logging
import sys
from fastapi import FastAPI
from apirouter import apirouter
from mainbotweather import telegramrouter, dp
from threading import Thread
from aiogram import Bot
from config import tg_bot_token
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


app = FastAPI()


app.include_router(apirouter, tags=["Api methods"])
app.include_router(telegramrouter, tags=["Telegram commands"])


def start_fast():
    uvicorn.run(app)
    
    
async def main():
    bot = Bot(token=tg_bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":    
    # Запускаем FastApi в отдельном потоке

    Thread(target=start_fast).start()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
