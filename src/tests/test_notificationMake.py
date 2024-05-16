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


class TestNotificationMake:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

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
        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Account successfully created\\\\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Log In").click()
        element = self.driver.find_element(By.LINK_TEXT, "Log In")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element, 0, 0).perform()
        self.driver.find_element(By.ID, "login-email").click()
        self.driver.find_element(By.ID, "login-email").send_keys("selenium@example.com")
        self.driver.find_element(By.ID, "login-password").send_keys("Password123!")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(6)").click()
        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Successfully logged in\\\\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Browse Posts").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".card:nth-child(4) form > .btn"
        ).click()
        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Connect request sent.\\\\n×"
        )
        self.driver.find_element(
            By.CSS_SELECTOR, ".card:nth-child(10) form > .btn"
        ).click()
        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Connect request sent.\\\\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Log Out").click()
        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "You have been logged out.\\\\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Log In").click()
        self.driver.find_element(By.ID, "login-email").click()
        self.driver.find_element(By.ID, "login-email").send_keys("alice@example.com")
        self.driver.find_element(By.ID, "login-password").send_keys("password123")
        self.driver.find_element(By.ID, "login-password").send_keys(Keys.ENTER)
        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "Successfully logged in\\\\n×"
        )
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".col-md-3:nth-child(3) .card-title"
            ).text
            == "Responses3"
        )
        self.driver.find_element(By.LINK_TEXT, "Notifications").click()
        assert (
            self.driver.find_element(By.LINK_TEXT, "Selenium Test").text
            == "Selenium Test"
        )
        self.driver.find_element(By.LINK_TEXT, "Log Out").click()
        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".alert-success").text
            == "You have been logged out.\\\\n×"
        )
        self.driver.find_element(By.LINK_TEXT, "Log In").click()
        self.driver.find_element(By.ID, "login-email").click()
        self.driver.find_element(By.ID, "login-email").send_keys("bob@example.com")
        self.driver.find_element(By.ID, "login-password").send_keys("password123")
        self.driver.find_element(By.ID, "login-password").send_keys(Keys.ENTER)
        self.driver.find_element(By.LINK_TEXT, "Notifications").click()
        assert (
            self.driver.find_element(By.LINK_TEXT, "Selenium Test").text
            == "Selenium Test"
        )
