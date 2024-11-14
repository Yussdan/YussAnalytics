import requests
from dotenv import load_dotenv
import os
from PIL import Image
from io import BytesIO

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

load_dotenv()

bot = os.getenv("bot")
curr = ['BTC', 'ETH', 'USDT']


def make_request(url):
    response = requests.get(url)
    return response.json() if response.status_code == 200 else f"Ошибка при получении данных. Попробуйте позже."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, message=None):
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(cur, callback_data=f'{cur}') for cur in curr]])
    
    if message:
        await message.edit_text(
            "Привет! Я бот для аналитики криптовалют. Выберите одну из криптовалют или нажмите /help.",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "Привет! Я бот для аналитики криптовалют. Выберите одну из криптовалют или нажмите /help.",
            reply_markup=reply_markup
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ans = query.data

    if ans in [f'{cur}_{time}' for cur in curr for time in ['latest', 'history', 'day', 'hour']]:
        cripto, action = ans.split('_')
        
        if action == 'history':
            await query.edit_message_text(
                text=f"Вы выбрали {cripto}. Выберите период для анализа:",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Статистика по цене за прошедние 10 дней", callback_data=f'{cripto}_day')],
                        [InlineKeyboardButton("Статистика по цене за последние 10 часов", callback_data=f'{cripto}_hour')],
                        [InlineKeyboardButton("Назад", callback_data='back')]
                    ]
                )
            )

        if action in ['day', 'hour']:
                stats = make_request(f'http://127.0.0.1:5000/{cripto}/analytics/USD/{action}/10')
                await query.edit_message_text(
                    text="\n".join([
                    "Статистика стоимости :",
                    f"Средняя стоимость за данный период : {stats['average']}",
                    f"Максимальная стоимость за данный период : {stats['max']}",
                    f"Медианная стоимость за данный период : {stats['median']}",
                    f"Минимальная стоимость за данный период : {stats['min']}"]))

                image_file = BytesIO()
                Image.open(BytesIO(requests.get(f'http://127.0.0.1:5000/{cripto}/plot/USD/{action}/10').content)).save(image_file, format="PNG")
                image_file.seek(0) 
                await query.message.reply_photo(photo=InputFile(image_file, filename="crypto_plot.png"))

        if action == 'latest':
            await query.edit_message_text(text=make_request(f'http://127.0.0.1:5000/{cripto}/latest/USD')[cripto])

    elif ans in curr:
        await query.edit_message_text(
            text=f"Вы выбрали {ans}. Выберите действие:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Показать текущий курс", callback_data=f'{ans}_latest')],
                    [InlineKeyboardButton("Статистику", callback_data=f'{ans}_history')],
                    [InlineKeyboardButton("Назад", callback_data='back')]
                ]
            )
        )

    else:
        await start(update, context, message=query.message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Вот что я умею:\n/start - Запустить бота\n/help - Показать справку")

def main():
    app = ApplicationBuilder().token(bot).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()