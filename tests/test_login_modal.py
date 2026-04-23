import pytest

from data.config import Config


@pytest.mark.skipif(
    not Config.EMAIL or not Config.PASSWORD,
    reason="LOGIN credentials are not configured in data/.env",
)
def test_login_successfully(home_page):
    login_modal = home_page.click_sign_in()

    assert login_modal.is_displayed(), "Login modal is not displayed"
    login_modal.enter_email(Config.EMAIL)
    login_modal.enter_password(Config.PASSWORD)
    login_modal.click_sign_in()

    assert login_modal.wait_until_it_disappears(), "Login modal should disappear after successful login"


def test_login_with_invalid_credentials(home_page):
    login_modal = home_page.click_sign_in()

    assert login_modal.is_displayed(), "Login modal is not displayed"
    login_modal.enter_email("invalid@example.com")
    login_modal.enter_password("invalidpassword")
    login_modal.click_sign_in()

    assert login_modal.is_displayed(), "Login modal should remain visible after failed login"
    assert not login_modal.wait_until_it_disappears(timeout=3), "Login modal should stay open after failed login"