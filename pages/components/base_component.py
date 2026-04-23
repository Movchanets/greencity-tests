from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BaseComponent:
    
    def __init__(self, root:WebElement):
        self.node = root
        self.driver = root.parent

    def _get_wait(self, timeout=10):
        return WebDriverWait(self.driver, timeout)

    def find_element(self, by=By.XPATH, value=None):
        return self.node.find_element(by, value)

    def find_elements(self, by=By.XPATH, value=None):
        return self.node.find_elements(by, value)

    def wait_for_presence(self, locator, timeout=10):
        return self._get_wait(timeout).until(EC.presence_of_element_located(locator))

    def wait_for_visible(self, locator, timeout=10):
        return self._get_wait(timeout).until(EC.visibility_of_element_located(locator))

    def scroll_to(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )