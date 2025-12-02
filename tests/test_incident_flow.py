"""
Student Name: Cian O'Connor
Student Number: 22109668
Student Email: x22109668@student.ncirl.ie
Project: Secure Incident Reporting System
Branch: INSECURE

Description:
This Playwright test performs a basic end-to-end check of the web application.

It verifies that:
- A user can access the login page
- A user can log in using a valid account
- The system redirects to the incident list after login

This test is intentionally minimal and focuses on verifying workflow
rather than security, as the insecure branch is designed to highlight
vulnerabilities rather than prevent them.
"""

from playwright.sync_api import sync_playwright

# Base URL where the Django development server runs locally
BASE_URL = "http://127.0.0.1:8000"


def test_login_and_create_incident():
    """
    Basic automated UI test.

    This test does NOT create an incident.
    It simply verifies that the login flow works correctly
    and that the incident list page loads after authentication.
    """

    with sync_playwright() as p:
        # Launch Chromium browser 
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Step 1: Open the login page
        page.goto(f"{BASE_URL}/login/")
        page.wait_for_load_state("networkidle")

        # Step 2: Log in using the dedicated test account
        # This user is created purely for automated testing purposes.
        page.fill("input[name='username']", "test_automation")
        page.fill("input[name='password']", "Test1234!")

        # Submit the login form directly using JavaScript
        page.evaluate("document.querySelector('form').submit()")

        # Step 3: Confirm successful redirect to the incidents page
        page.wait_for_url(f"{BASE_URL}/incidents/", timeout=10000)

        # Step 4: Confirm key page text appears
        body_text = page.text_content("body")
        assert "Incidents" in body_text

        # Close browser after test completes
        browser.close()