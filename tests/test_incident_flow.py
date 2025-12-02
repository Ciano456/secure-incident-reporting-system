"""
Student Name: Cian O'Connor
Student Number: 22109668
Student Email: x22109668@student.ncirl.ie
Project: Secure Incident Reporting System

File Purpose:
This file contains an automated end-to-end UI test written using Playwright.
The test simulates a real user logging into the system and verifies that the
incident list page loads successfully after authentication.

A dedicated test user account was created for this purpose so that credentials
do not depend on personal user accounts. In a real production system, credentials
would never be hardcoded and would instead be stored securely using environment
variables or secret stores.
"""

from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"


def test_login_and_create_incident():
    """
    End-to-end UI test using Playwright.

    This test checks:
    1. Whether the login page loads correctly
    2. Whether a test user can log in
    3. Whether the incidents page is displayed after login

    The goal is to confirm that authentication and page routing works correctly.
    """

    with sync_playwright() as p:
        # Launch a lightweight browser instance
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Open the login page
        page.goto(f"{BASE_URL}/login/")
        page.wait_for_load_state("networkidle")

        # Log in using the dedicated test account
        page.fill("input[name='username']", "test_automation")
        page.fill("input[name='password']", "Test1234!")

        # Submit the login form manually using JavaScript
        page.evaluate("document.querySelector('form').submit()")

        # Wait for redirect to the incidents list
        page.wait_for_url(f"{BASE_URL}/incidents/", timeout=10000)

        # Confirm the page content is visible
        body_text = page.text_content("body")
        assert "Incidents" in body_text

        # Close the browser
        browser.close()