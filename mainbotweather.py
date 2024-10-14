import requests
from datetime import datetime
from config import open_weather_token
from models import Log, SessionLocal
from aiogram import Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from fastapi import APIRouter


dp = Dispatcher()
db = SessionLocal()
telegramrouter = APIRouter()


def add_base(userid, command, datatime, answer):
    log = Log(userid=userid, command=command, datatime=datatime, answer=answer)
    db.add(log)
    db.commit()
    db.refresh(log)


@telegramrouter.get("/start")
@dp.message(CommandStart())
async def command_start_handler(message: Message):
    """
    Отправляет приветственное сообщение
    """
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}! Чтобы узнать какая сейчас погода, напиши "
                         f"команду '/weather' и название города.")


@telegramrouter.get("/weather {city_name}")
@dp.message(Command('weather'))
async def process_weather_command(message: types.Message):
    """
    По команде /weather <city_name> возвращает погоду в указанном городе на данный момент
    """
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
