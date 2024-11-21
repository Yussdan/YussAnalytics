import os
from io import BytesIO
import requests
from dotenv import load_dotenv

from utils.s3_client import S3Client, make_request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler , CallbackQueryHandler



load_dotenv()

bot = os.getenv("bot")
curr = ['BTC', 'ETH', 'TON']


def get_time_buttons(cripto):
    return [
        [InlineKeyboardButton("10 дней", callback_data=f'{cripto}_day')],
        [InlineKeyboardButton("10 часов", callback_data=f'{cripto}_hour')],
        [InlineKeyboardButton("Назад", callback_data='back')],
        [InlineKeyboardButton("Главное меню", callback_data='start')],
    ]

def get_main_menu_buttons():
    return [[InlineKeyboardButton(cur, callback_data=f'{cur}') for cur in curr]]

async def start(update: Update, message=None):
    """
    Handles the /start command. Greets the user and displays cryptocurrency options.
    """
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(cur, callback_data=f'{cur}') for cur in curr]])

    if message:
        if message.text:
            await message.edit_text(
            "Привет! Я бот для аналитики криптовалют. Выберите одну из криптовалют",
            reply_markup=reply_markup
            )
        else:
            await message.reply_text(
            "Привет! Я бот для аналитики криптовалют. Выберите одну из криптовалют",
            reply_markup=reply_markup
            )
    elif update.message:
        await update.message.reply_text(
            "Привет! Я бот для аналитики криптовалют. Выберите одну из криптовалют",
            reply_markup=reply_markup
        )
    else:
        print("Ошибка: Нет доступного сообщения для отправки.")


async def button_handler(update: Update):
    # logic button
    query = update.callback_query
    await query.answer()
    ans = query.data

    if "start" in ans:
        if 'callback' in ans:
            await start(update, None)
        else:
            await start(update, query.message)
        return

    if ans == "back":
        await query.edit_message_text(
            text="Выберите криптовалюту:",
            reply_markup=InlineKeyboardMarkup(get_main_menu_buttons())
        )
        return

    if ans in curr:
        await query.edit_message_text(
            text=f"Вы выбрали {ans}. Выберите действие:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Показать текущий курс", callback_data=f'{ans}_latest')],
                    [InlineKeyboardButton("Статистика", callback_data=f'{ans}_history')],
                    [InlineKeyboardButton("Назад", callback_data='back')],
                    [InlineKeyboardButton("Главное меню", callback_data='start')],
                ]
            )
        )
        return
    if 'callback' in ans:
        await query.message.edit_reply_markup(reply_markup=None)
        ans=ans.replace('_callback','')
        await query.message.reply_text(
            text=f"Вы выбрали {ans}. Выберите действие:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Показать текущий курс", callback_data=f'{ans}_latest')],
                    [InlineKeyboardButton("Статистика", callback_data=f'{ans}_history')],
                    [InlineKeyboardButton("Назад", callback_data='back')],
                    [InlineKeyboardButton("Главное меню", callback_data='start')],
                ]
            )
        )
        return

    if "_" in ans:
        cripto, action = ans.split("_")

        if action == "history":
            await query.edit_message_text(
                text=f"Вы выбрали {cripto}. Выберите период для анализа:",
                reply_markup=InlineKeyboardMarkup(get_time_buttons(cripto))
            )
            return

    if action in ["day", "hour"]:
        try:
            await query.message.edit_reply_markup(reply_markup=None)
            stats = make_request(url=f'http://127.0.0.1:5000/{cripto}/analytics/USD/{action}/10')
            if not stats or 'error' in stats:
                raise ValueError("Ошибка при запросе аналитики данных")

            make_request(url=f'http://127.0.0.1:5000/{cripto}/plot/USD/{action}/10')
            data = S3Client().download_image(
                bucket='bucket-2490b3', bucket_file=f'{cripto}/{action}.png')
            if not data:
                raise FileNotFoundError("Ошибка при загрузке изображения")

            buffer = BytesIO(data)
            buffer.seek(0)
            await query.message.reply_photo(
                photo=buffer,
                filename=f"{cripto}_{action}.png",
                caption="\n".join([
                    f"Статистика {cripto} за 10 {'дней' if action == 'day' else 'часов'}:",
                    f"Средняя стоимость: {stats.get('average', 'N/A')}",
                    f"Максимальная стоимость: {stats.get('max', 'N/A')}",
                    f"Медианная стоимость: {stats.get('median', 'N/A')}",
                    f"Минимальная стоимость: {stats.get('min', 'N/A')}"
                ]),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Назад", callback_data=f'{cripto}_callback')],
                    [InlineKeyboardButton("Главное меню", callback_data='start')],
                ])
            )
        except ValueError as ve:
            await query.message.reply_text(f"Ошибка в данных: {ve}")
        except FileNotFoundError as fe:
            await query.message.reply_text(f"Ошибка при работе с файлами: {fe}")


        if action == "latest":
            try:
                latest = make_request(url=f'http://127.0.0.1:5000/{cripto}/latest/USD')
                if not latest or 'error' in latest:
                    raise ValueError("Ошибка при запросе данных")

                await query.edit_message_text(
                    text=f"Текущий курс {cripto}: {latest[cripto]}",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Назад", callback_data=f'{cripto}_callback')],
                        [InlineKeyboardButton("Главное меню", callback_data='start')],
                    ])
                )
                return

            except requests.HTTPError as ve:
                await query.message.reply_text(f"Ошибка {ve}")
async def help_command(update: Update):
    # Handle start action logic
    await update.message.reply_text(
        "Вот что я умею:\n/start - Запустить бота\n/help - Показать справку")

def main():
    app = ApplicationBuilder().token(bot).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
