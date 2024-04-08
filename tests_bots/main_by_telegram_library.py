from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler, PicklePersistence
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from secret import TOKEN
import logging
from uuid import uuid4
from html import escape
from telegram.constants import ParseMode
import random

# import BotSetup

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=logging.INFO
)

# logging.getLogger("httpx").setLevel(logging.WARNING)
bot_logger = logging.getLogger("httpx")
bot_logger.setLevel(logging.WARNING)
bot_logger.addHandler(logging.StreamHandler())
bot_logger.addHandler(logging.FileHandler("../bot.log"))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")


async def scream(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["screams"] = context.user_data.get("screams", 0) + 1
    if update.message.text:
        scream_text = update.message.text.upper()

        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{scream_text}!!!")


async def scream_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "screams" in context.user_data:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'You made me scream {context.user_data["screams"]}')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"I have not screams for yet")


async def inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.inline_query.query:
        return

    exclamations = "!" * random.randint(1, 10)
    result = [InlineQueryResultArticle(
        id=str(uuid4()),
        title="Scream this vry loud",
        input_message_content=InputTextMessageContent(
            f"<b><i>{update.inline_query.query.upper()} {exclamations}</i></b>", parse_mode=ParseMode.HTML)
    )]

    await update.inline_query.answer(result, cache_time=10, is_personal=True)


if __name__ == '__main__':
    persistence = PicklePersistence(filepath="../data")

    app_builder = ApplicationBuilder()
    app_builder.token(TOKEN)
    app_builder.persistence(persistence)
    app = app_builder.build()

    start_handler = CommandHandler("hello", start)
    app.add_handler(start_handler)
    scream_handler = CommandHandler("scream", scream)
    app.add_handler(scream_handler)
    scream_handler = CommandHandler("scream_count", scream_count)
    app.add_handler(scream_handler)

    app.add_handler(InlineQueryHandler(inline))

    app.run_polling()
