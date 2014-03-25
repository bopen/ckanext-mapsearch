import unittest
from time import sleep

from selenium import webdriver

from helpers import wait_for_ajaxes_to_complete, get_result_stats
from helpers import display_javascript_notice, search_for_text
from helpers import get_displayed_title_word
from tests import MAPSEARCH_INSTANCE_URL
from helpers import get_driver


class TestExtents(unittest.TestCase):

    def setUp(self):
        try:
            self.driver = get_driver('firefox')
        except:
            self.driver = get_driver('chrome')
        self.driver.get(MAPSEARCH_INSTANCE_URL)
        display_javascript_notice(
            self.driver, "running test: {0}".format(self._testMethodName))
        wait_for_ajaxes_to_complete(self.driver)

    def tearDown(self):
        self.driver.quit()

    def _current_total(self):
        return get_result_stats(self.driver)['normal']

    def test_search_for_title(self):
	sleep(1)
        initial_total = self._current_total()
        search_for_text(self.driver, "title:" + get_displayed_title_word(self.driver))
	sleep(1)
        searched_total = self._current_total()
        self.assertNotEqual(initial_total, searched_total)

    def test_free_text_search(self):
	sleep(1)
        initial_total = self._current_total()
        search_for_text(self.driver, get_displayed_title_word(self.driver))
	sleep(1)
        searched_total = self.driver.find_element_by_id("current_total_display").text
        self.assertNotEqual(initial_total, searched_total)

    def test_combined_search_for_free_text_and_title(self):
	sleep(1)
        initial_total = self._current_total()
        first_q = "title:" + get_displayed_title_word(self.driver)
        search_for_text(self.driver, first_q)
        between_total = self._current_total()
        sleep(1)
        search_for_text(self.driver,
                        "title:" + get_displayed_title_word(self.driver) + " " + 
                        get_displayed_title_word(self.driver))
        final_total = self._current_total()
        self.assertNotEqual(initial_total, between_total)
        self.assertNotEqual(initial_total, final_total)
        self.assertTrue(initial_total >= between_total)
        self.assertTrue(between_total >= final_total)
