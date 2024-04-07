import html
import just_for_fun as justff
from aiogram import Router, Bot
from aiogram.types import ContentType
from aiogram import F, types
from aiogram.filters import Command, CommandStart, or_f
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.enums.parse_mode import ParseMode
from lexicon.lexicon import LEXICON_RU
from Parser import Parsa
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import time
import logging
from database.orm_query import orm_add_machine, orm_delete_machine, orm_delete_machines

# Инициализируем роутер уровня модуля
router = Router()


# router.message.filter(IsnotAdmin())

# Этот хэндлер срабатывает на команду /start
@router.message(
    or_f(CommandStart(), (F.text.lower() == "старт"), (F.text.lower() == "начало"), (F.text.lower() == "вперёд")))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], parse_mode=ParseMode.HTML)


# Этот хэндлер срабатывает на команду /help
@router.message(or_f(Command(commands='help'), (F.text.lower() == "help"), (F.text.lower() == "помощь")))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


@router.message(or_f(Command(commands='cat'), (F.text.lower() == "cat"), (F.text.lower() == "cats"),
                     (F.text.lower() == "кот"), (F.text.lower() == "коты"), (F.text.lower() == "котик"),
                     (F.text.lower() == "котики"), (F.text.lower() == "кошка"), (F.text.lower() == "кошки")))
async def get_cat(message: Message):
    await message.answer(text=LEXICON_RU['/cat'])
    await message.answer(text=justff.cat_answer())


@router.message(
    or_f(Command(commands='dog'), (F.text.lower() == "dog"), (F.text.lower() == "dogs"), (F.text.lower() == "собака"),
         (F.text.lower() == "собаки"), (F.text.lower() == "пёс"), (F.text.lower() == "пёсель"),
         (F.text.lower() == "псы")))
async def get_cat(message: Message):
    await message.answer(text=LEXICON_RU['/dog'])
    await message.answer(text=justff.dog_answer())


@router.message(
    or_f(Command(commands='fox'), (F.text.lower() == "лиса"), (F.text.lower() == "лис"), (F.text.lower() == "лисы"),
         (F.text.lower() == "fox"), (F.text.lower() == "foxes")))
async def get_cat(message: Message):
    await message.answer(text=LEXICON_RU['/fox'])
    await message.answer(text=justff.fox_answer())


@router.message(or_f(Command(commands='capybara'), (F.text.lower() == "капибара"), (F.text.lower() == "копибара"),
                     (F.text.lower() == "капебара"), (F.text.lower() == "копебара"), (F.text.lower() == "capybara")))
async def get_cat(message: Message):
    await message.answer(text=LEXICON_RU['/capybara'])
    await message.answer(text=justff.capybara_answer())


@router.message(or_f(Command("menu"), (F.text.lower() == "меню")))
async def menu_cmd(message: Message, session: AsyncSession):
    start_buttons = [KeyboardButton(text="Все машины"), KeyboardButton(text="Последние 5 машин"),
                     KeyboardButton(text="Обновления списка")]
    keyboard = types.ReplyKeyboardMarkup(keyboard=[start_buttons], resize_keyboard=True)
    # keyboard.add(*start_buttons)

    await message.answer("Вот меню:")
    await message.answer("Проверка списков машин", reply_markup=keyboard)


