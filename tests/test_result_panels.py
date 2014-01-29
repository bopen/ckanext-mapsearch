import unittest
from time import sleep
from helpers import wait_for_ajaxes_to_complete
from helpers import get_result_stats
from helpers import reload_datasets

from selenium import webdriver

class TestResultPanels(unittest.TestCase):

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

    def test_hover_result_panel(self):
        reload_datasets(self.driver)
        selected_result_panels = self.driver.find_elements_by_css_selector(".dataset_result_panel.selected")
        self.assertEqual(len(selected_result_panels), 0)
        selected_extents = self.driver.find_elements_by_css_selector("path[fill='#FFFFFF']")
        self.assertEqual(len(selected_extents), 0)
        all_result_panels = self.driver.find_elements_by_css_selector(".dataset_result_panel")
        target_panel = all_result_panels[1]
        self.driver.execute_script("$('#{0}').trigger('mouseenter')".format(target_panel.get_attribute('id')))
        selected_extents = self.driver.find_elements_by_css_selector("path[fill='#FFFFFF']")
        self.assertEqual(len(selected_extents), 1)
        selected_result_panels = self.driver.find_elements_by_css_selector(".dataset_result_panel.selected")
        self.assertEqual(len(selected_result_panels), 1)
        self.assertTrue(selected_result_panels[0].is_displayed())
