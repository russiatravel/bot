from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler

from bot.conversations import states
from bot.conversations.schemas import JSON

reply_keyboard = [
    ['City', 'Place'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def start(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    """Start the conversation and ask user for input."""
    question = """Hi!
    city or place?
    """
    assert update.message is not None
    update.message.reply_text(text=question, reply_markup=markup)

    return states.CHOOSING


def cancel(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    """Ask the user for info about the selected predefined choice."""
    assert update.message is not None
    question = 'Bue!'
    update.message.reply_text(question)

    return ConversationHandler.END
