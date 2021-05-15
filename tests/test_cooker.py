
import pickle
from typing import Dict, List
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
        self.vip_cooker = Cooker("https://xxviptips.blogspot.com/")
        self.combo_cooker = Cooker("https://xxcombotips.blogspot.com/")
        self.gold_cooker = Cooker("https://xxgoldtips.blogspot.com/")
        self.history_cooker = Cooker("https://hsitoriiquebet.blogspot.com/")

    def tearDown(self):
        self.vip_cooker = None
        self.combo_cooker = None
        self.gold_cooker = None
        self.history_cooker = None

    def test_get_recipe_is_called(self):
        with patch('src.cooker.requests') as mock_test_cooker_requests:
            # self.vip_cooker.get_sauce()
            # self.combo_cooker.get_sauce()
            # self.gold_cooker.get_sauce()
            self.history_cooker.get_sauce()
            mock_test_cooker_requests.get.assert_called()

    def test_get_recipe_response_is_ok(self):
        with patch('src.cooker.requests') as mock_cooker_requests:
            # self.vip_cooker.get_sauce()
            # self.combo_cooker.get_sauce()
            # self.gold_cooker.get_sauce()
            self.history_cooker.get_sauce()
            mock_cooker_requests.get.return_value = 200
            self.assertEqual(
                mock_cooker_requests.get.return_value,
                status_codes.codes.ok
            )

    def test_get_recipe_raises_request_exceptions(self):
        with patch('src.cooker.requests') as mock_cooker_requests:
            mock_cooker_requests.get.side_effect = exceptions.RequestException
            with self.assertRaises(exceptions.RequestException):
                # self.vip_cooker.get_sauce()
                # self.combo_cooker.get_sauce()
                # self.gold_cooker.get_sauce()
                self.history_cooker.get_sauce()

    def test_cook_recipe_is_called(self):
        with patch('src.cooker.requests') as mock_cooker_requests:
            # self.vip_cooker.get_sauce()
            # self.combo_cooker.get_sauce()
            # self.gold_cooker.get_sauce()
            self.history_cooker.get_sauce()
        with patch('src.cooker.bs') as mock_cooker_bs:
            # self.vip_cooker.cook_sauce()
            # self.combo_cooker.cook_sauce()
            # self.gold_cooker.cook_sauce()
            self.history_cooker.cook_sauce()
            mock_cooker_bs.BeautifulSoup.assert_called()

    def test_cook_recipe_with_requests_mocked(self):
        with patch('src.cooker.requests', autospec=True, spec_set=True) as mock_requests:
            agent_str = "Mozilla/5.0 (Linux; Android 10; SM-A207F Build/QP1A.190711.020) " + \
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.82 Mobile Safari/537.36 OPT/2.9"
            req_headers = {
                "User-Agent": agent_str
            }

            mock_requests.side_effect = None
            f = open('data/pickled_data/pickled_viptips.xyz', 'rb')
            g = open('data/pickled_data/pickled_combotips.xyz', 'rb')
            h = open('data/pickled_data/pickled_goldtips.xyz', 'rb')
            j = open('data/pickled_data/pickled_history.xyz', 'rb')

            mock_requests.get.return_value = pickle.load(f)
            f.close()
            res = self.vip_cooker.cook_sauce()
            mock_requests.get.assert_called_with("https://xxviptips.blogspot.com/", headers=req_headers)

            # mock_requests.get.return_value = pickle.load(g)
            # g.close()
            # res1 = self.combo_cooker.cook_sauce()
            # mock_requests.get.assert_called_with("https://xxcombotips.blogspot.com/", headers=req_headers)

            mock_requests.get.return_value = pickle.load(h)
            h.close()
            res2 = self.gold_cooker.cook_sauce()
            mock_requests.get.assert_called_with("https://xxgoldtips.blogspot.com/", headers=req_headers)

            mock_requests.get.return_value = pickle.load(j)
            j.close()
            res3 = self.history_cooker.cook_sauce()
            mock_requests.get.assert_called_with("https://hsitoriiquebet.blogspot.com/", headers=req_headers)

            self.assertIsInstance(res, List)
            # self.assertIsInstance(res1, List)
            self.assertIsInstance(res2, List)
            self.assertIsInstance(res3, List)

            one_res = res.pop()
            # two_res = res1.pop()
            three_res = res2.pop()
            four_res = res3.pop()

            # self.assertIsInstance(one_res, List)
            self.assertIsInstance(one_res, Dict)
            # self.assertIsInstance(two_res, List)
            # self.assertIsInstance(three_res, List)
            self.assertIsInstance(three_res, Dict)
            # self.assertIsInstance(four_res, List)
            self.assertIsInstance(four_res, Dict)
