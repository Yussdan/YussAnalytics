"""
This module contains the implementation of the Telegram bot for cryptocurrency analytics.
It handles user interaction, fetches data, and displays it in various formats.
"""

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext

from BOT.keyboards import get_main_menu_buttons
from BOT.config import bot, curr
from BOT.handlers import handle_start, handle_back, \
                        handle_cripto_selection, handle_callback, handle_cripto_value


async def start(update: Update, context: CallbackContext):
    """
    Handles the /start command. Greets the user and displays cryptocurrency options.
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
        print(type(update))
        print(f"Неизвестный тип обновления: {update}")


async def button_handler(update: Update, context: CallbackContext):
    """
    button logic
    """
    print(context)
    query = update.callback_query
    await query.answer()
    ans = query.data

    if "start" in ans:
        await handle_start(query)
        return

    if ans == "back":
        await handle_back(query)
        return

    if ans in curr:
        await handle_cripto_selection(query, ans)
        return

    if 'callback' in ans:
        await handle_callback(query, ans)
        return

    if "_" in ans:
        cripto, action = ans.split("_")
        await handle_cripto_value(action, query, cripto)

    else:
        await query.edit_message_text(
            text="Неизвестная команда. Попробуйте снова.",
            reply_markup=get_main_menu_buttons()
        )
        return

async def help_command(update: Update):
    """
    /help logic
    """
    await update.message.reply_text(
        "Вот что я умею:\n/start - Запустить бота\n/help - Показать справку")

def main():
    """
    Bot initialization and polling
    """
    app = ApplicationBuilder().token(bot).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
