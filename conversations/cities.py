from bot.clients.api import client as api
from bot.conversations import states
from bot.conversations.schemas import JSON
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler


def city_choice(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    """Ask the user for info about the selected predefined choice."""
    assert update.message is not None
    assert context.user_data is not None

    cities = api.cities.get_all()
    city_name = [city.name for city in cities]

    question = 'Which city form {cities}?'.format(cities=','.join(city_name))
    context.user_data['choice'] = 'city'
    update.message.reply_text(question, reply_markup=ReplyKeyboardRemove())

    return states.CITY_STATS


def city_stats(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    """Ask the user for info about the selected predefined choice."""
    assert update.message is not None
    city = update.message.text
    answer = f'about {city} ...'
    update.message.reply_text(answer)

    return ConversationHandler.END
