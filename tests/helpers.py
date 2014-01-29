from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


def setUp():
    try:
        driver = webdriver.Firefox()
    except:
        driver = webdriver.Chrome()
    driver.get("http://localhost:5000/mapsearch")
    return driver

def get_result_stats(driver):
    too_small = driver.find_element_by_css_selector(".omitted_too_small span");
    small = driver.find_element_by_css_selector(".omitted_small span");
    displayed = driver.find_element_by_css_selector(".normal_scale_count span");
    big = driver.find_element_by_css_selector(".omitted_big span");
    too_big = driver.find_element_by_css_selector(".omitted_too_big span");
    return {'too_small': int(too_small.text),
            'small': int(small.text),
            'displayed': int(displayed.text),
            'big': int(big.text),
            'too_big': int(too_big.text)
    }

def wait_for_ajaxes_to_complete(driver):
    try:
        # we have to wait for the page to refresh, the last thing that seems to be updated is the title
        WebDriverWait(driver, 5).until(
            lambda driver: driver.execute_script('return jQuery.active;') == 0
        )
    except TimeoutException:
        print "ajax calls longer than 5 seconds"
    return True

