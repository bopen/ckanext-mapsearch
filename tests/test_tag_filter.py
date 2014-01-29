import re
import unittest
from helpers import wait_for_ajaxes_to_complete
from helpers import get_result_stats

from selenium import webdriver

class TestTagFilter(unittest.TestCase):

    def setUp(self):
        try:
            self.driver = webdriver.Firefox()
        except:
            self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000/mapsearch")
        self.assertIn("Mapsearch", self.driver.title)
        wait_for_ajaxes_to_complete(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_filter_by_tag(self):
        filters_button = self.driver.find_element_by_css_selector("#filter_toggler");
        tag_links = self.driver.find_elements_by_css_selector(".filter_toggle");
        self.assertFalse(tag_links[1].is_displayed())
        filters_button.click()
        self.assertTrue(tag_links[1].is_displayed())
        tag_links = self.driver.find_elements_by_css_selector(".filter_toggle");
        comp = "tags:" + tag_links[1].text.split()[0]
        prior_stats = get_result_stats(self.driver)
        tag_links[1].click()
        search_input = self.driver.find_element_by_css_selector("#keyword_search_input");
        val = search_input.get_attribute('value').strip()
        self.assertEqual(re.sub("[^a-z].", "", val), re.sub("[^a-z].", "", comp))
        wait_for_ajaxes_to_complete(self.driver)
        later_stats = get_result_stats(self.driver)
        self.assertNotEqual(prior_stats, later_stats)
        return
