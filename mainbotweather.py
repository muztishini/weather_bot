import asyncio
import logging
import sys
import requests
from datetime import datetime
from aiogram.client.default import DefaultBotProperties
from config import tg_bot_token, open_weather_token
from models import Log, SessionLocal
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold


dp = Dispatcher()
db = SessionLocal()


def add_base(userid, command, datatime, answer):
    log = Log(userid=userid, command=command, datatime=datatime, answer=answer)
    db.add(log)
    db.commit()
    db.refresh(log)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}! Чтобы узнать какая сейчас погода, напиши "
                         f"команду '/weather' и название города.")


@dp.message(Command('weather'))
async def process_weather_command(message: types.Message):
    try:
        city = message.text.split(' ')[1]
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru"
        )

        userid = message.from_user.id
        command = message.text
        datetimes = datetime.now().strftime('%Y-%m-%d %H:%M')

        if response.status_code == 404:
            answer = "Пожалуйста, укажите правильное название города"
            add_base(userid, command, datetimes, answer)
            await message.answer(answer)

        else:
            data = response.json()
            cityname = data["name"]
            cur_weather = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            desc = data["weather"][0]["description"]

            weather = str(f"***{datetimes}***\n"
                          f"Погода в городе: {cityname}\nТемпература: {cur_weather}C \n"
                          f"Ощущаемая температура {feels_like}C \n"
                          f"Описание погоды: {desc}\n"
                          f"Влажность: {humidity}%\nВетер: {wind} м/с\n"
                          f"Хорошего дня!")
            add_base(userid, command, datetimes, weather)
            await message.answer(weather)

    except IndexError:
        userid = message.from_user.id
        command = message.text
        datetimes = datetime.now().strftime('%Y-%m-%d %H:%M')
        answer = "Пожалуйста, укажите город после команды /weather"
        add_base(userid, command, datetimes, answer)
        await message.answer(answer)


async def main():
    bot = Bot(token=tg_bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
