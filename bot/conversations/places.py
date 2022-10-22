from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler
from bot.conversations.schemas import JSON
from bot.conversations import states


def place_choice(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    """Ask the user for info about the selected predefined choice."""
    assert update.message is not None
    assert context.user_data is not None

    question = 'Which place?'

    context.user_data['choice'] = 'palce'
    update.message.reply_text(question, reply_markup=ReplyKeyboardRemove())

    return states.PLACE_STATS


def place_stats(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    """Ask the user for info about the selected predefined choice."""
    assert update.message is not None
    place = update.message.text
    answer = f'about {place} ...'
    update.message.reply_text(answer)

    return ConversationHandler.END
