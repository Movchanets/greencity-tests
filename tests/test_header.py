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
    with allure.step(f"Switch language to '{language}' and check header links"):
      home_page.switch_language(language)
    with allure.step("Check events link text updates"):
        event_link = home_page.get_events_link()
    with allure.step("Verify events link is displayed and has correct text"):
        assert event_link.is_displayed(), "Events link is not displayed"
    with allure.step("Verify events link text updates according to selected language"):
        assert expected_text in event_link.text, "Events link text is incorrect"


@allure.feature("Header")
@allure.story("Navigation")
@allure.title("Header navigation goes to events page")
def test_header_navigation_to_events_page(home_page):
    with allure.step("Navigate to events page using header link"):  
        home_page.navigate_to_events()
    with allure.step("Initialize events page and check it loaded"):
        events_page = EventsPage(home_page.driver)
        events_page.wait_until_loaded()
    with allure.step("Verify events page loaded by checking header and event cards"):
        assert events_page.get_cards_count() > 0, "No event cards found on the events page"
    with allure.step("Verify events page header is displayed"):
        assert events_page.get_main_header().is_displayed(), "Events page header is not displayed"