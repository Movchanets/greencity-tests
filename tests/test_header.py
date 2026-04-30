import allure
import pytest

from pages.events_page import EventsPage


@allure.feature("Header")
@allure.story("Language switch")
@allure.title("Switch header language updates links")
@pytest.mark.parametrize(
    ("language", "expected_text"),
    [
        ("ua", "Події"),
        ("en", "Events"),
    ],
)
def test_switch_language_updates_header_links(home_page, language, expected_text):
    home_page.switch_language(language)
    event_link = home_page.get_events_link()
    assert event_link.is_displayed(), "Events link is not displayed"
    assert expected_text in event_link.text, "Events link text is incorrect"


@allure.feature("Header")
@allure.story("Navigation")
@allure.title("Header navigation goes to events page")
def test_header_navigation_to_events_page(home_page):
    home_page.navigate_to_events()
    events_page = EventsPage(home_page.driver)
    events_page.wait_until_loaded()
    assert events_page.get_cards_count() > 0, "No event cards found on the events page"
    assert events_page.get_main_header().is_displayed(), "Events page header is not displayed"