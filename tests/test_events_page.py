import os
from time import sleep
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from helpers import (
    _setup_driver,
    _take_screenshot,
    _click_mat_select,
    _select_mat_option,
    _close_dropdown,
    _set_date_range,
)

from helpers import (
    _setup_driver,
    _take_screenshot,
    _click_mat_select,
    _select_mat_option,
    _close_dropdown,
    _set_date_range,
)

BASE_URL = "https://www.greencity.cx.ua/#/greenCity/events"
TIMEOUT = 15
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")


def _setup_driver():
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    return driver


def _take_screenshot(driver, test_name):
    try:
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        path = os.path.join(SCREENSHOT_DIR, f"{test_name}.png")
        driver.save_screenshot(path)
        print(f"\n  [Screenshot] {path}")
    except Exception:
        pass


def _click_mat_select(driver, mat_select_element):
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", mat_select_element
    )
    driver.execute_script("arguments[0].click();", mat_select_element)


def _select_mat_option(driver, option_text):
    wait = WebDriverWait(driver, TIMEOUT)
    option = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//mat-option[contains(., '{option_text}')]")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
    driver.execute_script("arguments[0].click();", option)


def _close_dropdown(driver):
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)


class TestEventsPage(unittest.TestCase):
    def setUp(self):
        print(f"\n{'=' * 60}")
        print(f"  [SETUP] Opening Chrome -> {BASE_URL}")
        self.driver = _setup_driver()
        self.driver.get(BASE_URL)
        self.wait = WebDriverWait(self.driver, TIMEOUT)

    def tearDown(self):
        if self.driver:
            _take_screenshot(self.driver, self._testMethodName)
            self.driver.quit()
            print(f"  [TEARDOWN] Browser closed")
            print(f"{'=' * 60}")

    def test_TC01_open_event_and_check_details(self):
        """TC-01: Відкрити подію зі списку і перевірити деталі."""

        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "mat-card.event-list-item")
            )
        )

        cards = self.driver.find_elements(By.CSS_SELECTOR, "mat-card.event-list-item")
        self.assertTrue(len(cards) > 0, "No event cards found on the page")
        print(f"  Found {len(cards)} event cards")

        first_card = cards[0]
        card_title = first_card.find_element(
            By.CSS_SELECTOR, ".event-title, .event-name, p"
        ).text
        print(f"  First event title: '{card_title}'")
        self.assertTrue(len(card_title.strip()) > 0, "Event title is empty")

        more_buttons = first_card.find_elements(
            By.CSS_SELECTOR, ".secondary-global-button, .event-button"
        )
        self.assertTrue(len(more_buttons) > 0, "No 'More' button found on card")

        more_btn = more_buttons[0]
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", more_btn
        )
        self.wait.until(EC.element_to_be_clickable(more_btn)).click()

        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".event-title, h2, h1, .event-name")
            )
        )
        
        detail_title = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".event-title, h2, h1, .event-name")
            )
        ).text
        print(f"  Detail page title: '{detail_title}'")
        self.assertTrue(len(detail_title.strip()) > 0, "Detail page title is empty")

        page_source = self.driver.page_source.lower()
        has_location = (
            "office" in page_source
            or "st." in page_source
            or "вул" in page_source.lower()
            or "online" in page_source
            or "link" in page_source
        )
        print(f"  Has location info: {has_location}")

    def test_TC02_filter_and_reset(self):
        """TC-02: Застосувати фільтр і скинути його."""

        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "mat-card.event-list-item")
            )
        )

        initial_cards = self.driver.find_elements(
            By.CSS_SELECTOR, "mat-card.event-list-item"
        )
        initial_count = len(initial_cards)
        print(f"  Initial events count: {initial_count}")

        mat_selects = self.driver.find_elements(By.CSS_SELECTOR, "mat-select")
        self.assertTrue(len(mat_selects) > 0, "No filter dropdowns found")
        print(f"  Found {len(mat_selects)} filter dropdowns")

        first_select = mat_selects[0]
        _click_mat_select(self.driver, first_select)

        options = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "mat-option"))
        )
        self.assertTrue(len(options) > 0, "No filter options appeared")
        print(f"  Found {len(options)} filter options")

        first_option_text = options[0].text
        print(f"  Selecting option: '{first_option_text}'")
        _select_mat_option(self.driver, first_option_text)

        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "mat-card.event-list-item")
            )
        )

        filtered_cards = self.driver.find_elements(
            By.CSS_SELECTOR, "mat-card.event-list-item"
        )
        print(f"  Events after filter: {len(filtered_cards)}")

        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

        reset_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.reset"))
        )
        print(f"  Reset button text: '{reset_btn.text}'")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", reset_btn
        )
        reset_btn.click()

        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "mat-card.event-list-item")
            )
        )

        final_cards = self.driver.find_elements(
            By.CSS_SELECTOR, "mat-card.event-list-item"
        )
        print(f"  Events after reset: {len(final_cards)}")
        self.assertTrue(
            len(final_cards) > 0,
            "No event cards found after resetting filters",
        )

    def test_TC04_filter_no_results(self):
        """TC-04: Негативний тест — Майбутні події + дата в минулому = 0 результатів."""

        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "mat-card.event-list-item")
            )
        )

        initial_cards = self.driver.find_elements(
            By.CSS_SELECTOR, "mat-card.event-list-item"
        )
        initial_count = len(initial_cards)
        print(f"  Initial events count: {initial_count}")

        mat_selects = self.driver.find_elements(By.CSS_SELECTOR, "mat-select")
        self.assertTrue(len(mat_selects) >= 4, "Not enough filter dropdowns")
        print(f"  Found {len(mat_selects)} filter dropdowns")

        _click_mat_select(self.driver, mat_selects[1])
        opts_status = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "mat-option"))
        )
        future_status = opts_status[1].text
        print(f"  Selecting status: '{future_status}'")
        _select_mat_option(self.driver, future_status)
        _close_dropdown(self.driver)

        _click_mat_select(self.driver, mat_selects[3])
        opts_date = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "mat-option"))
        )
        choose_date = opts_date[1].text
        print(f"  Selecting date option: '{choose_date}'")
        _select_mat_option(self.driver, choose_date)
        _close_dropdown(self.driver)

        _set_date_range(self.driver, "01/01/2024", "01/31/2024")
        print(f"  Set date range: Jan 2024 (past)")

        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "mat-card.event-list-item")
                )
            )
            remaining_cards = self.driver.find_elements(
                By.CSS_SELECTOR, "mat-card.event-list-item"
            )
        except TimeoutException:
            remaining_cards = []

        print(f"  Events after filters: {len(remaining_cards)}")

        self.assertEqual(
            len(remaining_cards),
            0,
            f"Expected 0 events (Future + past date), but found {len(remaining_cards)}",
        )
        


if __name__ == "__main__":
    unittest.main()
