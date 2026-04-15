import unittest
from selenium.webdriver.support.ui import WebDriverWait

from helpers import (
    _setup_driver,
    _take_screenshot,
)

from pages.events_page import EventsPage

BASE_URL = "https://www.greencity.cx.ua/#/greenCity/events"
TIMEOUT = 15


class TestEventsPage(unittest.TestCase):
    def setUp(self):
        print(f"\n{'=' * 60}")
        print(f"  [SETUP] Opening Chrome -> {BASE_URL}")
        self.driver = _setup_driver()
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        self.events_page = EventsPage(self.driver)
        self.events_page.open(BASE_URL)
        self.events_page.wait_until_loaded()

    def tearDown(self):
        if self.driver:
            _take_screenshot(self.driver, self._testMethodName)
            self.driver.quit()
            print(f"  [TEARDOWN] Browser closed")
            print(f"{'=' * 60}")

    def test_TC01_open_event_and_check_details(self):
        """TC-01: Відкрити подію зі списку і перевірити деталі."""

        cards = self.events_page.get_cards()
        self.assertTrue(len(cards) > 0, "No event cards found on the page")
        print(f"  Found {len(cards)} event cards")

        first_card = cards[0]
        card_title = first_card.get_name()
        print(f"  First event title: '{card_title}'")
        self.assertTrue(len(card_title.strip()) > 0, "Event title is empty")

        first_card.click_more()
        detail_title = self.events_page.get_detail_title_text()
        print(f"  Detail page title: '{detail_title}'")
        self.assertTrue(len(detail_title.strip()) > 0, "Detail page title is empty")

        has_location = self.events_page.page_has_location_hint()
        print(f"  Has location info: {has_location}")

    def test_TC02_filter_and_reset(self):
        """TC-02: Застосувати фільтр і скинути його."""

        initial_count = self.events_page.get_cards_count()
        print(f"  Initial events count: {initial_count}")

        mat_selects = self.events_page.get_filter_selects()
        self.assertTrue(len(mat_selects) > 0, "No filter dropdowns found")
        print(f"  Found {len(mat_selects)} filter dropdowns")

        self.events_page.open_filter_select(0)

        options = self.events_page.get_open_options()
        self.assertTrue(len(options) > 0, "No filter options appeared")
        print(f"  Found {len(options)} filter options")

        first_option_text = options[0].text.strip()
        print(f"  Selecting option: '{first_option_text}'")
        self.events_page.select_option_by_text(first_option_text)

        self.events_page.wait_until_loaded()
        filtered_cards = self.events_page.get_card_elements()
        print(f"  Events after filter: {len(filtered_cards)}")

        self.events_page.close_dropdown()
        self.events_page.click_reset()
        self.events_page.wait_until_loaded()

        final_cards = self.events_page.get_card_elements()
        print(f"  Events after reset: {len(final_cards)}")
        self.assertTrue(
            len(final_cards) > 0,
            "No event cards found after resetting filters",
        )

    def test_TC04_filter_no_results(self):
        """TC-04: Негативний тест — Майбутні події + дата в минулому = 0 результатів."""

        initial_count = self.events_page.get_cards_count()
        print(f"  Initial events count: {initial_count}")

        mat_selects = self.events_page.get_filter_selects()
        self.assertTrue(len(mat_selects) >= 4, "Not enough filter dropdowns")
        print(f"  Found {len(mat_selects)} filter dropdowns")

        self.events_page.open_filter_select(1)
        opts_status = self.events_page.get_open_options()
        future_status = opts_status[1].text.strip()
        print(f"  Selecting status: '{future_status}'")
        self.events_page.select_option_by_text(future_status)
        self.events_page.close_dropdown()

        self.events_page.open_filter_select(3)
        opts_date = self.events_page.get_open_options()
        choose_date = opts_date[1].text.strip()
        print(f"  Selecting date option: '{choose_date}'")
        self.events_page.select_option_by_text(choose_date)
        self.events_page.close_dropdown()

        self.events_page.set_date_range("01/01/2024", "01/31/2024")
        print(f"  Set date range: Jan 2024 (past)")

        remaining_cards = self.events_page.get_cards_or_empty_after_wait()

        print(f"  Events after filters: {len(remaining_cards)}")

        self.assertEqual(
            len(remaining_cards),
            0,
            f"Expected 0 events (Future + past date), but found {len(remaining_cards)}",
        )
        


if __name__ == "__main__":
    unittest.main()
