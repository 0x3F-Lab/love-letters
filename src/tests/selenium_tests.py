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
    
    # Wait until the "Log In" link is present and clickable
    login_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Login"))
    )
    login_link.click()
    
    # Wait until the email input field is present
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    email_field.send_keys("alice@example.com")
    
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys("password123")
    password_field.send_keys(Keys.RETURN)
    
    # Wait until the success message is present
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".alert"), "Successfully logged in")
    )
    reset_database()

if __name__ == "__main__":
    driver = webdriver.Chrome()  # or webdriver.Firefox() or any other browser
    try:
        test_login(driver)
        # Call other tests similarly...
    finally:
        driver.quit()
