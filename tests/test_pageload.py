import re
import unittest

from time import sleep
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from helpers import get_result_stats
from helpers import wait_for_ajaxes_to_complete


class TestPageload(unittest.TestCase):

    def setUp(self):
        try:
            self.driver = webdriver.Firefox()
        except:
            self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000/mapsearch")
        self.assertNotEqual(self.driver.title, "www")
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

    def example_input():
        act = webdriver.ActionChains(driver)
        act.send_keys(Keys.ESCAPE)
        act.send_keys(Keys.ESCAPE)
        act.perform()
        sleep(1)

    def example_xpath_query(driver):
        options = driver.find_element_by_xpath("//div[contains(.,'FAPAR')]")
        print options.text
        options.click()
        sleep(1)
        close_buttons = driver.find_elements_by_class_name("x-tool-close")
        for b in close_buttons:
            try:
                b.click()
            except ElementNotVisibleException:
                pass
        sleep(2)

if __name__ == "__main__":
    unittest.main()
    import sys
    sys.exit()

    driver = setup()
    sleep(1)
    zoom_in(driver)
    sleep(1)
    filter_by_tag(driver)
    driver.quit()
    import sys
    sys.exit()
    open_timeseries_window(driver)
    open_search_window(driver)
    sleep(2)
    driver.quit()

