
from selenium.webdriver.common.by import By
from pages.components.base_component import BaseComponent


class EventCardComponent(BaseComponent):
    more_button_locator = (By.CSS_SELECTOR, ".secondary-global-button, .event-button")
    name_locator = (By.CSS_SELECTOR, ".event-title, .event-name, p")

    def click_more(self):
        more_button = self.find_element(*self.more_button_locator)
        self.scroll_to(more_button)
        self.driver.execute_script("arguments[0].click();", more_button)

    def get_name(self):
        name_element = self.find_element(*self.name_locator)
        return name_element.text.strip()
    