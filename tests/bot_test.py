"""
Tests for the Telegram bot in CI.

This module contains tests for verifying the functionality of the bot's main commands 
and button handlers. The tests cover the start command and button click handlers.

Technologies used:
- pytest for organizing tests.
- unittest.mock for creating mock objects and replacing dependencies.
- Async tests using pytest.mark.asyncio.

Functions being tested:
- start: Handles the /start command, sending a welcome message 
            and a cryptocurrency selection keyboard.
- button_handler: Handles button presses and triggers 
            the corresponding handler for the selected action.
"""
from unittest.mock import AsyncMock, patch
import pytest
from BOT.bot import start, button_handler


@pytest.mark.asyncio
async def test_start_command():
    """
    Tests the /start command handler.

    This test checks that when the /start command is invoked, the bot sends a 
    welcome message with a keyboard for selecting a cryptocurrency.

    The update and context objects are mocked, and the InlineKeyboardMarkup and 
    InlineKeyboardButton are patched to simulate the keyboard.
    """
    mock_update = AsyncMock()
    mock_context = AsyncMock()

    mock_update.callback_query = AsyncMock()
    mock_update.callback_query.edit_message_text = AsyncMock()

    mock_update.message = AsyncMock()
    mock_update.message.reply_text = AsyncMock()

    with patch("BOT.keyboards.InlineKeyboardMarkup") as mock_markup, \
         patch("BOT.keyboards.InlineKeyboardButton") as mock_button:
        mock_markup.return_value = "mock_markup"
        mock_button.return_value = "mock_button"

        await start(mock_update, mock_context)

        mock_update.callback_query.edit_message_text.assert_called_once_with(
            "Привет! Я бот для аналитики криптовалют. Выберите одну из опций.",
            reply_markup="mock_markup"
        )

        mock_update.callback_query = None
        await start(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with(
            "Привет! Я бот для аналитики криптовалют. Выберите одну из опций.",
            reply_markup="mock_markup"
        )

@pytest.mark.asyncio
async def test_button_handler():
    """
    Tests the button press handler.

    This test verifies that when a button is pressed, the bot correctly handles 
    the button click and calls the appropriate handler depending on the button data.

    The test mocks different button actions, such as 'start', 'back', cryptocurrency selection, 
    and callback actions, ensuring that the correct handler function is invoked for each.
    """
    mock_update = AsyncMock()
    mock_context = AsyncMock()

    mock_update.callback_query = AsyncMock()
    mock_update.callback_query.answer = AsyncMock()

    with patch("BOT.bot.handle_start", new_callable=AsyncMock) as mock_handle_start:
        mock_update.callback_query.data = "start"
        await button_handler(mock_update, mock_context)
        mock_handle_start.assert_called_once_with(mock_update.callback_query)

    with patch("BOT.bot.handle_back", new_callable=AsyncMock) as mock_handle_back:
        mock_update.callback_query.data = "back"
        await button_handler(mock_update, mock_context)
        mock_handle_back.assert_called_once_with(mock_update.callback_query)

    with patch("BOT.bot.handle_cripto_selection",
                new_callable=AsyncMock) as mock_handle_cripto_selection:
        mock_update.callback_query.data = "BTC"
        await button_handler(mock_update, mock_context)
        mock_handle_cripto_selection.assert_called_once_with(
            mock_update.callback_query, mock_update.callback_query.data)

    with patch("BOT.bot.handle_cripto_value", new_callable=AsyncMock) as mock_cripto_value:
        mock_update.callback_query.data = "BTC_history"
        await button_handler(mock_update, mock_context)
        mock_cripto_value.assert_called_once_with('history', mock_update.callback_query, 'BTC')

    with patch("BOT.bot.handle_callback", new_callable=AsyncMock) as mock_handle_callback:
        mock_update.callback_query.data = "BTC_callback"
        await button_handler(mock_update, mock_context)
        mock_handle_callback.assert_called_once_with(mock_update.callback_query, "BTC_callback")
