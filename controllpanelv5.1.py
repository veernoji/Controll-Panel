import asyncio
import os
import logging
import pyfiglet
import configparser
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from PIL import ImageGrab
import keyboard
import pyautogui
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO)

ascii_banner = pyfiglet.figlet_format("controll recode")
print(ascii_banner)
print("by veernoji. <3")
print(" ")
print("💢Координаты для персонажей💢:")
print("💢1 Персонаж x= 1546, y= 383 💢")
print("💢2 Персонаж x= 1626 , y= 557 💢")
print("💢3 Персонаж x= 1555 , y= 685 💢")

CONFIG_FILE = "settings.ini"
config = configparser.ConfigParser()

if os.path.exists(CONFIG_FILE):
    config.read(CONFIG_FILE)
    TOKEN = config["Telegram"]["token"]
    CHAT_ID = int(config["Telegram"]["chat_id"])
    PASSWORD = config["Telegram"]["password"]
    RECONNECT_X = int(config["Reconnect"]["x"])
    RECONNECT_Y = int(config["Reconnect"]["y"])
    print("💢Данные загружены из settings.ini💢")
else:
    TOKEN = input("💢Введите ваш Telegram токен от бота💢: ")
    CHAT_ID = int(input("💢Введите ваш Telegram id💢: "))
    PASSWORD = input("💢Введите ваш пароль💢: ")

    RECONNECT_X = int(input("💢Введите X координату для переподключения💢: "))
    RECONNECT_Y = int(input("💢Введите Y координату для переподключения💢: "))

    config["Telegram"] = {
        "token": TOKEN,
        "chat_id": str(CHAT_ID),
        "password": PASSWORD
    }
    
    config["Reconnect"] = {
        "x": str(RECONNECT_X),
        "y": str(RECONNECT_Y)
    }

    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)
    
    print("💢Данные сохранены в settings.ini💢")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
dp.include_router(router)

BASE_WIDTH = 1920
BASE_HEIGHT = 1080

def normalize_coords(x_abs, y_abs):
    screen_width, screen_height = pyautogui.size()
    return int(x_abs * screen_width / BASE_WIDTH), int(y_abs * screen_height / BASE_HEIGHT)

