from dotenv import load_dotenv
import os
import time
import telebot
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from transliterate import translit

load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

MESSAGE_COOLDOWN = float(os.getenv('MESSAGE_COOLDOWN'))
BAN_TIME = float(os.getenv('BAN_TIME'))

last_message_time = {}
message_count_when_limit_reached = {}
banned_until = {}


@bot.message_handler(commands=['start'])
def handle_start(message) -> None:
    bot.send_message(message.chat.id, "Привет! Я бот, который поможет вам найти товары на Cenoteka.")


@bot.message_handler(commands=['search'])
def handle_search_command(message) -> None:
    bot.send_message(message.chat.id, "Введите название товара, который хотите найти.")


@bot.message_handler(commands=['help'])
def handle_help_command(message) -> None:
    bot.send_message(message.chat.id, "Для поиска товара введите название товара, который хотите найти.")


def get_icon(price_div):
    if 'promo_price' in price_div['class']:
        if 'cheapest' in price_div['class']:
            return '⭐'
        return '🔥'
    if 'cheapest' in price_div['class']:
        return '💵'
    return ''


def get_search_query(message):
    # transliterating the message to latin
    return translit(message.text, 'ru', reversed=True)


def get_webpage(url):
    # adding User-Agent to avoid 403 error
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urlopen(req).read()


def get_products(soup):
    # getting all products from the html page and returning only the first 8 products
    return soup.select('div.product_wrap')[:8]


def get_product_info(product):
    product_name_div = product.select_one('div.product_info')
    product_name = product_name_div.text

    discount_div = product.select_one('div.product_savings')
    discount = discount_div.text if discount_div else "No discount"

    return product_name, discount


def get_price_shop_list(product):
    price_shop_divs = product.select_one('div.product_info_wrap').contents
    price_shop_list = []
    for div in price_shop_divs:
        img = div.select_one('img')
        shop = img['alt'] if img else 'No shop'
        price_div = div.select_one('div.product_price')

        if price_div:
            price = price_div.text if price_div else 'No price'
            icon = get_icon(price_div)
            price_shop_list.append((icon if icon else "-----", shop, price))

    return price_shop_list


def handle_spamming(user_id) -> bool:
    # if the user is banned, ignore their messages
    if user_id in banned_until and banned_until[user_id] > time.time():
        bot.send_message(user_id,
                         f"До окончания блокировки осталось {int(banned_until[user_id] - time.time())} секунд.")
        return False

    # rate limiting
    if user_id in last_message_time and time.time() - last_message_time[user_id] < MESSAGE_COOLDOWN:
        bot.send_message(user_id,
                         f"Подождите, пока не прошло {MESSAGE_COOLDOWN} секунд с момента последнего сообщения.")
        message_count_when_limit_reached[user_id] = message_count_when_limit_reached.get(user_id, 0) + 1

        # If the user has sent too many messages in the cooldown period, ban them for a certain time
        if message_count_when_limit_reached[user_id] > 5:  # Adjust this value as needed
            banned_until[user_id] = time.time() + BAN_TIME
            bot.send_message(user_id,
                             f"Вы были заблокированы на {BAN_TIME} секунд из-за слишком большого количества сообщений.")

        return False
    return True


@bot.message_handler(func=lambda message: True)
def handle_search(message):
    user_id = message.chat.id

    if handle_spamming(user_id) is False:
        return

    last_message_time[user_id] = time.time()
    message_count_when_limit_reached[user_id] = 0

    try:
        # getting a search query from user
        search_query = get_search_query(message)
        url = f'https://cenoteka.rs/pretraga/?s={search_query}'

        # getting html page
        webpage = get_webpage(url)

        # parsing html page
        soup = BeautifulSoup(webpage, "html.parser")

        # getting all products from html page
        products = get_products(soup)

        # if there are no products, send the message to the user and print message
        if not products:
            bot.send_message(message.chat.id, "Ничего не найдено.")
            print("Ничего не найдено.")
            return

        # getting product name, discount and prices from each product
        message_text = ''
        for product in products:

            # getting product name, discount and prices
            product_name, discount = get_product_info(product)
            price_shop_list = get_price_shop_list(product)

            # adding product name, discount and prices to the message
            message_text += f'Товар: {product_name.strip()}\n'
            message_text += f'Скидка: {discount.strip()}\n'
            for icon, shop, price in price_shop_list:
                message_text += f'{icon} {shop}, Цена: {price}\n'

            message_text += '\n' * 2

        # sending the message to the user and printing the message to the console
        print(message_text)
        bot.send_message(message.chat.id, message_text)

    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка.")
        print(e)


if __name__ == '__main__':
    bot.infinity_polling()
