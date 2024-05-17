# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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


class Test_login:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

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

        self.driver.implicitly_wait(10)

        self.driver.find_element(By.CSS_SELECTOR, ".alert-success").click()


class Test_createPost:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()
        reset_database()

    def test_post(self):
        self.driver.get("http://127.0.0.1:5000")
        self.driver.set_window_size(1245, 1040)
        self.driver.find_element(By.LINK_TEXT, "Log In").click()
        self.driver.find_element(By.ID, "login-email").click()
        self.driver.find_element(By.ID, "login-email").send_keys("alice@example.com")
        self.driver.find_element(By.ID, "login-password").click()
        self.driver.find_element(By.ID, "login-password").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(6)").click()

        self.driver.implicitly_wait(10)

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

        self.driver.implicitly_wait(10)

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


class Test_checkReplies:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()
        reset_database()

    def test_checkReplies(self):
        self.driver.get("http://127.0.0.1:5000")
        self.driver.set_window_size(1245, 1040)
        self.driver.find_element(By.LINK_TEXT, "Browse Posts").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".card:nth-child(4) .btn-info"
        ).click()
        assert (
            self.driver.find_element(By.CSS_SELECTOR, "#replies-1 .card-subtitle").text
            == "Reply by Anonymous"
        )
        self.driver.find_element(
            By.CSS_SELECTOR, ".card:nth-child(6) .btn-info"
        ).click()
        assert (
            self.driver.find_element(By.CSS_SELECTOR, "#replies-2 .card-subtitle").text
            == "Reply by Anonymous"
        )
        self.driver.find_element(
            By.CSS_SELECTOR, ".card:nth-child(8) .btn-info"
        ).click()
        assert (
            self.driver.find_element(By.CSS_SELECTOR, "#replies-3 .card-subtitle").text
            == "Reply by Anonymous"
        )


class Test_passwordChange:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}
        reset_database()

    def teardown_method(self, method):
        self.driver.quit()
        reset_database()

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

        time.sleep(0.5)

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