def main_keyboard():
    buttons = [
        [KeyboardButton(text="💢Скриншот💢"), KeyboardButton(text="💢АнтиАФК💢")],
        [KeyboardButton(text="💢Чек Статистику💢"), KeyboardButton(text="💢Колесо Удачи💢"),
         KeyboardButton(text="💢Лотерейка💢"), KeyboardButton(text="💢Переподключение💢")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

async def msg_tg(text: str):
    await bot.send_message(CHAT_ID, text)

async def screen_tg():
    try:
        path = "screenshot.png"
        screenshot = ImageGrab.grab()
        screenshot.save(path)
        photo = FSInputFile(path)
        await bot.send_photo(CHAT_ID, photo)
        os.remove(path)
    except Exception as e:
        await bot.send_message(CHAT_ID, f"Ошибка при создании скриншота: {e}")

@router.message(Command("start"))
async def menu(message: types.Message):
    await message.answer("💢Control Panel💢", reply_markup=main_keyboard())

@router.message(F.text == "💢Скриншот💢")
async def screenshot_handler(message: types.Message):
    await screen_tg()

@router.message(F.text == "💢Лотерейка💢")
async def buy_lottery(message: types.Message):
    keyboard.press_and_release('f4')
    now = datetime.now()
    if 1 <= now.hour < 12:
        await bot.send_message(message.chat.id, '💢До 12 часов по мск покупка билетов для Лотерейки невозможна💢')
        await menu(message)
        return

    for _ in range(3):
        pyautogui.press('up')
        time.sleep(1)

    pyautogui.click(*normalize_coords(1650, 760))  
    time.sleep(1)
    pyautogui.click(*normalize_coords(1750, 1000))  
    time.sleep(1)

    for _ in range(3):
        pyautogui.press('backspace')

    await bot.send_message(message.chat.id, '💢Билет на Лотерейку был куплен💢')
    keyboard.press_and_release('f3')
    await menu(message)
    await asyncio.sleep(7200)

@router.message(F.text == "💢Колесо Удачи💢")
async def test228(message: types.Message):
    await msg_tg("💢Отлично! Запускаю Колесо Удачи...💢")
    await asyncio.sleep(1)

    keyboard.press_and_release("f10")
    await asyncio.sleep(2)

    pyautogui.click(*normalize_coords(1289, 285))
    await asyncio.sleep(1)
    pyautogui.click(*normalize_coords(596, 345))
    await asyncio.sleep(1)
    pyautogui.click(*normalize_coords(773, 656))
    await asyncio.sleep(1)
    pyautogui.click(*normalize_coords(989, 861))
    await asyncio.sleep(1)

    keyboard.send("esc")
    await asyncio.sleep(1)
    keyboard.send("esc")
    await asyncio.sleep(1)
    keyboard.send("esc")

    await screen_tg()
    await msg_tg("💢Скрипт выполнен💢")

@router.message(F.text == "💢Переподключение💢")
async def reconnect(message: types.Message):
    await msg_tg("💢Отлично! Переподключаюсь...💢")
    await asyncio.sleep(1)
    keyboard.press_and_release("f1")
    await asyncio.sleep(1)
    pyautogui.click(*normalize_coords(484, 232))
    await asyncio.sleep(15)
    pyautogui.click(*normalize_coords(894, 615))
    await asyncio.sleep(2)
    keyboard.write(PASSWORD)  
    await asyncio.sleep(1)
    pyautogui.click(*normalize_coords(953, 692))
    await asyncio.sleep(1)

    print(f"💢Используются координаты: X={RECONNECT_X}, Y={RECONNECT_Y}💢")
    pyautogui.click(*normalize_coords(RECONNECT_X, RECONNECT_Y))

    await asyncio.sleep(3)
    pyautogui.click(*normalize_coords(941, 954))
    await asyncio.sleep(3)
    pyautogui.click(*normalize_coords(958, 990))
    await asyncio.sleep(3)
    pyautogui.click(*normalize_coords(981, 796))
    await asyncio.sleep(3)
    await screen_tg()
    await msg_tg("💢Скрипт выполнен💢")

@router.message(F.text == "💢АнтиАФК💢")
async def afkws(message: types.Message):
    await msg_tg("💢Запускаю Анти-АФК...💢")

    for _ in range(7):
        keyboard.press("w")
        keyboard.press("s")
        await asyncio.sleep(600)
        keyboard.release("w")
        keyboard.release("s")
        await asyncio.sleep(1)

        keyboard.press_and_release("f10")
        await asyncio.sleep(2)

        pyautogui.click(*normalize_coords(1289, 285))
        await asyncio.sleep(1)
        pyautogui.click(*normalize_coords(596, 345))
        await asyncio.sleep(1)
        pyautogui.click(*normalize_coords(773, 656))
        await asyncio.sleep(1)
        pyautogui.click(*normalize_coords(989, 861))
        await asyncio.sleep(1)

        keyboard.send("esc")
        await asyncio.sleep(1)
        keyboard.send("esc")
        await asyncio.sleep(1)
        keyboard.send("esc")

        await screen_tg()

    await msg_tg("💢Анти-АФК завершен💢")

@router.message(F.text == "💢Чек Статистику💢")
async def check_stats(message: types.Message):
    await msg_tg("💢Запускаю проверку статистики...💢")
    await asyncio.sleep(1)

    keyboard.press_and_release("f10")
    await asyncio.sleep(2)

    await screen_tg()
    keyboard.send("esc")
    await msg_tg("💢Статистика отправлена💢")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
