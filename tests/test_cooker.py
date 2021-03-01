import unittest
from unittest.mock import patch, Mock, MagicMock
from src.cooker import Cooker
from requests import status_codes, exceptions


class CookerTestSuites(unittest.TestCase):
    """
    tests the Cooker class.
    """
    def setUp(self):
        self.cooker = Cooker("https://viiiiiptips.blogspot.com/")
        with patch('src.cooker.requests', autospec=True) as mock_cooker_requests:
            self.cooker.get_recipe()
            self.cooker.sauce.content.return_value = ""

    def tearDown(self):
        self.cooker = None

    def test_get_recipe_is_called(self):
        with patch('src.cooker.requests') as mock_test_cooker_requests:
            self.cooker.get_recipe()
            mock_test_cooker_requests.get.assert_called()

    def test_get_recipe_response_is_ok(self):
        with patch('src.cooker.requests') as mock_cooker_requests:
            self.cooker.get_recipe()
            mock_cooker_requests.get.return_value = 200
            self.assertEqual(
                mock_cooker_requests.get.return_value,
                status_codes.codes.ok
            )

    def test_get_recipe_raises_request_exceptions(self):
        with patch('src.cooker.requests') as mock_cooker_requests:
            mock_cooker_requests.get.side_effect = exceptions.RequestException
            with self.assertRaises(exceptions.RequestException):
                self.cooker.get_recipe()

    def test_cook_recipe_is_called(self):
        with patch('src.cooker.bs') as mock_cooker_bs:
            self.cooker.cook_recipe()
            mock_cooker_bs.BeautifulSoup.assert_called()

    @patch('src.cooker.bs.BeautifulSoup.find', autospec=True,)
    def test_cook_recipe_returns_table(self, mocked_find, *args, **kwargs):
        mocked_find.return_value.name = "table"
        self.cooker.get_recipe()
        tbl = self.cooker.cook_recipe()
        mocked_find.assert_called()
        self.assertEqual(tbl.name, mocked_find.return_value.name)
