"""
button
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from BOT.config import curr


def get_time_buttons(cripto):
    """
    return button with cripto
    """
    return InlineKeyboardMarkup(
        [
        [InlineKeyboardButton("10 дней", callback_data=f'{cripto}_day')],
        [InlineKeyboardButton("10 часов", callback_data=f'{cripto}_hour')],
        [InlineKeyboardButton("Назад", callback_data='back')],
        [InlineKeyboardButton("Главное меню", callback_data='start')],
        ]
    )


def get_main_menu_buttons():
    """
    return to menu
    """
    return InlineKeyboardMarkup([InlineKeyboardButton(cur, callback_data=f'{cur}') for cur in curr])


def get_action_buttons(cripto):
    """
    return action button
    """
    return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Показать текущий курс", callback_data=f'{cripto}_latest')],
                [InlineKeyboardButton("Статистика", callback_data=f'{cripto}_history')],
                [InlineKeyboardButton("Назад", callback_data='back')],
                [InlineKeyboardButton("Главное меню", callback_data='start')],
            ]
        )


def callback_photo(cripto):
    """
    return callback button
    """
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Назад", callback_data=f'{cripto}_callback')],
            [InlineKeyboardButton("Главное меню", callback_data='start')],
        ]
    )
