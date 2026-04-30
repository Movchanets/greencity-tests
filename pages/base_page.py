from time import sleep

import allure
from data.config import Config
from pages.components.signin_modal import SigninModal
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    sign_in_button_locator = (By.CSS_SELECTOR, ".header_navigation-menu-right-list > .header_sign-in-link")
    sign_in_modal_locator = (By.XPATH, "//app-auth-modal")
    language_switcher = (By.XPATH, "//ul[@aria-label='language switcher']")
    language_en_option = (By.XPATH, ".//span[contains(text(), 'En')]")
    language_ua_option = (By.XPATH, ".//span[contains(text(), 'Uk')]")

    eco_news_link_locator = (By.XPATH, "//header//a[contains(@class, 'url-name') and contains(., 'Еко новини') or contains(., 'Eco news')]")
    events_link_locator = (By.XPATH, "//header//a[contains(@class, 'url-name') and contains(., 'Події') or contains(., 'Events')]")
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.timeout = timeout

    @allure.step("Open page by URL")
    def open(self, url=None):
        self.driver.get(url or Config.BASE_UI_URL)

    def wait(self, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout)

    def wait_for_presence(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def wait_for_visible(self, locator, timeout=None):
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator, timeout=None):
        return self.wait(timeout).until(EC.element_to_be_clickable(locator))

    def wait_for_all_present(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_all_elements_located(locator))

    def scroll_to(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)
    
    @allure.step("Get sign in button")
    def get_sign_in_button(self):
        return self.wait_for_clickable(self.sign_in_button_locator)

    @allure.step("Get sign in modal")
    def get_sign_in_modal(self):
        return self.wait_for_visible(self.sign_in_modal_locator)

    @allure.step("Click sign in in header")
    def click_sign_in(self):
        sign_in_button = self.get_sign_in_button()
        sign_in_button.click()
        return SigninModal(self.get_sign_in_modal())

    @allure.step("Get language switcher")
    def get_language_switcher(self):
        return self.wait_for_clickable(self.language_switcher)

    @allure.step("Switch language to '{language}'")
    def switch_language(self, language):
        language_switcher = self.get_language_switcher()
        language_switcher.click()
        if language.lower() == "en":
            language_option = self.wait_for_clickable(self.language_en_option)
        elif language.lower() == "ua":
            language_option = self.wait_for_clickable(self.language_ua_option)
        else:
            raise ValueError("Unsupported language: {}".format(language))
        language_option.click()
        sleep(1)

    @allure.step("Get eco news link from header")
    def get_eco_news_link(self):
        return self.wait_for_clickable(self.eco_news_link_locator)
    
    @allure.step("Navigate to eco news page using header link")
    def navigate_to_eco_news(self):
        eco_news_link = self.get_eco_news_link()
        eco_news_link.click()


    @allure.step("Get events link from header")
    def get_events_link(self):
        return self.wait_for_clickable(self.events_link_locator)
    
    @allure.step("Navigate to events page using header link")
    def navigate_to_events(self):
        events_link = self.get_events_link()
        events_link.click()

