import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

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


class Test_selenium:
    def setup_method(self, method):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Enable headless mode
        # chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1200")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.vars = {}
        reset_database()

    def teardown_method(self, method):
        self.driver.quit()
        reset_database()

    def test_login(self):
        self.driver.get("http://127.0.0.1:5000/auth/login")
        self.driver.set_window_size(1245, 1040)
        self.driver.find_element(By.LINK_TEXT, "Log In").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(6)").click()
        self.driver.find_element(By.ID, "login-email").send_keys("alice@example.com")
        self.driver.find_element(By.ID, "login-password").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(6)").click()

        time.sleep(0.1)

        self.driver.find_element(By.CSS_SELECTOR, ".alert-success").click()

    def test_createPost(self):
        self.driver.get("http://127.0.0.1:5000")
        self.driver.set_window_size(1245, 1040)
        self.driver.find_element(By.LINK_TEXT, "Log In").click()
        self.driver.find_element(By.ID, "login-email").click()
        self.driver.find_element(By.ID, "login-email").send_keys("alice@example.com")
        self.driver.find_element(By.ID, "login-password").click()
        self.driver.find_element(By.ID, "login-password").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(6)").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Successfully logged in\n×"
        )
        self.driver.find_element(
            By.CSS_SELECTOR, ".col-md-3:nth-child(2) .card-title"
        ).click()
        self.driver.find_element(By.NAME, "title").click()
        self.driver.find_element(By.NAME, "title").send_keys("Selenium Test")
        self.driver.find_element(By.NAME, "content").click()
        self.driver.find_element(By.NAME, "content").send_keys("Testing 123")
        self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(7)").click()

        time.sleep(0.1)
        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Post created successfully!\n×"
        )

        self.driver.implicitly_wait(10)

        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".card:nth-child(4) .card-title"
            ).text
            == "Selenium Test"
        )

    def test_checkReplies(self):
        self.driver.get("http://127.0.0.1:5000")
        self.driver.set_window_size(1245, 1040)
        self.driver.find_element(By.LINK_TEXT, "Browse Posts").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".card:nth-child(4) .btn-info"
        ).click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, "#replies-1 .card-subtitle").text
            == "Reply by Anonymous"
        )
        self.driver.find_element(
            By.CSS_SELECTOR, ".card:nth-child(6) .btn-info"
        ).click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, "#replies-2 .card-subtitle").text
            == "Reply by Anonymous"
        )
        self.driver.find_element(
            By.CSS_SELECTOR, ".card:nth-child(8) .btn-info"
        ).click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, "#replies-3 .card-subtitle").text
            == "Reply by Anonymous"
        )

    def test_passwordChange(self):
        self.driver.get("http://127.0.0.1:5000")
        self.driver.set_window_size(1285, 1039)
        self.driver.find_element(By.CSS_SELECTOR, "body").click()
        self.driver.find_element(By.LINK_TEXT, "Log In").click()
        element = self.driver.find_element(By.LINK_TEXT, "Log In")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "#loginModal .modal-header").click()
        self.driver.find_element(By.ID, "login-email").click()
        self.driver.find_element(By.ID, "login-email").send_keys("alice@example.com")
        self.driver.find_element(By.ID, "login-password").click()
        self.driver.find_element(By.ID, "login-password").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(6)").click()

        time.sleep(0.5)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Successfully logged in\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Alice Johnson").click()
        self.driver.find_element(By.ID, "changePasswordButton").click()
        self.driver.find_element(By.ID, "current_password").click()
        self.driver.find_element(By.ID, "current_password").send_keys("password123")
        self.driver.find_element(By.ID, "new_password").click()
        self.driver.find_element(By.ID, "new_password").send_keys("password1234")
        self.driver.find_element(By.ID, "confirm_password").click()
        self.driver.find_element(By.ID, "confirm_password").send_keys("password1234")
        self.driver.find_element(By.CSS_SELECTOR, "#passwordForm > .btn").click()

        time.sleep(0.5)

        assert (
            self.driver.find_element(By.ID, "passwordError").text
            == "Password must contain at least one uppercase letter."
        )
        self.driver.find_element(By.ID, "new_password").clear()
        self.driver.find_element(By.ID, "confirm_password").clear()
        self.driver.find_element(By.ID, "new_password").click()
        self.driver.find_element(By.ID, "new_password").send_keys("Password1234")
        self.driver.find_element(By.ID, "confirm_password").click()
        self.driver.find_element(By.ID, "confirm_password").send_keys("Password1234")
        self.driver.find_element(By.CSS_SELECTOR, "#passwordForm > .btn").click()

        time.sleep(0.5)

        assert (
            self.driver.find_element(By.ID, "passwordError").text
            == "Password must contain at least one special character."
        )
        self.driver.find_element(By.ID, "new_password").clear()
        self.driver.find_element(By.ID, "confirm_password").clear()
        self.driver.find_element(By.ID, "new_password").click()
        self.driver.find_element(By.ID, "new_password").send_keys("Password1234!")
        self.driver.find_element(By.ID, "confirm_password").click()
        self.driver.find_element(By.ID, "confirm_password").send_keys("Password1234!")
        self.driver.find_element(By.CSS_SELECTOR, "#passwordForm > .btn").click()

        time.sleep(0.3)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Password successfully updated\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Log Out").click()

        time.sleep(0.5)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "You have been logged out.\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Log In").click()
        self.driver.find_element(By.ID, "login-email").click()
        self.driver.find_element(By.ID, "login-email").send_keys("alice@example.com")
        self.driver.find_element(By.ID, "login-password").click()
        self.driver.find_element(By.ID, "login-password").send_keys("Password1234!")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(6)").click()

        time.sleep(0.5)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Successfully logged in\n×"
        )

    def test_notificationcheck(self):
        self.driver.get("http://127.0.0.1:5000")
        self.driver.set_window_size(1285, 1039)
        self.driver.find_element(By.LINK_TEXT, "Log In").click()
        self.driver.find_element(By.ID, "login-email").click()
        self.driver.find_element(By.ID, "login-email").send_keys("alice@example.com")
        self.driver.find_element(By.ID, "login-password").send_keys("password123")
        self.driver.find_element(By.ID, "login-password").send_keys(Keys.ENTER)

        time.sleep(0.1)

        self.driver.find_element(By.CSS_SELECTOR, ".centered-content").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Successfully logged in\n×"
        )
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".col-md-3:nth-child(3) .card-title"
            ).text
            == "Responses1"
        ) or (
            self.driver.find_element(
                By.CSS_SELECTOR, ".col-md-3:nth-child(3) .card-title"
            ).text
            == "Responses2"
        )

        time.sleep(0.1)

        self.driver.find_element(By.LINK_TEXT, "Notifications").click()

        time.sleep(0.1)

        assert self.driver.find_element(By.LINK_TEXT, "Bob Smith").text == "Bob Smith"
        assert (
            self.driver.find_element(By.LINK_TEXT, "Carol Martinez").text
            == "Carol Martinez"
        )
        self.driver.find_element(By.CSS_SELECTOR, ".alert:nth-child(2) span").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Notification dismissed.\n×"
        )
        self.driver.find_element(By.CSS_SELECTOR, "form span").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Notification dismissed.\n×"
        )

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, "p").text
            == "No notifications to show."
        )
        self.driver.find_element(By.LINK_TEXT, "Love Letters").click()
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".col-md-3:nth-child(3) .card-title"
            ).text
            == "Responses0"
        )

    def test_checkBrowse(self):
        self.driver.get("http://127.0.0.1:5000")
        self.driver.set_window_size(1245, 1040)
        self.driver.find_element(By.CSS_SELECTOR, ".centered-content").click()
        self.driver.find_element(By.LINK_TEXT, "Browse Posts").click()
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".card:nth-child(4) .card-title"
            ).text
            == "Alice's Post #1"
        )
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".card:nth-child(6) .card-title"
            ).text
            == "Alice's Post #2"
        )
        self.driver.execute_script("window.scrollTo(0,800)")
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".card:nth-child(8) .card-title"
            ).text
            == "Alice's Post #3"
        )
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".card:nth-child(10) .card-title"
            ).text
            == "Bob's Post #1"
        )
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".card:nth-child(12) .card-title"
            ).text
            == "Bob's Post #2"
        )
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".card:nth-child(14) .card-title"
            ).text
            == "Bob's Post #3"
        )
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".card:nth-child(16) .card-title"
            ).text
            == "Carol's Post #1"
        )
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".card:nth-child(18) .card-title"
            ).text
            == "Carol's Post #2"
        )
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".card:nth-child(20) .card-title"
            ).text
            == "Carol's Post #3"
        )

    def test_makeReplies(self):
        self.driver.get("http://127.0.0.1:5000")
        self.driver.set_window_size(1285, 1039)
        self.driver.find_element(By.LINK_TEXT, "Log In").click()
        self.driver.find_element(By.ID, "login-email").click()
        self.driver.find_element(By.ID, "login-email").send_keys("alice@example.com")
        self.driver.find_element(By.ID, "login-password").send_keys("password123")
        self.driver.find_element(By.ID, "login-password").send_keys(Keys.ENTER)

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Successfully logged in\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Browse Posts").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".card:nth-child(4) .d-flex > .btn-primary"
        ).click()
        self.driver.find_element(By.NAME, "content").click()
        self.driver.find_element(By.NAME, "content").send_keys("Sent from Selenium")

        time.sleep(0.1)

        self.driver.find_element(
            By.CSS_SELECTOR, ".modal-footer > .btn-primary"
        ).click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, "#replies-1 > .card:nth-child(1) .card-subtitle"
            ).text
            == "Reply by You"
        )
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, "#replies-1 > .card:nth-child(1) .card-text"
            ).text
            == "Sent from Selenium"
        )

    def test_profileEdit(self):
        self.driver.get("http://127.0.0.1:5000")
        self.driver.set_window_size(1167, 1020)
        self.driver.find_element(By.LINK_TEXT, "Log In").click()
        self.driver.find_element(By.ID, "login-email").click()
        self.driver.find_element(By.ID, "login-email").send_keys("alice@example.com")
        self.driver.find_element(By.ID, "login-password").send_keys("password123")
        self.driver.find_element(By.ID, "login-password").send_keys(Keys.ENTER)

        time.sleep(0.1)

        self.driver.find_element(By.LINK_TEXT, "Alice Johnson").click()
        assert (
            self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(5)").text
            == "Gender: Female"
        )
        assert (
            self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(7)").text
            == "Instagram: alice_j"
        )
        assert (
            self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(9)").text
            == "Snapchat: Not provided"
        )

        time.sleep(0.1)

        self.driver.find_element(By.ID, "editButton").click()

        time.sleep(0.1)

        self.driver.find_element(By.ID, "edit_instagram").clear()
        self.driver.find_element(By.ID, "edit_instagram").click()
        self.driver.find_element(By.ID, "edit_instagram").send_keys("alice_james")
        self.driver.find_element(By.ID, "edit_snapchat").clear()
        self.driver.find_element(By.ID, "edit_snapchat").click()
        self.driver.find_element(By.ID, "edit_snapchat").send_keys("Selenium")

        time.sleep(0.1)

        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(9)").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Account details successfully updated\n×"
        )
        assert (
            self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(7)").text
            == "Instagram: alice_james"
        )
        assert (
            self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(9)").text
            == "Snapchat: Selenium"
        )

    def test_notificationMake(self):
        self.driver.get("http://127.0.0.1:5000")
        self.driver.set_window_size(1167, 1020)
        self.driver.find_element(By.LINK_TEXT, "Sign Up").click()
        self.driver.find_element(By.ID, "first_name").click()
        self.driver.find_element(By.ID, "first_name").send_keys("Selenium")
        self.driver.find_element(By.ID, "last_name").send_keys("Test")
        self.driver.find_element(By.ID, "gender").click()
        dropdown = self.driver.find_element(By.ID, "gender")
        dropdown.find_element(By.XPATH, "//option[. = 'Male']").click()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("selenium@example.com")
        self.driver.find_element(By.ID, "password").send_keys("Password123!")
        self.driver.find_element(By.ID, "instagram").click()
        self.driver.find_element(By.ID, "instagram").send_keys("selenium")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(13)").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Account successfully created\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Log In").click()
        element = self.driver.find_element(By.LINK_TEXT, "Log In")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.ID, "login-email").click()
        self.driver.find_element(By.ID, "login-email").send_keys("selenium@example.com")
        self.driver.find_element(By.ID, "login-password").send_keys("Password123!")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(6)").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Successfully logged in\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Browse Posts").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".card:nth-child(4) form > .btn"
        ).click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Connect request sent.\n×"
        )
        self.driver.find_element(
            By.CSS_SELECTOR, ".card:nth-child(10) form > .btn"
        ).click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Connect request sent.\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Log Out").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "You have been logged out.\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Log In").click()
        self.driver.find_element(By.ID, "login-email").click()
        self.driver.find_element(By.ID, "login-email").send_keys("alice@example.com")
        self.driver.find_element(By.ID, "login-password").send_keys("password123")
        self.driver.find_element(By.ID, "login-password").send_keys(Keys.ENTER)

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Successfully logged in\n×"
        )

        time.sleep(0.1)

        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".col-md-3:nth-child(3) .card-title"
            ).text
            == "Responses3"
        )
        self.driver.find_element(By.LINK_TEXT, "Notifications").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.LINK_TEXT, "Selenium Test").text
            == "Selenium Test"
        )
        self.driver.find_element(By.LINK_TEXT, "Log Out").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "You have been logged out.\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Log In").click()
        self.driver.find_element(By.ID, "login-email").click()
        self.driver.find_element(By.ID, "login-email").send_keys("bob@example.com")
        self.driver.find_element(By.ID, "login-password").send_keys("password123")
        self.driver.find_element(By.ID, "login-password").send_keys(Keys.ENTER)

        time.sleep(0.1)

        self.driver.find_element(By.LINK_TEXT, "Notifications").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.LINK_TEXT, "Selenium Test").text
            == "Selenium Test"
        )

    def test_likeButton(self):
        self.driver.get("http://127.0.0.1:5000")
        self.driver.set_window_size(1227, 1020)
        self.driver.find_element(By.LINK_TEXT, "Log In").click()
        self.driver.find_element(By.ID, "login-email").click()
        self.driver.find_element(By.ID, "login-email").send_keys("alice@example.com")
        self.driver.find_element(By.ID, "login-password").send_keys("password123")
        self.driver.find_element(By.ID, "login-password").send_keys(Keys.ENTER)
        time.sleep(0.1)
        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Successfully logged in\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Browse Posts").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".card:nth-child(4) .d-flex > .btn-outline-primary"
            ).text
            == "Like (0)"
        )

        time.sleep(0.1)

        self.driver.find_element(
            By.CSS_SELECTOR, ".card:nth-child(4) .d-flex > .btn-outline-primary"
        ).click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".card:nth-child(4) .d-flex > .btn-outline-primary"
            ).text
            == "Unlike (1)"
        )
        self.driver.find_element(By.LINK_TEXT, "Log Out").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "You have been logged out.\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Log In").click()
        element = self.driver.find_element(By.LINK_TEXT, "Log In")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.ID, "login-email").click()
        self.driver.find_element(By.ID, "login-email").send_keys("bob@example.com")
        self.driver.find_element(By.ID, "login-password").send_keys("password123")
        self.driver.find_element(By.ID, "login-password").send_keys(Keys.ENTER)

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Successfully logged in\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Browse Posts").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".card:nth-child(4) .d-flex > .btn-outline-primary"
            ).text
            == "Like (1)"
        )
        self.driver.find_element(
            By.CSS_SELECTOR, ".card:nth-child(4) .d-flex > .btn-outline-primary"
        ).click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".card:nth-child(4) .d-flex > .btn-outline-primary"
            ).text
            == "Unlike (2)"
        )

    def test_notLoggedIn(self):
        self.driver.get("http://127.0.0.1:5000")
        self.driver.set_window_size(1227, 1020)
        self.driver.find_element(By.LINK_TEXT, "Create Post").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-warning").text
            == "You must log in to access this page.\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Notifications").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-warning").text
            == "You must log in to access this page.\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Browse Posts").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".card:nth-child(4) form > .btn"
        ).click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-dismissible").text
            == "You need to login to connect.\n×"
        )

    def test_accountValidation(self):
        self.driver.get("http://127.0.0.1:5000")
        self.driver.set_window_size(1357, 1020)
        self.driver.find_element(By.LINK_TEXT, "Sign Up").click()
        self.driver.find_element(By.ID, "first_name").click()
        self.driver.find_element(By.ID, "first_name").send_keys("123")
        self.driver.find_element(By.ID, "last_name").send_keys("123")
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("test")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("1")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(13)").click()
        self.driver.find_element(By.ID, "email").clear()
        self.driver.find_element(By.ID, "email").send_keys("test@")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(13)").click()
        self.driver.find_element(By.ID, "email").clear()
        self.driver.find_element(By.ID, "email").send_keys("test@test")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(13)").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".form-group:nth-child(3) > .error-message"
            ).text
            == "First Name should contain only alphabetic characters."
        )
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".form-group:nth-child(4) > .error-message"
            ).text
            == "Last Name should contain only alphabetic characters."
        )
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".form-group:nth-child(6) > .error-message"
            ).text
            == "Invalid email format."
        )
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".form-group:nth-child(7) > .error-message"
            ).text
            == "Password must be at least 8 characters long."
        )
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".error-message:nth-child(13)"
            ).text
            == "At least one social media handle must be provided"
        )
        self.driver.find_element(By.ID, "first_name").click()
        self.driver.find_element(By.ID, "first_name").clear()
        self.driver.find_element(By.ID, "first_name").send_keys("a")
        self.driver.find_element(By.ID, "last_name").click()
        self.driver.find_element(By.ID, "last_name").clear()
        self.driver.find_element(By.ID, "last_name").send_keys("a")
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").clear()
        self.driver.find_element(By.ID, "email").send_keys("test@test.com")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys("1aaaaaaa")
        self.driver.find_element(By.ID, "instagram").click()
        self.driver.find_element(By.ID, "instagram").send_keys("a")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(14)").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".error-message").text
            == "Password must contain at least one uppercase letter."
        )
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys("1aaaaaaA")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(13)").click()
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys("1aaaaaaA!")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(13)").click()

        time.sleep(0.1)

        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Account successfully created\n×"
        )
