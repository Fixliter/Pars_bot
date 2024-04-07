from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU

# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер будет срабатывать на любые сообщения,
# кроме команд "/start" и "/help"
@router.message()
async def echo(message: Message):
    text = message.text
    try:
        if text in ['Привет', 'привет', 'hi', 'hello', 'здарово', 'здаров', 'салют', 'алоха']:
            await message.answer('И тебе привет!')
        elif text in ['Пока', 'пока', 'До свидания', 'чао','покеда','bye', 'goodbye']:
            await message.answer('И тебе пока!')
        else:
            await message.answer(message.text)
    except TypeError:
        await message.reply(text=LEXICON_RU['no_echo'])

