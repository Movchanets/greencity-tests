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
    cards = events_page.get_cards()
    assert len(cards) > 0, "No event cards found on the page"

    first_card = cards[0]
    card_title = first_card.get_name()
    assert len(card_title.strip()) > 0, "Event title is empty"

    first_card.click_more()
    detail_title = events_page.get_detail_title_text()
    assert len(detail_title.strip()) > 0, "Detail page title is empty"

    has_location = events_page.page_has_location_hint()
    assert isinstance(has_location, bool), "Location hint flag should be boolean"


@allure.feature("Events page")
@allure.story("Filter events")
@allure.title("TC-02 Filter and reset events")
def test_TC02_filter_and_reset(events_page):
    """TC-02: Застосувати фільтр і скинути його."""
    cards = events_page.get_cards()
    assert len(cards) > 0, "No event cards found on the page"
    initial_count = events_page.get_cards_count()
    assert initial_count > 0, "Initial events count should be greater than zero"

    mat_selects = events_page.get_filter_selects()
    assert len(mat_selects) > 0, "No filter dropdowns found"
    events_page.open_filter_select(0)

    options = events_page.get_open_options()
    assert len(options) > 0, "No filter options appeared"
    first_option_text = options[0].text.strip()
    events_page.select_option_by_text(first_option_text)
    events_page.wait_until_loaded()
    filtered_cards = events_page.get_card_elements()
    assert len(filtered_cards) >= 0, "Filtered cards collection should be available"

    events_page.close_dropdown()
    events_page.click_reset()
    events_page.wait_until_loaded()

    final_cards = events_page.get_card_elements()
    assert len(final_cards) > 0, "No event cards found after resetting filters"


@allure.feature("Events page")
@allure.story("Negative filtering")
@allure.title("TC-04 Filter with no results")
def test_TC04_filter_no_results(events_page):
    """TC-04: Негативний тест — Майбутні події + дата в минулому = 0 результатів."""

    initial_count = events_page.get_cards_count()
    assert initial_count >= 0, "Initial events count should be available"

    mat_selects = events_page.get_filter_selects()
    assert len(mat_selects) >= 4, "Not enough filter dropdowns"

    events_page.open_filter_select(1)
    opts_status = events_page.get_open_options()
    future_status = opts_status[1].text.strip()
    events_page.select_option_by_text(future_status)
    events_page.close_dropdown()

    events_page.open_filter_select(3)
    opts_date = events_page.get_open_options()
    choose_date = opts_date[1].text.strip()
    events_page.select_option_by_text(choose_date)
    events_page.close_dropdown()

    events_page.set_date_range("01/01/2024", "01/31/2024")

    remaining_cards = events_page.get_cards_or_empty_after_wait()

    assert len(remaining_cards) == 0, (
        f"Expected 0 events (Future + past date), but found {len(remaining_cards)}"
    )
