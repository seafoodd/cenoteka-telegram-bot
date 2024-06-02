from bot_init import bot
from utils.search_utils import search_products
from src.utils.message_utils import send_message


@bot.message_handler(commands=['start'])
def handle_start(message) -> None:
    send_message(message.chat.id, "Привет! Я бот, который поможет вам найти товары на Cenoteka.")


@bot.message_handler(commands=['search'])
def handle_search_command(message) -> None:
    send_message(message.chat.id, "Введите название товара, который хотите найти.")


@bot.message_handler(commands=['help'])
def handle_help_command(message) -> None:
    send_message(message.chat.id, "Для поиска товара введите название товара, который хотите найти.")


@bot.message_handler(func=lambda message: True)
def handle_search(message):
    search_products(message)


if __name__ == '__main__':
    bot.infinity_polling()
