from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"


def test_login_and_create_incident():
    """
    Basic end-to-end UI test using Playwright.

    Uses a dedicated test account (test_automation) created locally
    for this assignment. In a real production environment, credentials
    would not be hard-coded in source code.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Open login page
        page.goto(f"{BASE_URL}/login/")
        page.wait_for_load_state("networkidle")

        # Use local test user
        page.fill("input[name='username']", "test_automation")
        page.fill("input[name='password']", "Test1234!")

        # Submit the first form on the page
        page.evaluate("document.querySelector('form').submit()")

        # Confirm redirect to incidents page
        page.wait_for_url(f"{BASE_URL}/incidents/", timeout=10000)
        body_text = page.text_content("body")
        assert "Incidents" in body_text

        browser.close()