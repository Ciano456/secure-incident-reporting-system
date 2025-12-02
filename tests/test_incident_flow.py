from playwright.sync_api import sync_playwright

# Base URL for the Django development server
BASE_URL = "http://127.0.0.1:8000"


def test_login_and_create_incident():
    """
    Basic end-to-end UI test using Playwright.

    This test does one simple but important thing:
    - It proves a real user can log in successfully
    - It confirms the user is redirected to the incidents page

    The goal here is not to test every feature, but to show that
    authentication and navigation still work correctly after security changes.
    """

    # Start Playwright and launch a browser instance
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Step 1: Open the login page
        page.goto(f"{BASE_URL}/login/")
        page.wait_for_load_state("networkidle")

        # Step 2: Enter valid login credentials
        # (These should be an existing test user account)
        page.fill("input[name='username']", "cianoconnor")
        page.fill("input[name='password']", "Today291125!!")

        # Step 3: Submit the form directly using JavaScript
        # This avoids any issues with locating buttons in different templates
        page.evaluate("document.querySelector('form').submit()")

        # Step 4: Confirm redirect to the incidents list
        # If login failed, this URL would never be reached
        page.wait_for_url(f"{BASE_URL}/incidents/", timeout=10000)

        # Step 5: Verify that the incidents page loaded successfully
        body_text = page.text_content("body")
        assert "Incidents" in body_text

        # Close the browser cleanly after test completion
        browser.close()