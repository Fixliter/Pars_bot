# Telegram Chatbot with parsing some site/s

This is a Python-based Sample of Telegram chatbot that can be used for parsing some sites of the used food packaging equipment and some fun things

<p align="center">
<img src="https://xakep.ru/wp-content/uploads/2015/09/botFather-telegram-site.png" alt="dialog-chat-bot-cover" border="0" ></a>
</p>


В планах было в учебных целях написать парсеры к определенным сайтам, сохранение данных в какую-то БД, телеграмм бот, который по запрашиваемым командам делает парсинг, обновляет БД оперативную таблицу, сравнивает с архивной, говорит что нового появилось. 
<br>Ну основа положена =)<br>


**Ссылка на бота**: https://t.me/pars_for_used_equip_bot

___

# 🔥 <span style="color:yellow">Features</span>

- предоставляет данные парсинга сайта б.у. упаковочного оборудования, позволяя получить весь список, обновления, последние 5 из списка 
- Сохранение данных в json и БД
- В Бот подставлен один сайт для работы по отправке/сохранению данных, но по факту реализован парсинг трёх разных сайтов разными инструментами (request, Selenium, Beautiful soap)
- Just for fun можно получить рандомные картинки: котиков, собак, лис, капибар
- При тексте, не входящем в предусмотренные ответы, бот отвечает эхом
- Бот использует базу данных SQLLite для хранения в ней данных парсинга в тренировочных целях
- Бот использует файл json для хранения в ней данных парсинга в тренировочных целях

**Команды бота**:

 - `/start` - запустить бота и получить команды для работы.
 - `/help` - краткая пояснялка.
 - `/menu` - для получения кнопок парсера "Все машины", "Последние 5 машин", "Обновления списка".
 - `/clear_database` - очистить базу данных.
 - `/cat` - получить картинку котика.
 - `/dog` - получить картинку собаки.
 - `/fox` - получить картинку лисы.
 - `/capybara` - получить картинку капибары.

<p align="center">
<img src="https://cdn.sites.admitad.ru/www.admitad.ru/2023/08/admitad-bot-blog.png" alt="dialog-chat-bot-cover" border="0" ></a>
</p>

___

# 🛠️ <span style="color:red">Requirements</span>

- Python 3.11+
- SQLlite или PostgreSQL
- requests~=2.31.0
- lxml~=5.1.0
- beautifulsoup4~=4.12.3
- selenium~=4.18.1
- aiogram~=3.4.1
- environs~=11.0.0
- python-dotenv~=1.0.1
- SQLAlchemy~=2.0.29
- pandas~=2.2.1
- PyYAML~=6.0.1

___
# 🏗️ <span style="color:blue">Installation</span>

## Local

- Clone or download the repository.

    ```
    git clone git@github.com: https://github.com/Fixliter/Pars_bot.git
    ```

