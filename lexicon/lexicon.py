from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
import logging

logger = logging.getLogger(__name__)

logger.debug('Лог DEBUG')
logger.info('Лог INFO')
logger.warning('Лог WARNING')
logger.error('Лог ERROR')
logger.critical('Лог CRITICAL')

LEXICON_RU: dict[str, str] = {
    '/start': 'Привет!\n\nЯ бот для демонстрации работы парсера и некоторых API!\n\n'
              'Если хотите - можете мне что-нибудь прислать или '
              'отправить команду /help \n'
              'для получения данных по б.у. машинам отправить команду /menu \n'
              'ну или просто могу вам отправить котика по команде /cat \n'
              'если хотите взглянуть на пёселя то команда /dog \n'
              'лису можно получить по команде /fox \n'
              'также есть и копибарки по команде /capybara \n',
    '/help': 'Я просто отправляю вам информацию с сайта по б.у. машинам для упаковочной линии пищевых продуктов\n'
             'ну и еще могу всякую глупость в виде картинок котиков, собак и т.д.,\n'
             'в принципе все возможности описаны когда вы вызываете команду /start \n',
    '/cat': 'Вот такого котика тебе отправляю',
    '/dog': 'Вот такого пёселя тебе отправляю',
    '/fox': 'Вот такую лису тебе отправляю',
    '/capybara': 'Вот такого копибарчика тебе отправляю',
    'no_echo': 'Данный тип апдейтов не поддерживается '
               'методом send_copy'
}

LEXICON_COMMANDS_RU: dict[str, str] = {
    '/help': 'Справка по работе бота',
    '/start': 'Описание функций бота при начале работы',
    '/menu': 'Меню для получения списка б.у. машин с сайта',
    '/clear_database': 'Почистить базу данных машин',
    '/get_machines_from_db': 'Получить данные по машинам из БД',
    '/cat': 'Получить картинку котика',
    '/dog': 'Получить картинку пёсика',
    '/fox': 'Получить картинку лисички',
    '/capybara': 'Получить картинку капибары'
}
