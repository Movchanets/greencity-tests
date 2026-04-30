import re

import allure
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from pages.components.event_card_components import EventCardComponent

class EventsPage(BasePage):

    main_header_locator = (By.XPATH, "//h1[contains(@class, 'main-header')] | //p[contains(@class, 'main-header')]")
    items_fount_locator = (By.XPATH, "//div[@class='active-filter-container']/p")
    cards_locator = (By.CSS_SELECTOR, "mat-card.event-list-item")
    detail_title_locator = (By.CSS_SELECTOR, ".event-title, h2, h1, .event-name")
    mat_select_locator = (By.CSS_SELECTOR, "mat-select")
    mat_option_locator = (By.CSS_SELECTOR, "mat-option")
    reset_button_locator = (By.CSS_SELECTOR, "button.reset")
    body_locator = (By.TAG_NAME, "body")
    start_date_locator = (By.CSS_SELECTOR, "input.mat-start-date")
    end_date_locator = (By.CSS_SELECTOR, "input.mat-end-date")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Open events page")
    def open(self, base_url):
        self.driver.get(base_url)

    @allure.step("Wait until events page is loaded")
    def wait_until_loaded(self):
        self.wait_for_presence(self.cards_locator)

    @allure.step("Get events page main header")
    def get_main_header(self):
        return self.wait_for_visible(self.main_header_locator)

    @allure.step("Get items found label")
    def get_items_found(self):
        return self.wait_for_visible(self.items_fount_locator)
    
    @allure.step("Get items found count")
    def get_items_count(self):
        items_found = self.get_items_found()
        text = items_found.text

        match = re.search(r'\d+', text)
        if match:
            result = int(match.group())
            return result

    @allure.step("Get event card web elements")
    def get_card_elements(self):
        return self.driver.find_elements(*self.cards_locator)

    @allure.step("Build event card components")
    def get_cards(self):
        cards_web_elements = self.get_card_elements()
        return [EventCardComponent(card_element) for card_element in cards_web_elements]

    @allure.step("Count event cards on events page")
    def get_cards_count(self):
        return len(self.get_card_elements())

    @allure.step("Open first event details")
    def open_first_event_details(self):
        cards = self.get_cards()
        if not cards:
            return None
        cards[0].click_more()
        return cards[0]

    @allure.step("Get event details title text")
    def get_detail_title_text(self):
        return self.wait_for_visible(self.detail_title_locator).text

    @allure.step("Check if details page has location hint")
    def page_has_location_hint(self):
        page_source = self.driver.page_source.lower()
        return (
            "office" in page_source
            or "st." in page_source
            or "вул" in page_source
            or "online" in page_source
            or "link" in page_source
        )

    @allure.step("Get filter dropdowns")
    def get_filter_selects(self):
        return self.driver.find_elements(*self.mat_select_locator)

    @allure.step("Open filter dropdown by index: {index}")
    def open_filter_select(self, index):
        selects = self.get_filter_selects()
        if index >= len(selects):
            raise IndexError("Filter index is out of range")
        target = selects[index]
        self.scroll_to(target)
        self.js_click(target)

    @allure.step("Get opened filter options")
    def get_open_options(self):
        return self.wait_for_all_present(self.mat_option_locator)

    @allure.step("Select filter option by text: {option_text}")
    def select_option_by_text(self, option_text):
        option_locator = (By.XPATH, f"//mat-option[contains(., '{option_text}')]")
        option = self.wait_for_clickable(option_locator)
        self.scroll_to(option)
        self.js_click(option)

    @allure.step("Select filter option by index: {index}")
    def select_option_by_index(self, index):
        options = self.get_open_options()
        if index >= len(options):
            raise IndexError("Option index is out of range")
        selected_text = options[index].text
        self.select_option_by_text(selected_text)
        return selected_text

    @allure.step("Close opened dropdown")
    def close_dropdown(self):
        self.driver.find_element(*self.body_locator).send_keys(Keys.ESCAPE)

    @allure.step("Click reset filters button")
    def click_reset(self):
        reset = self.wait_for_clickable(self.reset_button_locator)
        self.scroll_to(reset)
        reset.click()

    @allure.step("Set date range: {start_date} - {end_date}")
    def set_date_range(self, start_date, end_date):
        start_input = self.wait_for_presence(self.start_date_locator)
        end_input = self.wait_for_presence(self.end_date_locator)
        self.driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles: true}));",
            start_input,
            start_date,
        )
        self.driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles: true}));",
            end_input,
            end_date,
        )

    @allure.step("Get cards or empty list after wait")
    def get_cards_or_empty_after_wait(self):
        try:
            self.wait_for_presence(self.cards_locator)
            return self.get_card_elements()
        except TimeoutException:
            return []
