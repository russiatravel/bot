import os

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

    if not places:
        update.message.reply_text('Таких достопримечательностей у нас нет')
        return states.PLACE_STATS

    for place in places:
        city = api.cities.get_by_id(place.city_id)

        max_lenght = int(os.environ['DESCRIPTION_LENGHT'])

        if len(place.description) > max_lenght:
            output_description = place.description[:max_lenght]
            output_description = f'{output_description}...'
        else:
            output_description = place.description

        answer = (
            f'<b>{place.name}</b> находится в <b>{city.name}</b>. \n \n'
            f'{output_description}'
            f'<a href="{place.preview_image_url}">&#8205;</a>'
        )

        update.message.reply_html(answer)

    return ConversationHandler.END


def place_stats_by_city(update: Update, context: CallbackContext[JSON, JSON, JSON]) -> int:
    """Asks the user to enter a place name."""
    assert update.message is not None
    assert context.user_data is not None

    if not isinstance(update.message.text, str):
        update.message.reply_text('Input text')
        return states.PLACE_STATS_BY_CITY

    target_places = update.message.text
    places = api.places.get_place(target_places)
    target_city_id = context.user_data.get('city_id', 'Not found')

    if not places:
        update.message.reply_text('Таких достопримечательностей у нас нет')
        return states.PLACE_STATS

    max_lenght = int(os.environ['DESCRIPTION_LENGHT'])

    for place in places:
        city = api.cities.get_by_id(place.city_id)

        if city.uid == target_city_id:
            if len(place.description) > max_lenght:
                output_description = place.description[:max_lenght]
                output_description = f'{output_description}...'
            else:
                output_description = place.description

            answer = (
                f'<b>{place.name}</b> находится в <b>{city.name}</b>. \n \n'
                f'{output_description}'
                f'<a href="{place.preview_image_url}">&#8205;</a>'
            )
            update.message.reply_html(answer)

    return ConversationHandler.END
