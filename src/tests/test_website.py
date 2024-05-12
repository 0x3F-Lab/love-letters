# Playwright imports
import re
from playwright.sync_api import Page, expect

# All to get and run the generate_example_db.py script
# Will need to change if we change the path of the script though
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


# Logs into Alice's account, and checks that it was successful
def test_login(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.get_by_role("link", name="Log In").click()
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("alice@example.com")
    page.get_by_role("textbox", name="Email").press("Tab")
    page.get_by_role("textbox", name="Password").fill("password123")
    page.get_by_role("button", name="Log In").click()
    expect(page.get_by_role("alert")).to_contain_text("Successfully logged in ×")

    reset_database()


# Logs in to Alice's account, changes the password, fighting against validation, and then signs out,
# then checks that the old password doesn't work, then checks that the new one does
def test_passwordChange(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.get_by_role("link", name="Log In").click()
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("alice@example.com")
    page.get_by_role("textbox", name="Email").press("Tab")
    page.get_by_role("textbox", name="Password").fill("password123")
    page.get_by_role("button", name="Log In").click()
    page.get_by_role("heading", name="My Account").click()

    page.get_by_role("button", name="Change Password").click()
    page.locator("#current_password").click()
    page.locator("#current_password").fill("password123")
    page.locator("#current_password").press("Tab")
    page.get_by_role("textbox", name="Uppercase, lowercase, number").fill(
        "password1234"
    )
    page.locator("#confirm_password").click()
    page.locator("#confirm_password").fill("password1234")
    page.get_by_role("button", name="Update Password").click()
    expect(page.locator("#passwordError")).to_contain_text(
        "Password must contain at least one uppercase letter."
    )

    page.get_by_role("textbox", name="Uppercase, lowercase, number").click()
    page.get_by_role("textbox", name="Uppercase, lowercase, number").fill(
        "Password1234"
    )
    page.locator("#confirm_password").click()
    page.locator("#confirm_password").fill("Password1234")
    page.get_by_role("button", name="Update Password").click()
    expect(page.locator("#passwordError")).to_contain_text(
        "Password must contain at least one special character."
    )

    page.get_by_role("textbox", name="Uppercase, lowercase, number").click()
    page.get_by_role("textbox", name="Uppercase, lowercase, number").fill(
        "Password1234!"
    )
    page.locator("#confirm_password").click()
    page.locator("#confirm_password").fill("Password1234!")
    page.get_by_role("button", name="Update Password").click()
    expect(page.get_by_role("alert")).to_contain_text("Password successfully updated ×")

    page.get_by_role("link", name="Log Out").click()
    expect(page.get_by_role("alert")).to_contain_text("You have been logged out. ×")
    page.get_by_role("link", name="Log In").click()
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("alice@example.com")
    page.get_by_role("textbox", name="Email").press("Tab")
    page.get_by_role("textbox", name="Password").fill("password123")
    page.get_by_role("button", name="Log In").click()
    expect(page.locator("#loginError")).to_contain_text("Invalid email or password.")
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("Password1234!")
    page.get_by_role("button", name="Log In").click()
    expect(page.get_by_role("alert")).to_contain_text("Successfully logged in ×")

    reset_database()


# Logs into Alice's account, checks there are 2 responses, then removes them and checks that there are 0
def test_notificationCheck(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.get_by_role("link", name="Log In").click()
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("alice@example.com")
    page.get_by_role("textbox", name="Email").press("Tab")
    page.get_by_role("textbox", name="Password").fill("password123")
    page.get_by_role("textbox", name="Password").press("Enter")
    expect(page.locator("body")).to_contain_text("Responses2")
    page.get_by_role("heading", name="Responses").click()
    expect(page.locator("body")).to_contain_text("Bob Smith")
    expect(page.locator("body")).to_contain_text("Carol Martinez")
    page.get_by_role("button", name="Close").first.click()
    page.locator("form").filter(has_text="×").get_by_label("Close").click()
    page.get_by_role("link", name="Love Letters").click()
    expect(page.locator("body")).to_contain_text("Responses0")

    reset_database()


# Logs into Alice's account, and creates a General Broadcast post,
# then checks that it is created successfully and visible
def test_createPost(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.get_by_role("link", name="Log In").click()
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("alice@example.com")
    page.get_by_role("textbox", name="Email").press("Tab")
    page.get_by_role("textbox", name="Password").fill("password123")
    page.get_by_role("textbox", name="Password").press("Enter")
    page.get_by_role("heading", name="Post Letters").click()
    page.get_by_placeholder("Enter Title").click()
    page.get_by_placeholder("Enter Title").fill("Playwright Test Post")
    page.get_by_placeholder("Enter Title").press("Tab")
    page.get_by_placeholder("Enter your content here").fill(
        "This post was created from a Playwright test"
    )
    page.get_by_role("combobox").select_option("question")
    page.get_by_role("button", name="Submit Post").click()
    expect(page.get_by_role("alert")).to_contain_text("Post created successfully! ×")
    expect(page.get_by_role("heading", name="Playwright Test Post")).to_be_visible()
    expect(page.get_by_text("This post was created from a")).to_be_visible()

    reset_database()


# Goes straight to Browse Letters, and checks if the first two posts of Alice, Bob and Carol are visible.
def test_checkBrowse(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.get_by_role("heading", name="Browse Letters").click()
    expect(page.get_by_role("heading", name="Alice's Post #1")).to_be_visible()
    expect(page.get_by_role("heading", name="Alice's Post #2")).to_be_visible()
    expect(page.get_by_role("heading", name="Bob's Post #1")).to_be_visible()
    expect(page.get_by_role("heading", name="Bob's Post #2")).to_be_visible()
    expect(page.get_by_role("heading", name="Carol's Post #1")).to_be_visible()
    expect(page.get_by_role("heading", name="Carol's Post #2")).to_be_visible()

    reset_database()


# Had to change the generate_example_db to test this, as the randomness was too much
# Logs in as Alice, and then checks that there are replies on the first two posts.
def test_checkReplies(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.get_by_role("link", name="Log In").click()
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("alice@example.com")
    page.get_by_role("textbox", name="Email").press("Tab")
    page.get_by_role("textbox", name="Password").fill("password123")
    page.get_by_role("textbox", name="Password").press("Enter")
    page.get_by_role("heading", name="Browse Letters").click()
    page.locator("button:nth-child(5)").first.click()
    expect(page.locator("#replies-1")).to_contain_text("Reply by Anonymous")
    page.locator("div:nth-child(6) > div > .d-flex > button:nth-child(5)").click()
    expect(page.locator("#replies-2")).to_contain_text("Reply by Anonymous")

    reset_database()


def test_makeReplies(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.get_by_role("link", name="Log In").click()
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("alice@example.com")
    page.get_by_role("textbox", name="Email").press("Tab")
    page.get_by_role("textbox", name="Password").fill("password123")
    page.get_by_role("textbox", name="Password").press("Enter")
    page.get_by_text("Description").first.click()
    page.locator("div:nth-child(6) > div > .d-flex > button").first.click()
    page.get_by_placeholder("Write your reply here...").click()
    page.get_by_placeholder("Write your reply here...").fill("testing")
    page.get_by_role("button", name="Submit Reply").click()
    expect(page.locator("#replies-2")).to_contain_text("Reply by Youtesting")

    reset_database()


def test_profileEdit(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.get_by_role("link", name="Log In").click()
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("alice@example.com")
    page.get_by_role("textbox", name="Email").press("Tab")
    page.get_by_role("textbox", name="Password").fill("password123")
    page.get_by_role("textbox", name="Password").press("Enter")
    page.get_by_role("link", name="Alice Johnson").click()
    expect(page.locator("body")).to_contain_text("Gender: Female")
    expect(page.locator("body")).to_contain_text("Instagram: alice_j")
    expect(page.locator("body")).to_contain_text("Facebook: Not provided")
    expect(page.locator("body")).to_contain_text("Snapchat: Not provided")
    page.get_by_role("button", name="Edit").click()
    page.get_by_role("combobox").select_option("Male")
    page.get_by_role("textbox", name="Instagram username").click()
    page.get_by_role("textbox", name="Instagram username").fill("alice_james")
    page.get_by_role("textbox", name="Facebook profile link").click()
    page.get_by_role("textbox", name="Facebook profile link").fill("facebooktest.com")
    page.get_by_role("textbox", name="Snapchat username").click()
    page.get_by_role("textbox", name="Snapchat username").fill("alicetest")
    page.get_by_role("button", name="Update").click()
    expect(page.locator("#editForm")).to_contain_text(
        "Please enter a valid Facebook URL"
    )
    page.get_by_role("textbox", name="Facebook profile link").click()
    page.get_by_role("textbox", name="Facebook profile link").fill(
        "https://www.facebook.com/alice"
    )
    page.get_by_role("button", name="Update").click()
    expect(page.locator("body")).to_contain_text("Gender: Male")
    expect(page.locator("body")).to_contain_text("Instagram: alice_james")
    expect(page.locator("body")).to_contain_text(
        "Facebook: https://www.facebook.com/alice"
    )
    expect(page.locator("body")).to_contain_text("Snapchat: alicetest")

    reset_database()


def test_notificationMake(page: Page):
    page.goto("http://127.0.0.1:5000/")
    page.get_by_role("link", name="Sign Up").click()
    page.get_by_placeholder("Cameron", exact=True).click()
    page.get_by_placeholder("Cameron", exact=True).fill("Playwright")
    page.get_by_placeholder("Cameron", exact=True).press("Tab")
    page.get_by_placeholder("O'Niell").fill("Test")
    page.get_by_label("Gender (optional)").select_option("male")
    page.get_by_placeholder("cameron@example.com").click()
    page.get_by_placeholder("cameron@example.com").fill("playwright@example.com")
    page.get_by_placeholder("Uppercase, lowercase, number").click()
    page.get_by_placeholder("Uppercase, lowercase, number").fill("Password123!")
    page.get_by_placeholder("Instagram username").click()
    page.get_by_placeholder("Instagram username").fill("playwright")
    page.get_by_role("button", name="Sign Up").click()
    expect(page.get_by_role("alert")).to_contain_text("Account successfully created ×")
    page.get_by_role("link", name="Log In").click()
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("playwright@example.com")
    page.get_by_role("textbox", name="Email").press("Tab")
    page.get_by_role("textbox", name="Password").fill("Password123!")
    page.get_by_role("button", name="Log In").click()
    expect(page.get_by_role("alert")).to_contain_text("Successfully logged in ×")
    page.get_by_role("link", name="Browse Posts").click()
    page.locator(".d-flex > form > .btn").first.click()
    expect(page.get_by_role("alert")).to_contain_text("Connect request sent. ×")
    page.locator("div:nth-child(10) > div > .d-flex > form > .btn").click()
    expect(page.get_by_role("alert")).to_contain_text("Connect request sent. ×")
    page.get_by_role("link", name="Log Out").click()
    expect(page.get_by_role("alert")).to_contain_text("You have been logged out. ×")
    page.get_by_role("link", name="Log In").click()
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("alice@example.com")
    page.get_by_role("textbox", name="Email").press("Tab")
    page.get_by_role("textbox", name="Password").fill("password123")
    page.get_by_role("textbox", name="Password").press("Enter")
    page.get_by_role("heading", name="Responses").click()
    expect(page.get_by_role("link", name="Playwright Test")).to_be_visible()
    page.get_by_role("link", name="Log Out").click()
    expect(page.get_by_role("alert")).to_contain_text("You have been logged out. ×")
    page.get_by_role("link", name="Log In").click()
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("bob@example.com")
    page.get_by_role("textbox", name="Email").press("Tab")
    page.get_by_role("textbox", name="Password").fill("password123")
    page.get_by_role("textbox", name="Password").press("Enter")
    page.get_by_role("heading", name="Responses").click()
    expect(page.get_by_role("link", name="Playwright Test")).to_be_visible()

    reset_database()
