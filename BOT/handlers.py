"""
Bot Handlers Module

This module defines handlers for various bot interactions, including processing user input,
fetching data, and returning responses in the form of messages or media (e.g., plots and stats).

Functions:
    - handle_start: Handles the start command and resets the main menu.
    - handle_back: Navigates back to the main cryptocurrency selection menu.
    - handle_callback: Processes user selection and navigates to the action menu.
    - handle_cripto_value: Fetches cryptocurrency data (latest, history, or plots).
    - handle_cripto_selection: Handles the initial cryptocurrency selection.

Dependencies:
    - Requests to external APIs for data and analysis.
    - S3Client for image retrieval from cloud storage.
"""
from datetime import datetime
from io import BytesIO
import requests

from utils.s3_client import S3Client
from utils.make_request import make_request
from BOT.keyboards import (
    get_main_menu_buttons,
    get_time_buttons,
    get_action_buttons,
    callback_photo
)
from BOT.config import BASE_URL
from api.config import s3_key_id, s3_key_pass, bucket


async def handle_start(query):
    """
    Handles the /start command or callback.

    Args:
        query: Telegram query object containing user interaction data.

    Resets the interface and displays the main menu.
    """
    from BOT.bot import start  # pylint: disable=C0415
    if 'callback' in query.data:
        await start(query, None)
    else:
        await query.message.edit_reply_markup(reply_markup=None)
        await start(query, query.message)


async def handle_back(query):
    """
    Navigates back to the main cryptocurrency selection menu.

    Args:
        query: Telegram query object containing user interaction data.
    """
    await query.edit_message_text(
        text="Выберите криптовалюту:",
        reply_markup=get_main_menu_buttons()
    )


async def handle_callback(query, ans):
    """
    Navigates to the action menu for a selected cryptocurrency.

    Args:
        query: Telegram query object containing user interaction data.
        ans (str): User selection string, specifying the cryptocurrency.

    Modifies the reply markup to present action options for the selected cryptocurrency.
    """
    await query.message.edit_reply_markup(reply_markup=None)
    ans = ans.replace('_callback', '')
    await query.message.reply_text(
        text=f"Вы выбрали {ans}. Выберите действие:",
        reply_markup=get_action_buttons(ans)
    )


async def handle_cripto_value(time, query, crypto):
    """
    Fetches and processes cryptocurrency data.

    Args:
        time (str): Time range for data ('latest', 'day', 'hour', or 'history').
        query: Telegram query object containing user interaction data.
        crypto (str): Selected cryptocurrency.

    Depending on the time parameter, fetches either the latest price, historical data,
    or generates a plot. Returns the data and/or an image in response.
    """
    if time == "history":
        await query.edit_message_text(
            text=f"Вы выбрали {crypto}. Выберите период для анализа:",
            reply_markup=get_time_buttons(crypto)
        )
        return

    if time in ["day", "hour"]:
        try:
            await query.message.edit_reply_markup(reply_markup=None)
            stats = make_request(
                url=f'{BASE_URL}/analytics/{crypto}/{time}/USD/10')
            if not stats or 'error' in stats:
                raise ValueError("Ошибка при запросе аналитики данных")

            resp = make_request(url=f'{BASE_URL}/plot/{crypto}/{time}/USD/10')
            time_resp = resp['time_resp']
            time_resp = datetime.strptime(time_resp, '%a, %d %b %Y %H:%M:%S %Z')
            date_part = time_resp.strftime('%Y-%m-%d')
            time_part = time_resp.strftime('%H:%M')
            data = S3Client(
                aws_access_key_id=s3_key_id,
                aws_secret_access_key=s3_key_pass
            ).download_image(bucket=bucket,
                             bucket_file=f'{crypto}/{time}/{date_part}/{time_part}/plot.png')
            if not data:
                raise FileNotFoundError("Ошибка при загрузке изображения")

            buffer = BytesIO(data)
            buffer.seek(0)
            await query.message.reply_photo(
                photo=buffer,
                filename=f"{crypto}_{time}.png",
                caption="\n".join([
                    f"Статистика {crypto} за 10 {'дней' if time == 'day' else 'часов'}:",
                    f"Средняя стоимость: {stats.get('average', 'N/A')}",
                    f"Максимальная стоимость: {stats.get('max', 'N/A')}",
                    f"Медианная стоимость: {stats.get('median', 'N/A')}",
                    f"Минимальная стоимость: {stats.get('min', 'N/A')}"
                ]),
                reply_markup=callback_photo(crypto)
            )
        except ValueError as ve:
            await query.message.reply_text(f"Ошибка в данных: {ve}")
        except FileNotFoundError as fe:
            await query.message.reply_text(f"Ошибка при работе с файлами: {fe}")

    if time == 'latest':
        try:
            latest = make_request(url=f'{BASE_URL}/latest/{crypto}/USD')
            if not latest or 'error' in latest:
                raise ValueError("Ошибка при запросе данных")

            await query.edit_message_text(
                text=f"Текущий курс {crypto}: {latest[crypto]}",
                reply_markup=callback_photo(crypto)
            )
            return
        except requests.HTTPError as ve:
            await query.message.reply_text(f"Ошибка {ve}")


async def handle_cripto_selection(query, ans):
    """
    Handles cryptocurrency selection and navigates to the action menu.

    Args:
        query: Telegram query object containing user interaction data.
        ans (str): Selected cryptocurrency.
    """
    await query.edit_message_text(
        text=f"Вы выбрали {ans}. Выберите действие:",
        reply_markup=get_action_buttons(ans)
    )
