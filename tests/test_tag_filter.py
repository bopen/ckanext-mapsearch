import re
import unittest
from time import sleep
from selenium import webdriver

from helpers import wait_for_ajaxes_to_complete
from helpers import get_result_stats, display_javascript_notice
from tests import MAPSEARCH_INSTANCE_URL
from helpers import get_driver


class TestTagFilter(unittest.TestCase):

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

    def test_filter_by_tag(self):
	sleep(1)
        filters_button = self.driver.find_element_by_css_selector(
            "#filter_toggler")
        tag_links = self.driver.find_elements_by_css_selector(
            ".filter_toggle")
        self.assertFalse(tag_links[1].is_displayed())
        filters_button.click()
        self.assertTrue(tag_links[1].is_displayed())
        tag_links = self.driver.find_elements_by_css_selector(
            ".filter_toggle")
        comp = "tags:" + tag_links[1].text.split()[0]
        prior_stats = get_result_stats(self.driver)
        tag_links[1].click()
        search_input = self.driver.find_element_by_css_selector(
            "#keyword_search_input")
        val = search_input.get_attribute('value').strip()
        self.assertEqual(re.sub("[^a-z].", "", val),
                         re.sub("[^a-z].", "", comp))
        wait_for_ajaxes_to_complete(self.driver)
        later_stats = get_result_stats(self.driver)
        self.assertNotEqual(prior_stats, later_stats)
        return
