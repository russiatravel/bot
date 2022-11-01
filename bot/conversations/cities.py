from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext

from bot.clients.api import client as api
from bot.conversations import states
from bot.conversations.schemas import JSON


def city_choice(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    """Asks the user to select a city."""
    assert update.message is not None
    assert context.user_data is not None

    cities = api.cities.get_all()
    city_name = [city.name for city in cities]

    question = 'Which city from {cities}?'.format(cities=', '.join(city_name))
    context.user_data['choice'] = 'city'
    update.message.reply_text(question, reply_markup=ReplyKeyboardRemove())

    return states.CITY_STATS


def city_stats(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    """Asks the user to select a place."""
    assert update.message is not None

    if not isinstance(update.message.text, str):
        update.message.reply_text('Input text')
        return states.CITY_STATS

    target_city = update.message.text
    city = api.cities.get_by_name(target_city)[0]
    city_places = api.cities.get_for_city(city.uid)

    place_name = [place.name for place in city_places]
    update.message.reply_text(', '.join(place_name))

    return states.PLACE_STATS
