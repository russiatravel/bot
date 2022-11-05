from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext

from bot.clients.api import client as api
from bot.conversations import states
from bot.conversations.schemas import JSON


def city_choice(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    """Asks the user to select a city."""
    assert update.message is not None
    assert context.user_data is not None

    question = 'В каком городе будем искать достопримечательности?'
    context.user_data['choice'] = 'city'
    update.message.reply_text(question, reply_markup=ReplyKeyboardRemove())

    return states.CITY_LIST


def city_list(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    assert update.message is not None
    assert context.user_data is not None

    if not isinstance(update.message.text, str):
        update.message.reply_text('Input text')
        return states.CITY_LIST

    target_cities = update.message.text
    cities = api.cities.get_list_by_name(target_cities)

    if not cities:
        update.message.reply_text('Такого города у нас нет')
        return states.CITY_LIST

    city_name = [city.name for city in cities]
    update.message.reply_text(', '.join(city_name))

    return states.CITY_STATS


def city_stats(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    """Asks the user to select a place."""
    assert update.message is not None
    assert context.user_data is not None

    if not isinstance(update.message.text, str):
        update.message.reply_text('Input text')
        return states.CITY_STATS

    target_city = update.message.text
    cities = api.cities.get_by_name(target_city)

    if not cities:
        update.message.reply_text('Такого города у нас нет')
        return states.CITY_STATS

    city = cities[0]
    city_places = api.cities.get_for_city(city.uid)

    place_name = [place.name for place in city_places]
    update.message.reply_text(', '.join(place_name))
    context.user_data['city_id'] = city.uid

    return states.PLACE_STATS_BY_CITY
