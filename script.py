import os
from pathlib import Path
from playwright.sync_api import sync_playwright

USERNAME = os.getenv("TRAINEX_USER")
PASSWORD = os.getenv("TRAINEX_PASS")

# Login-URL und iCal-Seite
LOGIN_URL = "https://trex.phwt.de/phwt-trainex//login.cfm"
ICAL_PAGE_URL = "https://trex.phwt.de/phwt-trainex//cfm/einsatzplan/einsatzplan_listenansicht_iCal.cfm?TokCF19=0T1320846724&IDphp17=3P846724&sec18m=7S208467241320846724&1771320846877&utag=17&umonat=2&ujahr=2026&ics=1"

# Speicherort
OUTPUT_FILE = Path("stundenplan.ics")

def download_ical():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Login
        page.goto(LOGIN_URL)
        page.fill("input[name='username']", USERNAME)  # ggf. anpassen
        page.fill("input[name='password']", PASSWORD)  # ggf. anpassen
        page.click("input[type='submit']")
        page.wait_for_load_state("networkidle")

        # iCal-Download-Seite
        page.goto(ICAL_PAGE_URL)

        # Download der Datei
        with page.expect_download() as download_info:
            page.click("text=iCal")  # wenn nötig, ggf. anpassen

        download = download_info.value
        download.save_as(OUTPUT_FILE)

        browser.close()
        print(f"iCal erfolgreich gespeichert: {OUTPUT_FILE}")

if __name__ == "__main__":
    download_ical()
