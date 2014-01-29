import unittest
from helpers import wait_for_ajaxes_to_complete
from helpers import get_result_stats

from selenium import webdriver

class TestZoom(unittest.TestCase):

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

    def test_zoom_in(self):
        zoom_button = self.driver.find_element_by_css_selector(".leaflet-control-zoom-in");
        #print "zooming in", zoom_button, dir(zoom_button)
        prior_stats = get_result_stats(self.driver)
        zoom_button.click()
        #print self.driver.execute_script('return jQuery.active;')
        wait_for_ajaxes_to_complete(self.driver)
        later_stats = get_result_stats(self.driver)
        self.assertNotEqual(prior_stats, later_stats)
        return

