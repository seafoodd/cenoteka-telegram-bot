import unittest
from unittest.mock import patch, MagicMock
from random import choice
from string import ascii_letters, digits
from src.utils.search_utils import search_products

class TestSearchProducts(unittest.TestCase):
    @patch('src.utils.search_utils.get_search_query')
    @patch('src.utils.search_utils.get_webpage')
    @patch('src.utils.search_utils.get_products')
    @patch('src.utils.search_utils.get_product_info')
    @patch('src.utils.search_utils.get_price_shop_list')
    @patch('src.utils.search_utils.send_message')
    def test_search_products_with_random_inputs(self, mock_send_message, mock_get_price_shop_list,
                                                mock_get_product_info,
                                                mock_get_products, mock_get_webpage, mock_get_search_query):
        # Arrange
        mock_message = MagicMock()
        mock_message.chat.id = 5166211222
        mock_get_webpage.return_value = "<html></html>"
        mock_product = MagicMock()
        mock_get_products.return_value = [mock_product]
        mock_get_product_info.return_value = ("product name", "discount")
        mock_get_price_shop_list.return_value = [("icon", "shop", "price")]

        # Generate 1000 random strings of length 10
        random_strings = [''.join(choice(ascii_letters + digits) for _ in range(10)) for _ in range(10)]

        for random_string in random_strings:
            mock_message.text = random_string
            mock_get_search_query.return_value = random_string

            # Act
            try:
                search_products(mock_message)
            except UnicodeEncodeError:
                self.fail(f"search_products raised UnicodeEncodeError when called with '{random_string}'")
            except Exception as e:
                self.fail(
                    f"search_products raised {type(e).__name__} with message {e} when called with '{random_string}'")

if __name__ == '__main__':
    unittest.main()