from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.components.base_component import BaseComponent


class SigninModal(BaseComponent):
    email = (By.ID, "email")
    password = (By.ID, "password")
    forgot_password = (By.CLASS_NAME, "forgot-password")
    sign_in_button = (By.XPATH, "//app-sign-in//button[@type='submit']")
    sign_up_button = (By.XPATH, '//a[contains(text(), "Sign up")]')
    close_button = (By.CLASS_NAME, "close-modal-window")
    email_error = (By.ID, "email-err-msg")
    password_error = (By.ID, "pass-err-msg")

    def enter_email(self, email):
        email_field = self.find_element(*self.email)
        email_field.clear()
        email_field.send_keys(email)

    def enter_password(self, password):
        password_field = self.find_element(*self.password)
        password_field.clear()
        password_field.send_keys(password)

    def click_forgot_password(self):
        self.find_element(*self.forgot_password).click()

    def click_sign_in(self):
        self.find_element(*self.sign_in_button).click()

    def click_sign_up(self):
        self.find_element(*self.sign_up_button).click()

    def close(self):
        self.find_element(*self.close_button).click()

    def wait_until_it_disappears(self, timeout=10):
        try:
            self._get_wait(timeout).until(EC.invisibility_of_element_located(self.email))
            return True
        except Exception:
            return False

    def is_displayed(self):
        return self.node.is_displayed()

    def email_error_message(self):
        return self.find_element(*self.email_error).text

    def password_error_message(self):
        return self.find_element(*self.password_error).text

    def email_error_is_displayed(self):
        return self.find_element(*self.email_error).is_displayed()

    def password_error_is_displayed(self):
        return self.find_element(*self.password_error).is_displayed()