@router.message(F.text == "Все машины")
# @router.message(Command('all_machines'))
async def get_all_machines(message: Message, session: AsyncSession):
    try:
        await orm_delete_machines(session)
        # time.sleep(2)
        await message.answer("БД очищена")
    except Exception as e:
        await message.answer(f'Ошибка: \n{str(e)}\nВозможно не получилось почистить БД"')
    await message.answer("Прошу подождать, сайт и соединение медленные")

    p = Parsa()
    machines_dict = p.parser_resale()
    for k, v in sorted(machines_dict.items()):
        cards = f"{v['machine_image']} \n{hbold(datetime.datetime.fromtimestamp(v['machine_date_timestamp']))} \n{hbold(v['machine_title'])} \n{hunderline(v['machine_price'])} \n{hcode(v['machine_desc'])} \n" \
                f"{hlink(v['machine_title'], v['machine_url'])}"
        # cards = f"{datetime.datetime.fromtimestamp(v['machine_date_timestamp'])} \n {v['machine_title']} \n {v['machine_price']} \n {v['machine_desc']} \n" \
        #         f"{v['machine_url']}"
        try:
            await orm_add_machine(session, v)
            # time.sleep(2)
            await message.answer("Машина добавлена в базу данных")
        except Exception as e:
            await message.answer(f'Ошибка: \n{str(e)}\nДанные в базу данных возможно не добавились"')

        await message.answer(cards, parse_mode=ParseMode.HTML)


@router.message(F.text == "Последние 5 машин")
# @router.message(Command('5_last_machines'))
async def get_5_last_machines(message: Message):
    p = Parsa()
    machines_dict = p.parser_resale()
    for k, v in sorted(machines_dict.items())[-5:]:
        cards = f"{v['machine_image']} \n{hbold(datetime.datetime.fromtimestamp(v['machine_date_timestamp']))} \n{hbold(v['machine_title'])} \n{hunderline(v['machine_price'])} \n{hcode(v['machine_desc'])} \n" \
                f"{hlink(v['machine_title'], v['machine_url'])}"
        # cards = f"{datetime.datetime.fromtimestamp(v['machine_date_timestamp'])} \n {v['machine_title']} \n {v['machine_price']} \n {v['machine_desc']} \n" \
        #         f"{v['machine_url']}"

        await message.answer(cards, parse_mode=ParseMode.HTML)


@router.message(F.text == "Обновления списка")
# @router.message(Command('updates_new_machines'))
async def get_updates_new_machines(message: Message, session: AsyncSession):
    await message.answer("Посмотрим что там новенького, нужно время")
    p = Parsa()
    machines_dict = p.check_new_updates()
    if len(machines_dict) >= 1:
        for k, v in sorted(machines_dict.items()):
            cards = f"{v['machine_image']} \n{hbold(datetime.datetime.fromtimestamp(v['machine_date_timestamp']))} \n{hbold(v['machine_title'])} \n{hunderline(v['machine_price'])} \n{hcode(v['machine_desc'])} \n" \
                    f"{hlink(v['machine_title'], v['machine_url'])}"
            # cards = f"{datetime.datetime.fromtimestamp(v['machine_date_timestamp'])} \n {v['machine_title']} \n {v['machine_price']} \n {v['machine_desc']} \n" \
            #         f"{v['machine_url']}"
            await message.answer(cards, parse_mode=ParseMode.HTML)
            try:
                await orm_add_machine(session, v)
                # time.sleep(2)
                await message.answer("Машина добавлена в базу данных")
            except Exception as e:
                await message.answer(f'Ошибка: \n{str(e)}\nДанные в базу данных возможно не добавились"')
    else:
        await message.answer(hcode("Обновлений нет"), parse_mode=ParseMode.HTML)


@router.message(or_f(Command(commands='clear_database'), F.text == "Очистить"))
# @router.message(Command('all_machines'))
async def del_all_machines(message: Message, session: AsyncSession):
    await message.answer("Сейчас поудаляю всё")
    try:
        await orm_delete_machines(session)
        # time.sleep(2)
        await message.answer("БД очищена")
    except Exception as e:
        await message.answer(f'Ошибка: \n{str(e)}\nВозможно не получилось почистить БД"')


# Этот хэндлер будет срабатывать на команду "/delmenu"
# и удалять кнопку Menu c командами
@router.message(Command(commands='delmenu'))
async def del_main_menu(message: Message, bot: Bot):
    await bot.delete_my_commands()
    await message.answer(text='Кнопка "Menu" удалена')
