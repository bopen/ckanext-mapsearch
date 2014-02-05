import unittest

from time import sleep
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.keys import Keys
from helpers import display_javascript_notice
from helpers import wait_for_ajaxes_to_complete


class TestPageload(unittest.TestCase):

    def setUp(self):
        try:
            self.driver = webdriver.Firefox()
        except:
            self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_page_load(self):
        self.driver.get("http://localhost:5000/mapsearch")
        self.assertIn("Mapsearch", self.driver.title)
        display_javascript_notice(
            self.driver, "running test: {0}".format(self._testMethodName))
        wait_for_ajaxes_to_complete(self.driver)

    def example_input():
#        act = webdriver.ActionChains(driver)
#        act.send_keys(Keys.ESCAPE)
#        act.send_keys(Keys.ESCAPE)
#        act.perform()
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

#    driver = setup()
    sleep(1)
#    zoom_in(driver)
    sleep(1)
#    filter_by_tag(driver)
#    driver.quit()
    import sys
    sys.exit()
#    open_timeseries_window(driver)
#    open_search_window(driver)
    sleep(2)
#    driver.quit()
