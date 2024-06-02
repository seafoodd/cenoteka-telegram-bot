from src.bot_init import bot
from src.utils.search_utils import search_products
from src.utils.message_utils import send_message

@bot.message_handler(commands=['start'])
def handle_start(message) -> None:
    send_message(message.chat.id, "Hello! I'm a bot that will help you find products on Cenoteka.")


@bot.message_handler(commands=['search'])
def handle_search_command(message) -> None:
    send_message(message.chat.id, "Enter the name of the product you want to search for.")


@bot.message_handler(commands=['help'])
def handle_help_command(message) -> None:
    send_message(message.chat.id, "To search for a product, enter the name of the product you want to find.")


@bot.message_handler(func=lambda message: True)
def handle_search(message):
    search_products(message)


if __name__ == '__main__':
    bot.infinity_polling()
