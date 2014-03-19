import unittest
from time import sleep
from random import choice

from selenium import webdriver

from helpers import wait_for_ajaxes_to_complete, get_result_stats
from helpers import display_javascript_notice
from tests import MAPSEARCH_INSTANCE_URL


class TestExtents(unittest.TestCase):

    def setUp(self):
        try:
            self.driver = webdriver.Firefox()
        except:
            self.driver = webdriver.Chrome()
        self.driver.get(MAPSEARCH_INSTANCE_URL)
        display_javascript_notice(
            self.driver, "running test: {0}".format(self._testMethodName))
        wait_for_ajaxes_to_complete(self.driver)

    def tearDown(self):
        self.driver.quit()

    def _get_displayed_title_word(self):
        found_titles = sum(
            [t.text.split() for t in self.driver.find_elements_by_class_name("title_link")],
            [])
        #title = next(x for x in found_titles[2].text.split() if len(x) > 4)
        title_words = filter(lambda cand: len(cand) > 4, found_titles)
        return choice(title_words)

    def _search_for_text(self, text):
        self.driver.find_element_by_id("keyword_search_input").send_keys(text + "\n")
        wait_for_ajaxes_to_complete(self.driver)

    def test_search_for_title(self):
        inital_total = self.driver.find_element_by_id("current_total_display").text
        self._search_for_text("title:" + self._get_displayed_title_word())
        searched_total = self.driver.find_element_by_id("current_total_display").text
        self.assertNotEqual(inital_total, searched_total)

    def test_free_text_search(self):
        inital_total = self.driver.find_element_by_id("current_total_display").text
        self._search_for_text(self._get_displayed_title_word())
        searched_total = self.driver.find_element_by_id("current_total_display").text
        self.assertNotEqual(inital_total, searched_total)

    def test_combined_search_for_free_text_and_title(self):
        inital_total = int(self.driver.find_element_by_id("current_total_display").text)
        first_q = "title:" + self._get_displayed_title_word()
        self._search_for_text(first_q)
        between_total = int(self.driver.find_element_by_id("current_total_display").text)
        sleep(1)
        self._search_for_text(" " + self._get_displayed_title_word())
        final_total = int(self.driver.find_element_by_id("current_total_display").text)
        self.assertNotEqual(inital_total, between_total)
        self.assertNotEqual(inital_total, final_total)
        self.assertTrue(inital_total >= between_total)
        self.assertTrue(between_total >= final_total)
