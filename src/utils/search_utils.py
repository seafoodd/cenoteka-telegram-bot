from urllib.request import Request, urlopen
from transliterate import translit
from bs4 import BeautifulSoup
from bot_init import last_message_time, message_count_when_limit_reached
from .message_utils import handle_spamming, send_message
from .logging_utils import send_search_log, configure_logging
import time

configure_logging()


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


def search_products(message):
    user_id = message.chat.id
    if handle_spamming(message) is False:
        return

    last_message_time[user_id] = time.time()
    message_count_when_limit_reached[user_id] = 0

    try:
        # getting a search query from user
        search_query = get_search_query(message)

        url = f'https://cenoteka.rs/pretraga/?s={search_query}'
        send_search_log(message, search_query)

        # getting html page
        webpage = get_webpage(url)

        # parsing html page
        soup = BeautifulSoup(webpage, "html.parser")

        # getting all products from html page
        products = get_products(soup)

        # if there are no products, send the message to the user and print message
        if not products:
            send_message(message.chat.id, "Nothing found.")
            print("Nothing found.")
            return

        # getting product name, discount and prices from each product
        message_text = ''
        for product in products:

            # getting product name, discount and prices
            product_name, discount = get_product_info(product)
            price_shop_list = get_price_shop_list(product)

            # adding product name, discount and prices to the message
            message_text += f'Product: {product_name.strip()}\n'
            message_text += f'Discount: {discount.strip()}\n'
            for icon, shop, price in price_shop_list:
                message_text += f'{icon} {shop}, Price: {price}\n'

            message_text += '\n' * 2

        # sending the message to the user and printing the message to the console
        send_message(message.chat.id, message_text)

    except Exception as e:
        send_message(message.chat.id, "An error has occurred.")
        print(e)
