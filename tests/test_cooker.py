import unittest
import pickle
from unittest.mock import patch, Mock, MagicMock
from src.cooker import Cooker
from requests import status_codes, exceptions


class CookerTestSuites(unittest.TestCase):
    """
    tests the Cooker class.
    """
    def setUp(self):
        self.cooker = Cooker("https://viiiiiptips.blogspot.com/")

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
            self.cooker.get_recipe()
            self.cooker.cook_recipe()
            mock_cooker_bs.BeautifulSoup.assert_called()

    def test_cook_recipe_with_requests_mocked(self):
        with patch('src.cooker.requests', autospec=True, spec_set=True) as mock_requests:
            mock_requests.side_effect = None
            mock_requests.get.return_value = pickle.load(
                open(
                    'somethingsomething.xyz',
                    'rb'
                )
            )
            self.cooker.get_recipe()
            self.cooker.cook_recipe()
            self.assertIsInstance(self.cooker.meaty_list, list)
            self.assertGreater(len(self.cooker.meaty_list), 0)
            dict_1st = self.cooker.meaty_list.pop(0)
            self.assertIsInstance(dict_1st, dict)
            self.assertIn("teams", dict_1st.keys())
            mock_requests.get.assert_called_with("https://viiiiiptips.blogspot.com/")
