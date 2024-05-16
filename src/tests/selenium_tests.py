from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import runpy
import sys
from pathlib import Path

current_dir = Path(__file__).resolve()
parent_dir = current_dir.parents[2]
sys.path.append(str(parent_dir))


def reset_database():
    runpy.run_module("generate_example_db", run_name="__main__")


# Make sure the sample database has been generated before testing
reset_database()


def test_login(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.LINK_TEXT, "Log In").click()
    driver.find_element(By.NAME, "email").send_keys("alice@example.com")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, ".alert"), "Successfully logged in"
        )
    )
    reset_database()


if __name__ == "__main__":
    driver = webdriver.Chrome()  # or webdriver.Firefox() or any other browser
    try:
        test_login(driver)
        test_password_change(driver)
        # Call other tests similarly...
    finally:
        driver.quit()
