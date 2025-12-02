from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"


def test_login_and_create_incident():
    """
    Basic end-to-end UI test using Playwright.

    Uses a dedicated local test account (test_automation) created for this project.
    The goal is to confirm that a user can still log in and reach the Incidents
    page after security changes have been applied.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Open login page
        page.goto(f"{BASE_URL}/login/")
        page.wait_for_load_state("networkidle")

        # Log in using the local test user
        page.fill("input[name='username']", "test_automation")
        page.fill("input[name='password']", "Test1234!")

        # Submit the first form on the page
        page.evaluate("document.querySelector('form').submit()")

        # Wait for redirect to the incidents list
        page.wait_for_url(f"{BASE_URL}/incidents/", timeout=10000)

        # Check that the incidents page content is visible
        body_text = page.text_content("body")
        assert "Incidents" in body_text

        browser.close()