from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class BaseComponent:
    
    def __init__(self, root:WebElement):
        self.node = root
        self.driver = root.parent

    def find_element(self, by=By.XPATH, value=None):
        return self.node.find_element(by, value)

    def find_elements(self, by=By.XPATH, value=None):
        return self.node.find_elements(by, value)

    def scroll_to(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )