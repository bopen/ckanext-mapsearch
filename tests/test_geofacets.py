import unittest
from time import sleep
from random import choice

from selenium import webdriver

from helpers import wait_for_ajaxes_to_complete, get_result_stats
from helpers import display_javascript_notice, search_for_text
from helpers import get_map_bounds, get_displayed_title_word
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

    def test_geofacets_with_spaces_change_map_extent(self):
        search_for_text(self.driver, 'geo:italy')
        sleep(0.2)
        italy_bounds = get_map_bounds(self.driver)
        italy_total = get_result_stats(self.driver)['normal']
        search_for_text(self.driver, 'geo:"emilia romagna"')
        sleep(0.2)
        emilia_bounds = get_map_bounds(self.driver)
        emilia_total = get_result_stats(self.driver)['normal']
        self.assertLess(italy_bounds['_southWest']['lat'], emilia_bounds['_southWest']['lat'])
        self.assertLess(italy_bounds['_southWest']['lng'], emilia_bounds['_southWest']['lng'])
        self.assertGreater(italy_total, emilia_total)

    def test_geofacets_with_spaces_works_with_other_facets(self):
        search_for_text(self.driver, 'geo:"emilia romagna"')
        sleep(0.2)
        emilia_total = get_result_stats(self.driver)['normal']
        title = get_displayed_title_word(self.driver)
        search_for_text(self.driver, 'geo:"emilia romagna" title:' + title)
        sleep(0.6)
        title_total = get_result_stats(self.driver)['normal']
        self.assertGreater(emilia_total, title_total)
        search_for_text(self.driver, 'title:' + title + ' geo:"emilia romagna"')
        sleep(1)
        title_total2 = get_result_stats(self.driver)['normal']
        self.assertEqual(title_total, title_total2)

    def test_geofacet_changes_map_extent1(self):
        search_for_text(self.driver, "geo:capranica")
        sleep(0.2)
        capra_bounds1 = get_map_bounds(self.driver)
        search_for_text(self.driver, "geo:sutri")
        sleep(0.2)
        sutri_bounds = get_map_bounds(self.driver)
        search_for_text(self.driver, "geo:capranica")
        capra_bounds2 = get_map_bounds(self.driver)
        sleep(0.2)
        self.assertEqual(capra_bounds1, capra_bounds2)
        self.assertNotEqual(capra_bounds1, sutri_bounds)

    def test_geofacet_changes_map_extent2(self):
        search_for_text(self.driver, "geo:capranica")
        capra_bounds = get_map_bounds(self.driver)
        self.assertLess(capra_bounds['_southWest']['lat'], 50)
        search_for_text(self.driver, "geo:kreuzberg")
        kreuz_bounds = get_map_bounds(self.driver)
        self.assertGreater(kreuz_bounds['_southWest']['lat'], 50)

    def test_geofacet_alone(self):
        initial_total = get_result_stats(self.driver)['normal']
        search_for_text(self.driver, "geo:abruzzo")
        searched_total = get_result_stats(self.driver)['normal']
        self.assertTrue(initial_total >= searched_total)
        self.assertTrue(searched_total >= 1)

    def test_geofacet_positive_with_text_before(self):
        initial_total = get_result_stats(self.driver)['normal']
        search_for_text(self.driver, "tal geo:abruzzo")
        searched_total = get_result_stats(self.driver)['normal']
        self.assertTrue(initial_total >= searched_total)
        self.assertTrue(searched_total >= 1)

    def test_geofacet_positive_with_text_after(self):
        initial_total = get_result_stats(self.driver)['normal']
        search_for_text(self.driver, "geo:abruzzo tal")
        searched_total = get_result_stats(self.driver)['normal']
        self.assertTrue(initial_total >= searched_total)
        self.assertTrue(searched_total >= 1)

    def test_geofacet_positive_with_text_before_and_after(self):
        initial_total = get_result_stats(self.driver)['normal']
        search_for_text(self.driver, "tip geo:abruzzo tal")
        searched_total = get_result_stats(self.driver)['normal']
        self.assertTrue(initial_total >= searched_total)
        self.assertTrue(searched_total >= 1)

    def test_geofacet_negative_with_text_after(self):
        initial_total = get_result_stats(self.driver)['normal']
        search_for_text(self.driver, "tappppppp geo:abruzzo tal")
        searched_total = get_result_stats(self.driver)['normal']
        self.assertTrue(initial_total >= searched_total)
        self.assertTrue(searched_total == 0)
