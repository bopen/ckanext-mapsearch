import json
from os import environ
from random import choice

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from tests import MAPSEARCH_INSTANCE_URL


def get_driver(which='firefox'):
    if 'MAPSEARCH_TEST_DRIVER' in environ:
        which = environ['MAPSEARCH_TEST_DRIVER']

    if which == 'firefox':
        driver = webdriver.Firefox()
    elif which == 'chrome':
        driver = webdriver.Remote("http://localhost:9515", {})
    return driver


def setUp(which_driver='firefox'):
    if which_driver == 'firefox':
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Remote("http://localhost:9515", {})
    driver.get(MAPSEARCH_INSTANCE_URL)
    return driver


def get_displayed_title_word(driver):
    found_titles = sum(
        [t.text.split() for t
            in driver.find_elements_by_class_name("title_link")],
        [])
    #title = next(x for x in found_titles[2].text.split() if len(x) > 4)
    title_words = filter(lambda cand: len(cand) > 4, found_titles)
    return choice(title_words)


def display_javascript_notice(driver, message):
    driver.execute_script('bop.display_message("{0}");'.format(message))
    return True


def search_for_text(driver, text):
    driver.execute_script("$('#keyword_search_input').attr('value', '')")
    driver.find_element_by_id("keyword_search_input").send_keys(text + "\n")
    wait_for_ajaxes_to_complete(driver)


def get_map_bounds(driver):
    command = "return JSON.stringify(bop.map.getBounds())"
    in_json = driver.execute_script(command)
    return json.loads(in_json)


def get_result_stats(driver):
    too_small = driver.find_element_by_css_selector(".omitted_too_small span")
    small = driver.find_element_by_css_selector(".omitted_small span")
    normal = driver.find_element_by_css_selector(".normal_scale_count span")
    displayed = driver.find_element_by_css_selector("#current_total_display")
    big = driver.find_element_by_css_selector(".omitted_big span")
    too_big = driver.find_element_by_css_selector(".omitted_too_big span")
    return {'too_small': int(too_small.text or 0),
            'small': int(small.text or 0),
            'displayed': displayed.text,
            'normal': int(normal.text or 0),
            'big': int(big.text or 0),
            'too_big': int(too_big.text or 0)
            }


def reload_datasets(driver):
    driver.find_element_by_css_selector('#keyword_clear_button').click()
    wait_for_ajaxes_to_complete(driver)


def wait_for_ajaxes_to_complete(driver):
    try:
        # we have to wait for the page to refresh, the last thing that seems to
        # be updated is the title
        WebDriverWait(driver, 15).until(
            lambda driver: driver.execute_script('return jQuery.active;') == 0
        )
    except TimeoutException:
        print "ajax calls longer than 15 seconds"
        raise RuntimeError("too slow")
    return True
