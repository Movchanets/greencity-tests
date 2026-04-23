import allure
import pytest

from data.config import Config
from pages.events_page import EventsPage


@pytest.fixture
def events_page(init_driver):
    page = EventsPage(init_driver)
    page.open(Config.BASE_UI_URL)
    page.wait_until_loaded()
    return page


@allure.feature("Events page")
@allure.story("Open event details")
@allure.title("TC-01 Open event and check details")
def test_TC01_open_event_and_check_details(events_page):
    """TC-01: Відкрити подію зі списку і перевірити деталі."""
    with allure.step("Check events page loaded with event cards"):
        cards = events_page.get_cards()
    with allure.step("Verify event cards are displayed"):
        assert len(cards) > 0, "No event cards found on the page"
    
    with allure.step("Print event card count"):
        print(f"  Found {len(cards)} event cards")

    first_card = cards[0]
    card_title = first_card.get_name()
    with allure.step("Print first event title"):
        print(f"  First event title: '{card_title}'")
    assert len(card_title.strip()) > 0, "Event title is empty"

    first_card.click_more()
    detail_title = events_page.get_detail_title_text()
    with allure.step("Print detail page title"):
        print(f"  Detail page title: '{detail_title}'")
    assert len(detail_title.strip()) > 0, "Detail page title is empty"

    has_location = events_page.page_has_location_hint()
    with allure.step("Print location info"):
        print(f"  Has location info: {has_location}")


@allure.feature("Events page")
@allure.story("Filter events")
@allure.title("TC-02 Filter and reset events")
def test_TC02_filter_and_reset(events_page):
    """TC-02: Застосувати фільтр і скинути його."""
    with allure.step("Check events page loaded with event cards"):
        cards = events_page.get_cards()
    with allure.step("Verify event cards are displayed"):
        assert len(cards) > 0, "No event cards found on the page"
    with allure.step("Print initial event card count"):
        initial_count = events_page.get_cards_count()
        print(f"  Initial events count: {initial_count}")

    mat_selects = events_page.get_filter_selects()
    assert len(mat_selects) > 0, "No filter dropdowns found"
    with allure.step("Print filter dropdown count"):
        print(f"  Found {len(mat_selects)} filter dropdowns")
    with allure.step("Open first filter dropdown and select an option"):
        events_page.open_filter_select(0)

    with allure.step("Get filter options and select the first one"):
        options = events_page.get_open_options()
    with allure.step("Verify filter options are displayed"):
        assert len(options) > 0, "No filter options appeared"
    with allure.step("Print filter options count and select the first option"):
        print(f"  Found {len(options)} filter options")
    with allure.step("Select the first filter option"):
        first_option_text = options[0].text.strip()
    with allure.step("Print selected option"):
        print(f"  Selecting option: '{first_option_text}'")
    with allure.step("Apply filter by selecting the option"):
        events_page.select_option_by_text(first_option_text)
    with allure.step("Wait for events to be filtered and print resulting event count"):
        events_page.wait_until_loaded()
    with allure.step("Print filtered event count"):
        filtered_cards = events_page.get_card_elements()
        print(f"  Events after filter: {len(filtered_cards)}")

    events_page.close_dropdown()
    events_page.click_reset()
    events_page.wait_until_loaded()

    final_cards = events_page.get_card_elements()
    print(f"  Events after reset: {len(final_cards)}")
    assert len(final_cards) > 0, "No event cards found after resetting filters"


@allure.feature("Events page")
@allure.story("Negative filtering")
@allure.title("TC-04 Filter with no results")
def test_TC04_filter_no_results(events_page):
    """TC-04: Негативний тест — Майбутні події + дата в минулому = 0 результатів."""

    initial_count = events_page.get_cards_count()
    print(f"  Initial events count: {initial_count}")

    mat_selects = events_page.get_filter_selects()
    assert len(mat_selects) >= 4, "Not enough filter dropdowns"
    print(f"  Found {len(mat_selects)} filter dropdowns")

    events_page.open_filter_select(1)
    opts_status = events_page.get_open_options()
    future_status = opts_status[1].text.strip()
    print(f"  Selecting status: '{future_status}'")
    events_page.select_option_by_text(future_status)
    events_page.close_dropdown()

    events_page.open_filter_select(3)
    opts_date = events_page.get_open_options()
    choose_date = opts_date[1].text.strip()
    print(f"  Selecting date option: '{choose_date}'")
    events_page.select_option_by_text(choose_date)
    events_page.close_dropdown()

    events_page.set_date_range("01/01/2024", "01/31/2024")
    print("  Set date range: Jan 2024 (past)")

    remaining_cards = events_page.get_cards_or_empty_after_wait()

    print(f"  Events after filters: {len(remaining_cards)}")

    assert len(remaining_cards) == 0, (
        f"Expected 0 events (Future + past date), but found {len(remaining_cards)}"
    )
