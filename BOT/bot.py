"""
Telegram Bot for Cryptocurrency Analytics

This module implements the logic for a Telegram bot that provides cryptocurrency 
analytics. It allows users to interact through commands and buttons, fetches 
cryptocurrency data, and displays results in a user-friendly format.

Key Features:
- Display available cryptocurrencies to the user.
- Allow users to select cryptocurrencies and fetch analytics.
- Provide help information to guide users.
- Handle callback queries and maintain a seamless interaction.

Dependencies:
- `telegram` library for bot interaction.
- Custom modules for configuration, handlers, and keyboards.

Usage:
Run this module to start the bot. The bot listens for commands like `/start` and 
displays options in the chat interface.
"""

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext

from BOT.keyboards import get_main_menu_buttons
from BOT.config import bot, curr
from BOT.handlers import (
    handle_start,
    handle_back,
    handle_cripto_selection,
    handle_callback,
    handle_cripto_value
)

async def start(update: Update, context: CallbackContext):
    """
    Handle the /start command.

    Greets the user and displays the main menu with cryptocurrency options.

    Args:
        update (Update): The Telegram update object containing the user's message.
        context (CallbackContext): The context for managing bot state and data.

    Behavior:
        - Displays a message introducing the bot.
        - Presents a menu of cryptocurrency options.

    Example:
        User: /start
        Bot: Привет! Я бот для аналитики криптовалют. Выберите одну из криптовалют.
    """
    print(context)
    reply_markup = get_main_menu_buttons()

    if hasattr(update, 'callback_query') and update.callback_query:
        await update.callback_query.edit_message_text(
            "Привет! Я бот для аналитики криптовалют. Выберите одну из криптовалют",
            reply_markup=reply_markup
        )
    elif hasattr(update, 'message') and update.message:
        await update.message.reply_text(
            "Привет! Я бот для аналитики криптовалют. Выберите одну из криптовалют",
            reply_markup=reply_markup
        )
    else:
        print(f"Неизвестный тип обновления: {update}")

async def button_handler(update: Update, context: CallbackContext):
    """
    Handle button interactions from users.

    Processes user button clicks, interprets commands, and routes them 
    to appropriate handlers.

    Args:
        update (Update): The Telegram update object containing callback data.
        context (CallbackContext): The context for managing bot state and data.

    Callback Data Logic:
        - `start`: Calls the `handle_start` function.
        - `back`: Calls the `handle_back` function.
        - Cryptocurrency code (e.g., BTC): Calls `handle_cripto_selection`.
        - Callback (contains 'callback'): Calls `handle_callback`.
        - Cryptocurrency and action (e.g., BTC_info): Calls `handle_cripto_value`.
        - Default: Sends an "unknown command" message.

    Example:
        User clicks "BTC":
        - The bot calls `handle_cripto_selection` with BTC as the argument.
    """
    print(context)
    query = update.callback_query
    await query.answer()
    data = query.data

    handlers = {
        "start": handle_start,
        "back": handle_back,
        **{crypto: handle_cripto_selection for crypto in curr},
        'callback': handle_callback,
    }

    if handlers in data:
        if data in curr:
            await handlers[data](query, data)
        else:
            await handlers[data](query)
    elif "_" in data:
        crypto, time = data.split("_")
        await handle_cripto_value(time, query, crypto)
    else:
        await query.edit_message_text(
            text="Неизвестная команда. Попробуйте снова.",
            reply_markup=get_main_menu_buttons()
        )

async def help_command(update: Update):
    """
    Handle the /help command.

    Provides a list of available bot commands and their descriptions.

    Args:
        update (Update): The Telegram update object containing the user's message.

    Example:
        User: /help
        Bot: Вот что я умею:
             /start - Запустить бота
             /help - Показать справку
    """
    await update.message.reply_text(
        "Вот что я умею:\n/start - Запустить бота\n/help - Показать справку"
    )

def main():
    """
    Initialize and start the Telegram bot.

    Registers command and callback handlers and begins polling for updates.

    Behavior:
        - Registers the following handlers:
          * /start: Calls `start` function.
          * /help: Calls `help_command` function.
          * Button clicks: Calls `button_handler` function.
        - Starts polling for user interactions.

    Example:
        Run the script to launch the bot:
        $ python BOT/bot.py

    Output:
        The bot begins listening for user interactions.
        Prints "Бот запущен..." upon successful start.
    """
    app = ApplicationBuilder().token(bot).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
