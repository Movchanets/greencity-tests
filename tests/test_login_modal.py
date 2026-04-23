import allure
import pytest

from data.config import Config


@allure.feature("Authentication")
@allure.story("Successful login")
@allure.title("Login succeeds with valid credentials")
@pytest.mark.skipif(
    not Config.EMAIL or not Config.PASSWORD,
    reason="LOGIN credentials are not configured in data/.env",
)
def test_login_successfully(home_page):
    with allure.step("Open login modal and attempt to login with valid credentials"):
        login_modal = home_page.click_sign_in()
    
    with allure.step("Verify login modal is displayed and enter valid credentials"):
            assert login_modal.is_displayed(), "Login modal is not displayed"
    with allure.step("Enter valid email and password, then click sign in"):
        login_modal.enter_email(Config.EMAIL)
        login_modal.enter_password(Config.PASSWORD)
        login_modal.click_sign_in()
    with allure.step("Verify login modal disappears after successful login"):
        assert login_modal.wait_until_it_disappears(), "Login modal should disappear after successful login"


@allure.feature("Authentication")
@allure.story("Negative login")
@allure.title("Login stays open with invalid credentials")
def test_login_with_invalid_credentials(home_page):
    with allure.step("Open login modal and attempt to login with invalid credentials"):
        login_modal = home_page.click_sign_in()
    with allure.step("Verify login modal remains open and shows error messages"):
        assert login_modal.is_displayed(), "Login modal is not displayed"
    with allure.step("Enter invalid email and password, then click sign in"):
        login_modal.enter_email("invalid@example.com")
        login_modal.enter_password("invalidpassword")
        login_modal.click_sign_in()

    with allure.step("Verify login modal remains visible after failed login"):
        assert login_modal.is_displayed(), "Login modal should remain visible after failed login"
    with allure.step("Verify login modal stays open after failed login"):
        assert not login_modal.wait_until_it_disappears(timeout=3), "Login modal should stay open after failed login"