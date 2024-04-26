import re
from playwright.sync_api import Page, expect


def test_browse(page: Page):
    page.goto('http://127.0.0.1:5000/');
    page.get_by_text('Browse Letters Description').click();
    expect(page.get_by_text('Alice\'s Post #1 by Alice')).to_be_visible();
    expect(page.get_by_text('Alice\'s Post #2 by Alice')).to_be_visible();
    expect(page.get_by_text('Alice\'s Post #3 by Alice')).to_be_visible();
    expect(page.get_by_text('Bob\'s Post #1 by Anonymous')).to_be_visible();
    expect(page.get_by_text('Bob\'s Post #2 by Bob Smith')).to_be_visible();
    expect(page.get_by_text('Bob\'s Post #3 by Bob Smith')).to_be_visible();
    expect(page.get_by_text('Carol\'s Post #1 by Carol')).to_be_visible();
    expect(page.get_by_text('Carol\'s Post #2 by Anonymous')).to_be_visible();
    expect(page.get_by_text('Carol\'s Post #3 by Carol')).to_be_visible();
    page.get_by_role('link', name='Love Letters').click();

