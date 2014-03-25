import unittest
from time import sleep
from selenium import webdriver

from helpers import wait_for_ajaxes_to_complete
from helpers import display_javascript_notice
from helpers import reload_datasets
from helpers import get_driver
from tests import MAPSEARCH_INSTANCE_URL


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

    def test_click_extent_selects_it(self):
        reload_datasets(self.driver)
        selected_extents = (self.driver.find_elements_by_css_selector(
            "path[fill='#FFFFFF']") or
	    self.driver.find_elements_by_css_selector(
            "path[fill='#ffffff']"))
        self.assertEqual(len(selected_extents), 0)
        extent = self.driver.find_element_by_css_selector(
            ".leaflet-clickable")
        extent.click()
        sleep(1)
        selected_extents = (self.driver.find_elements_by_css_selector(
            "path[fill='#FFFFFF']") or
	    self.driver.find_elements_by_css_selector(
            "path[fill='#ffffff']"))
        self.assertEqual(len(selected_extents), 1)
        self.assertTrue(selected_extents[0].is_displayed())

    def test_click_extent_displays_panel(self):
        reload_datasets(self.driver)
        selected_result_panels = self.driver.find_elements_by_css_selector(
            ".dataset_result_panel.selected")
        self.assertEqual(len(selected_result_panels), 0)
        extent = self.driver.find_element_by_css_selector(".leaflet-clickable")
        extent.click()
        sleep(0.5)
        selected_result_panels = self.driver.find_elements_by_css_selector(
            ".dataset_result_panel.selected")
        self.assertEqual(len(selected_result_panels), 1)
        self.assertTrue(selected_result_panels[0].is_displayed())
