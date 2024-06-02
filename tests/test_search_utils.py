import unittest
from unittest.mock import patch, MagicMock
from src.utils.search_utils import search_products


class TestSearchProducts(unittest.TestCase):
    @patch('src.utils.search_utils.get_search_query')
    @patch('src.utils.search_utils.get_webpage')
    @patch('src.utils.search_utils.get_products')
    @patch('src.utils.search_utils.get_product_info')
    @patch('src.utils.search_utils.get_price_shop_list')
    @patch('src.utils.search_utils.send_message')
    def test_search_products(self, mock_send_message, mock_get_price_shop_list, mock_get_product_info,
                             mock_get_products, mock_get_webpage, mock_get_search_query):
        # Arrange
        mock_message = MagicMock()
        mock_message.chat.id = 123
        mock_get_search_query.return_value = "test query"
        mock_get_webpage.return_value = "test webpage"
        mock_get_products.return_value = ["product1", "product2"]
        mock_get_product_info.return_value = ("product name", "discount")
        mock_get_price_shop_list.return_value = [("icon", "shop", "price")]

        # Act
        search_products(mock_message)

        # Assert
        mock_get_search_query.assert_called_once_with(mock_message)
        mock_get_webpage.assert_called_once_with('https://cenoteka.rs/pretraga/?s=test query')
        mock_get_products.assert_called_once_with("test webpage")
        mock_get_product_info.assert_any_call("product1")
        mock_get_product_info.assert_any_call("product2")
        mock_get_price_shop_list.assert_any_call("product1")
        mock_get_price_shop_list.assert_any_call("product2")
        mock_send_message.assert_called()


if __name__ == '__main__':
    unittest.main()
