
import pickle
import unittest
from unittest.mock import (MagicMock, Mock, patch)

from requests import (exceptions, status_codes)
from src.cooker import (Cooker, bs)


class CookerTestSuites(unittest.TestCase):
    """
    CookerTestSuites: tests the Cooker class.

    Args:
        unittest (TestCase): A class whose instances are single test cases that are inherited.
    """
    def setUp(self):
        self.cooker = Cooker("https://viiiiiptips.blogspot.com/")

    def tearDown(self):
        self.cooker = None

    def test_get_recipe_is_called(self):
        with patch('src.cooker.requests') as mock_test_cooker_requests:
            self.cooker.get_sauce()
            mock_test_cooker_requests.get.assert_called()

    def test_get_recipe_response_is_ok(self):
        with patch('src.cooker.requests') as mock_cooker_requests:
            self.cooker.get_sauce()
            mock_cooker_requests.get.return_value = 200
            self.assertEqual(
                mock_cooker_requests.get.return_value,
                status_codes.codes.ok
            )

    def test_get_recipe_raises_request_exceptions(self):
        with patch('src.cooker.requests') as mock_cooker_requests:
            mock_cooker_requests.get.side_effect = exceptions.RequestException
            with self.assertRaises(exceptions.RequestException):
                self.cooker.get_sauce()

    def test_cook_recipe_is_called(self):
        with patch('src.cooker.requests') as mock_cooker_requests:
            self.cooker.get_sauce()
        with patch('src.cooker.bs') as mock_cooker_bs:
            self.cooker.cook_sauce()
            mock_cooker_bs.BeautifulSoup.assert_called()

    def test_cook_recipe_with_requests_mocked(self):
        with patch('src.cooker.requests', autospec=True, spec_set=True) as mock_requests:
            mock_requests.side_effect = None
            f = open('somethingsomething.xyz', 'rb')
            mock_requests.get.return_value = pickle.load(f)
            f.close()

            self.cooker.get_sauce()
            res = self.cooker.cook_sauce()
            self.assertIsInstance(res, bs.element.Tag)
            mock_requests.get.assert_called_with("https://viiiiiptips.blogspot.com/")
