from pathlib import Path

import pytest
from selenium import webdriver

from data.config import Config
from pages.base_page import BasePage


@pytest.fixture(scope="function")
def init_driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument(f"--lang={Config.BROWSER_LANG}")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if Config.HEADLESS_MODE:
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(Config.IMPLICIT_WAIT_TIMEOUT)

    yield driver

    screenshots_dir = Path(__file__).parent / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    screenshot_name = f"{request.node.name}.png"
    driver.save_screenshot(str(screenshots_dir / screenshot_name))
    driver.quit()


@pytest.fixture(scope="function")
def home_page(init_driver):
    page = BasePage(init_driver)
    page.open(Config.BASE_UI_URL)
    return page
