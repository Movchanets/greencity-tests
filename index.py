from selenium import webdriver
from selenium.webdriver. common.by import By
import time

if __name__ == "__main__":
    driver = webdriver. Chrome()
    driver.get("https://www.greencity.cx.ua/#/greenCity")
    time.sleep(2)
    sign_in_button = driver. find_element(By.XPATH, "//button[contains(text(), 'Sign In' ) ]")
    sign_in_button.click()
    time.sleep(2) # Wait for the sign-in form to load
    driver.quit()