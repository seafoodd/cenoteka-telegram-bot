from bot_init import bot
from utils.search_utils import search_products
from utils.message_utils import send_message


@bot.message_handler(commands=['start', 'menu'])
def handle_start(message) -> None:
    instructions = (
        "Hello! I'm a bot that will help you find products on Cenoteka.\n"
        "Here's how you can use me:\n"
        "- To search for a product, simply type the name of the product.\n"
        "- If you need help, type /help.\n"
        "Happy shopping!"
    )
    send_message(message.chat.id, instructions)


@bot.message_handler(commands=['help', 'search'])
def handle_help_command(message) -> None:
    send_message(message.chat.id, "To search for a product, enter the name of the product you want to find.")


@bot.message_handler(func=lambda message: True)
def handle_search(message):
    search_products(message)


if __name__ == '__main__':
    bot.infinity_polling()
