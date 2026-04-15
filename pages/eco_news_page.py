from .base_page import BasePage
from selenium.webdriver.common.by import By


class EcoNewsPage(BasePage):

    main_header_locator = (By.XPATH, "//h1[contains(@class, 'main-header')]")

    def __init__(self, driver):
        super().__init__(driver)