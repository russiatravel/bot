from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler

from bot.clients.api import client as api
from bot.conversations import states
from bot.conversations.schemas import JSON


def place_choice(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    """Ask the user for info about the selected predefined choice."""
    assert update.message is not None
    assert context.user_data is not None

    question = 'Which place?'

    context.user_data['choice'] = 'place'
    update.message.reply_text(question, reply_markup=ReplyKeyboardRemove())

    return states.PLACE_STATS


def place_stats(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    """Asks the user to enter a place name."""
    assert update.message is not None

    if not isinstance(update.message.text, str):
        update.message.reply_text('Input text')
        return states.PLACE_STATS

    target_places = update.message.text

    places = api.places.get_place(target_places)

    for place in places:
        answer = f'{place.name} находится в городе x. \n {place.description}'
        update.message.reply_text(answer)

    return ConversationHandler.END
