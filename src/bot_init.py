from dotenv import load_dotenv
import os
import telebot

load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

MESSAGE_COOLDOWN = float(os.getenv('MESSAGE_COOLDOWN'))
BAN_TIME = float(os.getenv('BAN_TIME'))

last_message_time = {}
message_count_when_limit_reached = {}
banned_until = {}
