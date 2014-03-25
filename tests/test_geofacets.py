import unittest
from time import sleep

from selenium import webdriver

from helpers import wait_for_ajaxes_to_complete, get_result_stats
from helpers import display_javascript_notice, search_for_text
from helpers import get_map_bounds, get_displayed_title_word
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

    def test_geofacets_with_spaces_change_map_extent(self):
        search_for_text(self.driver, 'geo:italy')
        sleep(0.6)
        italy_bounds = get_map_bounds(self.driver)
        italy_total = get_result_stats(self.driver)['normal']
        search_for_text(self.driver, 'geo:"emilia romagna"')
        sleep(0.6)
        emilia_bounds = get_map_bounds(self.driver)
        emilia_total = get_result_stats(self.driver)['normal']
        self.assertLess(italy_bounds['_southWest']['lat'], emilia_bounds['_southWest']['lat'])
        self.assertLess(italy_bounds['_southWest']['lng'], emilia_bounds['_southWest']['lng'])
        self.assertGreater(italy_total, emilia_total)

    def test_geofacets_with_spaces_works_with_other_facets(self):
        search_for_text(self.driver, 'geo:"emilia romagna"')
        sleep(1)
        emilia_total = get_result_stats(self.driver)['normal']
        title = get_displayed_title_word(self.driver)
        search_for_text(self.driver, 'geo:"emilia romagna" title:' + title)
        sleep(1)
        title_total = get_result_stats(self.driver)['normal']
        self.assertGreater(emilia_total, title_total)
        search_for_text(self.driver, 'title:' + title + ' geo:"emilia romagna"')
        sleep(1)
        title_total2 = get_result_stats(self.driver)['normal']
        self.assertEqual(title_total, title_total2)

    def test_geofacet_changes_map_extent1(self):
        search_for_text(self.driver, "geo:capranica")
        sleep(0.6)
        capra_bounds1 = get_map_bounds(self.driver)
        search_for_text(self.driver, "geo:sutri")
        sleep(0.6)
        sutri_bounds = get_map_bounds(self.driver)
        search_for_text(self.driver, "geo:capranica")
        sleep(0.6)
        capra_bounds2 = get_map_bounds(self.driver)
        self.assertAlmostEqual(capra_bounds1['_southWest']['lat'],
                               capra_bounds2['_southWest']['lat'],
                               places=3)
        self.assertAlmostEqual(capra_bounds1['_southWest']['lng'],
                               capra_bounds2['_southWest']['lng'],
                               places=3)
        self.assertNotEqual(capra_bounds1, sutri_bounds)

    def test_geofacet_changes_map_extent2(self):
        search_for_text(self.driver, "geo:capranica")
        sleep(0.6)
        capra_bounds = get_map_bounds(self.driver)
        self.assertLess(capra_bounds['_southWest']['lat'], 50)
        search_for_text(self.driver, "geo:kreuzberg")
        sleep(0.6)
        kreuz_bounds = get_map_bounds(self.driver)
        self.assertGreater(kreuz_bounds['_southWest']['lat'], 50)

    def test_geofacet_alone(self):
        sleep(1)
        initial_total = get_result_stats(self.driver)['normal']
        search_for_text(self.driver, "geo:abruzzo")
        sleep(0.6)
        searched_total = get_result_stats(self.driver)['normal']
        self.assertGreaterEqual(initial_total, searched_total)
        self.assertGreaterEqual(searched_total, 1)

    def test_geofacet_positive_with_text_before(self):
        sleep(0.6)
        initial_total = get_result_stats(self.driver)['normal']
        search_for_text(self.driver, "tal geo:abruzzo")
        sleep(0.6)
        searched_total = get_result_stats(self.driver)['normal']
        self.assertGreaterEqual(initial_total, searched_total)
        self.assertGreaterEqual(searched_total, 1)

    def test_geofacet_positive_with_text_after(self):
        sleep(0.6)
        initial_total = get_result_stats(self.driver)['normal']
        search_for_text(self.driver, "geo:abruzzo tal")
        sleep(0.6)
        searched_total = get_result_stats(self.driver)['normal']
        self.assertGreaterEqual(initial_total, searched_total)
        self.assertGreaterEqual(searched_total, 1)

    def test_geofacet_positive_with_text_before_and_after(self):
        sleep(0.6)
        initial_total = get_result_stats(self.driver)['normal']
        search_for_text(self.driver, "tip geo:abruzzo tal")
        sleep(0.6)
        searched_total = get_result_stats(self.driver)['normal']
        self.assertTrue(initial_total >= searched_total)
        self.assertTrue(searched_total >= 1)

    def test_geofacet_negative_with_text_after(self):
        sleep(0.6)
        initial_total = get_result_stats(self.driver)['normal']
        search_for_text(self.driver, "tappppppp geo:abruzzo tal")
        sleep(0.6)
        searched_total = get_result_stats(self.driver)['normal']
        self.assertGreaterEqual(initial_total, searched_total)
        self.assertEqual(searched_total, 0)
