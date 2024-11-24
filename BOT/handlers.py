"""
bot hadler 
"""
from io import BytesIO
import requests

from utils.s3_client import S3Client
from utils.make_request import make_request
from BOT.keyboards import get_main_menu_buttons, \
                        get_time_buttons, get_action_buttons, callback_photo
from BOT.config import BASE_URL
from api.config import s3_key_id, s3_key_pass, bucket


async def handle_start(query):
    """
    return callback
    """
    from BOT.bot import start # pylint: disable=C0415
    if 'callback' in query.data:
        await start(query, None)
    else:
        await query.message.edit_reply_markup(reply_markup=None)
        await start(query, query.message)


async def handle_back(query):
    """
    to menu
    """
    await query.edit_message_text(
        text="Выберите криптовалюту:",
        reply_markup=get_main_menu_buttons()
    )


async def handle_callback(query, ans):
    """
    to menu
    """
    await query.message.edit_reply_markup(reply_markup=None)
    ans=ans.replace('_callback','')
    await query.message.reply_text(
        text=f"Вы выбрали {ans}. Выберите действие:",
        reply_markup=get_action_buttons(ans)
    )


async def handle_cripto_value(time, query, crypto):
    """
    get data 
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

            make_request(url=f'{BASE_URL}/plot/{crypto}/{time}/USD/10')
            data = S3Client(
                aws_access_key_id=s3_key_id,
                aws_secret_access_key=s3_key_pass
            ).download_image(bucket=bucket, bucket_file=f'{crypto}/{time}.png')
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
    spdgdsp
    """
    await query.edit_message_text(
        text=f"Вы выбрали {ans}. Выберите действие:",
        reply_markup=get_action_buttons(ans)
    )
