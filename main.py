# from config_data.bot_config import load_config, Config
import config_data
from aiogram import Bot, Dispatcher, types
from handlers import user_handlers, other_handlers
import asyncio
from Parser import Parsa
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.types import BotCommand
from keyboards.set_menu import set_main_menu
import datetime
import logging.config
import yaml
from logging_conf.logging_settings import logging_config

# Для загрузки конфигурации логгирования из файла .yaml: (Требуется починить!!!)
# with open('logging_conf/logging_config.yaml', 'rt') as f:
#     config = yaml.safe_load(f.read())
# # logging.config.dictConfig(yaml.safe_load(f.read()))

################################# Для логирования раскоментировать:
# Загружаем настройки логирования из словаря `logging_config`
# logging.config.dictConfig(logging_config)


# альтернативный способ чтения секретов из .env
# from dotenv import find_dotenv, load_dotenv
#
# load_dotenv(find_dotenv())


# Функция конфигурирования и запуска бота
# async def main() -> None:
# Загружаем конфиг в переменную config
# config = load_config('.env')
config: config_data.Config = config_data.load_config()  # load_config('.env')

ALLOWED_UPDATES = ['message, edited_message']

# bot_token = config.tg_bot.token  # Сохраняем токен в переменную bot_token
superadmin = config.tg_bot.admin_ids[0]  # Сохраняем ID админа в переменную superadmin

from middlewares.db import DataBaseSession
from database.engine import create_db, drop_db, session_maker

# Инициализируем бот и диспетчер
# bot = Bot(token=bot_token)
bot = Bot(token=config.tg_bot.token)
dp = Dispatcher()
# print(bot.token)

# Регистрируем роутеры в диспетчере
dp.include_router(user_handlers.router)
dp.include_router(other_handlers.router)


async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('бот лЁг')

# Вручную создание кнопок в menu
# Создаем асинхронную функцию
# async def set_main_menu(bot: Bot):
#     # Создаем список с командами и их описанием для кнопки menu
#     main_menu_commands = [
#         BotCommand(command='/help',
#                    description='Справка по работе бота'),
#         BotCommand(command='/start',
#                    description='Описание функций бота при начале работы'),
#         BotCommand(command='/menu',
#                    description='Получить меню для получения списка б.у. машин с сайта'),
#         BotCommand(command='/clear_database',
#                    description='Почистить базу данных машин'),
#         BotCommand(command='/cat',
#                    description='Получить картинку котика'),
#         BotCommand(command='/dog',
#                    description='Получить картинку пёсика'),
#         BotCommand(command='/fox',
#                    description='Получить картинку лисички'),
#         BotCommand(command='/capybara',
#                    description='Получить картинку капибары')
#
#     ]
#
#     await bot.set_my_commands(main_menu_commands)


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))  # регистрируем Middleware с передачей сессии

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    # await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)  # c включением по допустимым update
    # dp.startup.register(set_main_menu)   # это для случая, если прямо в main команды menu определяем
    # Настраиваем кнопку Menu
    await set_main_menu(bot)

    await dp.start_polling(bot)

    # Создаем асинхронную функцию для периодической проверки и отправки обновлений с сайта (НЕ РАБОТАЕТ ВРЕМЕННО)
    async def news_every_day(wait_for):
        p = Parsa()
        while True:
            # await asyncio.sleep(wait_for)
            new_machines = p.check_new_updates()

            if len(new_machines) >= 1:
                for k, v in sorted(new_machines.items()):
                    cards = f"{hbold(datetime.datetime.fromtimestamp(v['machine_date_timestamp']))} \n{hbold(v['machine_title'])} \n{hunderline(v['machine_price'])} \n{hcode(v['machine_desc'])} \n" \
                            f"{hlink(v['machine_title'], v['machine_url'])}"

                    # get your id @userinfobot

                    await bot.send_message(superadmin, cards, disable_notification=True)

            else:
                await bot.send_message(superadmin, "Пока нет свежих новостей...", disable_notification=True)

            await asyncio.sleep(wait_for)

    # loop = asyncio.get_event_loop()
    # loop.create_task(news_every_day())
    # asyncio.create_task(news_every_day())
    #
    # dp.loop.create_task(news_every_day(10))  # пока что оставим 10 секунд (в качестве теста)

    await news_every_day(10)


if __name__ == '__main__':
    # print(bot.token, superadmin)

    asyncio.run(main())
