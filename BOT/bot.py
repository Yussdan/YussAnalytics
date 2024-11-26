"""
Telegram Bot for Cryptocurrency Analytics

This module implements a Telegram bot for cryptocurrency analytics, providing 
interactive commands and button-based navigation.

Key Features:
- Display and analyze cryptocurrencies.
- Interactive menu navigation with inline buttons.
- User-friendly guidance with commands like /start and /help.

Dependencies:
- `python-telegram-bot` library for bot interaction.
- Custom modules for configuration, handlers, and keyboards.

Usage:
Run this script to launch the bot.
"""

from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext
)
from BOT.keyboards import get_main_menu_buttons
from BOT.config import bot, curr
from BOT.handlers import (
    handle_start, handle_back, handle_cripto_selection, handle_callback,
    handle_cripto_value, handle_new, handle_analytics, handle_mailing
)

# Command Handlers
async def start(update: Update, context: CallbackContext):
    """
    Handle the /start command to greet users and display the main menu.

    Args:
        update (Update): Telegram update object with user data.
        context (CallbackContext): Context for managing bot state.
    """
    print(context)
    reply_markup = get_main_menu_buttons()
    message_text = "Привет! Я бот для аналитики криптовалют. Выберите одну из опций."

    if update.callback_query:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup)
    elif update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup)
    else:
        print(f"Неизвестный тип обновления: {update}")

async def help_command(update: Update, context: CallbackContext):
    """
    Handle the /help command to provide bot usage instructions.

    Args:
        update (Update): Telegram update object with user data.
        context (CallbackContext): Context for managing bot state.
    """
    print(context)
    help_text = (
        "Вот что я умею:\n"
        "/start - Запустить бота\n"
        "/help - Показать справку"
    )
    if update.message:
        await update.message.reply_text(help_text)

# Callback Query Handlers
async def button_handler(update: Update, context: CallbackContext):
    """
    Process button clicks and route to appropriate handlers.

    Args:
        update (Update): Telegram update object containing callback data.
        context (CallbackContext): Context for managing bot state.
    """
    query = update.callback_query
    await query.answer()
    data = query.data
    print(context)

    handlers = {
        "menu": handle_start,
        "return": handle_back,
        **{crypto: handle_cripto_selection for crypto in curr},
        "callback": handle_callback,
        "help": help_command,
        "news": handle_new,
        "mailing": handle_mailing,
        "analytics": handle_analytics,
    }

    if data in curr or "callback" in data:
        handler = handlers.get(data, handlers["callback"])
        await handler(query, data)
    elif data in handlers:
        await handlers[data](query)
    elif "_" in data:
        crypto, time = data.split("_")
        await handle_cripto_value(time, query, crypto)
    else:
        await query.edit_message_text(
            text="Неизвестная команда. Попробуйте снова.",
            reply_markup=get_main_menu_buttons()
        )

# Main Function
def main():
    """
    Initialize and start the Telegram bot.

    Registers command and callback handlers, then starts polling.
    """
    app = ApplicationBuilder().token(bot).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
