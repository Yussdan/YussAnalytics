"""
this module is base config bot
"""
import os
from dotenv import load_dotenv

load_dotenv()
bot = os.getenv("bot")
curr = ['BTC', 'ETH', 'TON']
BASE_URL = 'http://127.0.0.1:5000/'
