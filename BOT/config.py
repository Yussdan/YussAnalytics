"""
Bot Configuration Module

This module defines the basic configuration for the cryptocurrency analytics bot.
It handles environment variables and defines key constants used throughout the bot's logic.

Features:
- Loads environment variables using `dotenv`.
- Provides the bot token for Telegram API authentication.
- Lists supported cryptocurrencies.
- Defines the base URL for API requests.

Attributes:
    bot (str): Telegram bot token, loaded from the `.env` file.
    curr (list of str): Supported cryptocurrencies (e.g., 'BTC', 'ETH', 'TON').
    BASE_URL (str): Base URL for the backend API to fetch data and analytics.

Usage:
    Import this module to access the bot token, supported currencies, and base API URL.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram bot token
bot = os.getenv("bot")

# Supported cryptocurrencies
curr = ['BTC', 'ETH', 'TON']

# Base URL for API requests
BASE_URL = 'http://127.0.0.1:5000/'
