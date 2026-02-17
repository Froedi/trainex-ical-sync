import os
from pathlib import Path
from playwright.sync_api import sync_playwright

USERNAME = os.getenv("TRAINEX_USER")
PASSWORD = os.getenv("TRAINEX_PASS")

LOGIN_URL = "https://trex.phwt.de/phwt-trainex//login.cfm"
ICAL_DOWNLOAD_LINK_TEXT = "iCal"  # der Text des Links auf der Seite

OUTPUT_FILE = Path("stundenplan.ics")

def download_ical():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        # Login
        page.goto(LOGIN_URL)
        page.wait_for_selector("#Login", timeout=60000)
        page.fill("#Login", USERNAME)
        page.fill("#Passwort", PASSWORD)
        page.click("#btnanm")
        page.wait_for_load_state("networkidle")

        # Download auslösen
        # Hier klicken wir den Link auf der Seite, nicht direkt goto
        with page.expect_download() as download_info:
            page.click(f"text={ICAL_DOWNLOAD_LINK_TEXT}")  

        download = download_info.value
        download.save_as(OUTPUT_FILE)

        browser.close()
        print(f"iCal erfolgreich gespeichert: {OUTPUT_FILE}")

if __name__ == "__main__":
    download_ical()
