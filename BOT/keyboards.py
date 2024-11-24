"""
Button Generation Module

This module contains functions for generating inline keyboard buttons used in the
Telegram bot interface. The buttons are used to navigate between menus and perform actions 
related to cryptocurrency selection and data display.

Functions:
    - get_time_buttons: Returns buttons for selecting a time period (10 days or 10 hours)
    - get_main_menu_buttons: Returns buttons for selecting a cryptocurrency from the main menu.
    - get_action_buttons: Returns buttons for performing actions on a selected cryptocurrency.
    - callback_photo: Returns buttons for navigating back or to the main menu.

Dependencies:
    - curr: List of supported cryptocurrencies (BTC, ETH, TON).
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from BOT.config import curr


def get_time_buttons(cripto):
    """
    Generates an inline keyboard with time selection buttons for cryptocurrency analysis.

    Args:
        cripto (str): The selected cryptocurrency (e.g., 'BTC', 'ETH').

    Returns:
        InlineKeyboardMarkup: A markup object with buttons for time period selection 
        (10 days or 10 hours), as well as 'Back' and 'Main Menu' options.
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
    Generates an inline keyboard with buttons for selecting a cryptocurrency.

    Returns:
        InlineKeyboardMarkup: A markup object with buttons 
        for each cryptocurrency in the 'curr' list.
    """
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(cur, callback_data=f'{cur}') for cur in curr]
    ])


def get_action_buttons(cripto):
    """
    Generates an inline keyboard with action buttons for a selected cryptocurrency.

    Args:
        cripto (str): The selected cryptocurrency (e.g., 'BTC', 'ETH').

    Returns:
        InlineKeyboardMarkup: A markup object with buttons to show 
        the current price or view statistics for the selected cryptocurrency, 
        as well as 'Back' and 'Main Menu' options.
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
    Generates an inline keyboard with buttons for navigation after displaying a photo or data.

    Args:
        cripto (str): The selected cryptocurrency (e.g., 'BTC', 'ETH').

    Returns:
        InlineKeyboardMarkup: A markup object with buttons to go back or return to the main menu.
    """
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Назад", callback_data=f'{cripto}_callback')],
            [InlineKeyboardButton("Главное меню", callback_data='start')],
        ]
    )
