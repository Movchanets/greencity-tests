from selenium import webdriver
from selenium.webdriver.common.by import By
import time

if __name__ == "__main__":
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://www.greencity.cx.ua/#/greenCity")
        time.sleep(2)
        sign_in_button = driver.find_element(By.XPATH, "/html/body/app-root/app-main/div/app-header/header/div[2]/div/div/div/ul/a")
        sign_in_button.click()
        time.sleep(2)  # Wait for the sign-in form to load
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        email_input.send_keys("test@email.com")
        time.sleep(2)
        password_input.send_keys("testpassword")
        time.sleep(3)
        submit_button = driver.find_element(By.XPATH, "//button[contains(normalize-space(.), 'Sign in') or contains(normalize-space(.), 'Увійти')]")
        submit_button.click()
        time.sleep(5)  # Wait for the login process to complete
        driver.quit()
