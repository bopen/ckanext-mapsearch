import unittest
from selenium import webdriver
from time import sleep

from helpers import wait_for_ajaxes_to_complete
from helpers import get_result_stats, display_javascript_notice
from helpers import get_driver
from tests import MAPSEARCH_INSTANCE_URL

class TestZoom(unittest.TestCase):

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

    def test_zoom_in(self):
        zoom_button = self.driver.find_element_by_css_selector(
            ".leaflet-control-zoom-in")
        #print "zooming in", zoom_button, dir(zoom_button)
        wait_for_ajaxes_to_complete(self.driver)
        prior_stats = get_result_stats(self.driver)
        zoom_button.click()
        #print self.driver.execute_script('return jQuery.active;')
        wait_for_ajaxes_to_complete(self.driver)
        sleep(1)
        later_stats = get_result_stats(self.driver)
        self.assertNotEqual(prior_stats, later_stats)
        return
