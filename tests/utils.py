from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

BASE_URL = "https://www.greencity.cx.ua/#/greenCity/events"
TIMEOUT = 15


def wait_for_element_visible(driver, locator, timeout=TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def wait_for_element_clickable(driver, locator, timeout=TIMEOUT):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))


def wait_for_elements_visible(driver, locator, timeout=TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_all_elements_located(locator)
    )


def wait_for_element_present(driver, locator, timeout=TIMEOUT):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))


def wait_for_url_contains(driver, text, timeout=TIMEOUT):
    return WebDriverWait(driver, timeout).until(EC.url_contains(text))


def wait_for_element_text_to_be(driver, locator, text, timeout=TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.text_to_be_present_in_element(locator, text)
    )


def is_element_visible(driver, locator, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
        return True
    except Exception:
        return False
