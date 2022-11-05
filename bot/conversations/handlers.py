from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler

from bot.conversations import states
from bot.conversations.cities import city_choice, city_list, city_stats
from bot.conversations.core import cancel, start
from bot.conversations.places import place_choice, place_stats, place_stats_by_city

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        states.CHOOSING: [
            MessageHandler(
                Filters.regex('^(City|Город)$'), city_choice,
            ),
            MessageHandler(
                Filters.regex('^(Place|Достопримечательность)$'), place_choice,
            ),
        ],
        states.CITY_STATS: [
            MessageHandler(
                Filters.text, city_stats,
            ),
        ],
        states.CITY_LIST: [
            MessageHandler(
                Filters.text, city_list,
            ),
        ],
        states.PLACE_STATS: [
            MessageHandler(
                Filters.text, place_stats,
            ),
        ],
        states.PLACE_STATS_BY_CITY: [
            MessageHandler(
                Filters.text, place_stats_by_city,
            ),
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