- [Create virtual environment and activate it](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) and [install dependencies](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#using-requirements-files).

    ```
    python -m venv env
    source env/bin/activate
    BOT_TOKEN=
    pip install --upgrade pip && pip install -r requirements.txt
    ```
- Run the bot.

    ```
    python main.py
    ```
  

<p align="center">
<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSx5cB4IRqqUuvdtpyY9mTXOj-SAtRZwag39zt0gUJ8hXAXZPhNaCk9mCaMR9Qio5-Hnkg&usqp=CAU" alt="dialog-chat-bot-cover" border="0" ></a>
</p>  

# 🏃  <span style="color:deeppink">Start</span>

1. **Main**: исполнительный файл для запуска программы.
2. **Database**: Для работы через PostgreSQL, нужно установить сервер этой СУБД на ПК, или указать url адрес базы данных на удаленном сервере. Иначе, использовать engine на sqlite+aiosqlite, также удобно использовать DB Browser(SQLite) для непосредственного просмотра базы данных
3. **Secrets**: Необходимо создать и вставить свои данные в файл .env по примеру из файла .env.example 
<br>BOT_TOKEN,<br>ADMIN_IDS, <br>DB_LITE, <br>DB_URL(PostgreSql)<br>
```
BOT_TOKEN=5424991242:AAGwomxQz1p46bRi_2m3V7kvJlt5RjK9xr0
ADMIN_IDS=173901673,124543434,143343455
DB_LITE=sqlite+aiosqlite:///my_base.db
DB_URL=postgresql+asyncpg://login:password@localhost:5432/db_name


DATABASE=someDatabaseName
DB_HOST=127.0.0.1
DB_USER=dbUser
DB_PASSWORD=dbPassword
```
___
# 💻 <span style="color:green">Structure</span>

1. **Как и сказано выше, запускающий файл main.**
2. **__init__** Для каждого пакета добавлен __init__ с импортом для удобства на случай расширения функционала
3. **logging.** Основа и конфигурация logging в logging_conf. В logging_settings конфигурация через словарь, в logging_config через yaml файл, но регистрируется в main yaml(надо разбираться), поэтому выбрано через словарь
4. **filters.** Фильтры бота в filter, сделан для примера фильтра is_admin.py
5. **handlers.** В своей директории handlers разделены на user и other, в перспективе можно добавить для admin. 
6. **just_for_fun.** В этом пакете простые обращения к API для предоставления ссылки на картинку животных. 
6. **database.** Пакет с моделями (модель Machine), движком для определенной БД, ORM работой с данными. 
6. **keyboards.** Пакет используется для назначения команд "menu", также следует использовать при добавлении всех кнопок.
6. **middlewares.** В данном случае реализовано подключение сессии работы с БД к хэндлерам.
6. **config_data.** Реализована распаковка .env атрибутов для дальнейшего использования при работе с ботом и базой данных.
6. **lexicon.** Используется для шаблонов ответов и команд.
    

# Данные

**Данные парсинга сайта** хранятся в json файле `res/events.json`.

```json
{
  "163569866": { // Уникальный ID с сайта
        "machine_date_timestamp": 1712437200.0,
        "machine_title": "CRYOVAC CT303E P\nShrink film (3x)",
        "machine_url": "https://www.resale.info/../../../en/cryovac-ct303e-p-shrink-film-3x/No-163569866",
        "machine_desc": "Description: size roll 355 mm x 1740 meters 11 micron weight per roll\nis 14 kg delivered in original packaging Approx. Onsite Dimension. (l\nx w x h): 800 x 600 x 450 mm, weight approx.: 42 kg�... more information",
        "machine_price": "",   // Опциональное
        "machine_image": "https://res.surplex.com/images/c_fit,d_no_image.png,f_auto,fl_progressive,h_300,q_auto,w_465/i_06869811/CRYOVAC_CT303E_P_Shrink_film_3x_CRYOVAC_CT303E_P.jpg" // Опциональное
    }
}
```



**Структура DB:**

```js
// Table - Machine 
// Model:
{
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # - первичный ключ с автоинкрементом
    name: Mapped[str] = mapped_column(String(300), nullable=False)  # - не может быть пустым и более 300 символов
    description: Mapped[str] = mapped_column(Text)  # - класс Текст (не varchar), в котором может быть большой текст
    price: Mapped[str] = mapped_column(String(150))  # можно было бы парсить до float и mapped_column(Float(asdecimal=True), nullable=False)
    image: Mapped[str] = mapped_column(String(150))  # может быть varchar
    url: Mapped[str] = mapped_column(Text)  # - класс Текст (не varchar), в котором может быть большой текст
}
```
***
# 🙇 <span style="color:purple">To_do and to_improve</span>

- **try/Except**: Структуру хотелось бы сделать с try/Except блоками по кодам ошибок для большей отслеживаемости и надежности
- **orm users**: Завести БД пользователей
- **admin/user/vip user**: Разделить возможности админа и обычных пользователей/vip пользователей
- **logging**: Донастроить логгинг
- **async parser**: В целом парсеры можно переписать поасинхроннее
- **types**: Добавить аннотацию типов для более прозрачной и удобной работы
- **update timeout**: Не удалось/не успел настроить периодическую проверку обновлений данных сайта асинхронной функцией, не реагирует почему-то, но бота полностью не роняет
- **some sites**: Так как реализован парсинг еще двух сайтов, которые не задейстованы явно в боте, но можно также их прицепить и использовать через многоуровневое меню кнопок и вывод информации
- **fsm states**: Можно докрутить и сделать что-то интерфейсное с FSM машиной и разделением состояний админа и простого пользователя
- **inline**: И соответстенно далее инлайн кнопки у админа для удаления, добавления, редактирования записи в БД, у пользователя свои inline кнопки
- **webhook**: Запустить в режиме webhook'а


<p align="center">
<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEHPlHYmRKamBgcvcJQEu9A2P8ZRlLvrkpRg&s" alt="dialog-chat-bot-cover" border="0" ></a>
</p>