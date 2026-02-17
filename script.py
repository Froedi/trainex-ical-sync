import os
from playwright.sync_api import sync_playwright

USERNAME = os.getenv("TRAINEX_USER")
PASSWORD = os.getenv("TRAINEX_PASS")

LOGIN_URL = "https://trex.phwt.de/phwt-trainex//login.cfm"
STUNDENPLAN_URL = "HIER_STUNDENPLAN_URL_EINFÜGEN"

def download_ical():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Login
        page.goto(LOGIN_URL)
        page.fill("input[name='username']", USERNAME)  # ggf. anpassen
        page.fill("input[name='password']", PASSWORD)  # ggf. anpassen
        page.click("input[type='submit']")  # ggf. anpassen
        page.wait_for_load_state("networkidle")

        # Stundenplan-Seite
        page.goto(STUNDENPLAN_URL)

        # iCal Download
        with page.expect_download() as download_info:
            page.click("text=iCal")  # ggf. anpassen

        download = download_info.value
        download.save_as("stundenplan.ics")

        browser.close()

if __name__ == "__main__":
    download_ical()
