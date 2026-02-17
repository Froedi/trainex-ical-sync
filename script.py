import os
from pathlib import Path
from playwright.sync_api import sync_playwright

USERNAME = os.getenv("TRAINEX_USER")
PASSWORD = os.getenv("TRAINEX_PASS")

LOGIN_URL = "https://trex.phwt.de/phwt-trainex/"
ICAL_PAGE_URL = (
    "https://trex.phwt.de/phwt-trainex/cfm/einsatzplan/einsatzplan_listenansicht_iCal.cfm?"
    "TokCF19=0T1328959301&IDphp17=3P959301&sec18m=7S289593011328959301&"
    "1771328959448&utag=17&umonat=2&ujahr=2026&ics=1"
)

OUTPUT_FILE = Path("./trainex.studienplan.ics")

def download_ical():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)  # wichtig für Downloads
        page = context.new_page()

        # --- Login ---
        page.goto(LOGIN_URL)
        page.wait_for_selector("#Login", timeout=60000)
        page.fill("#Login", USERNAME)
        page.fill("#Passwort", PASSWORD)
        page.click("#btnanm")
        page.wait_for_load_state("networkidle")

        # --- iCal-Seite aufrufen und Download starten ---
        page.goto(ICAL_PAGE_URL)

        # --- Download abfangen ---
        with page.expect_download() as download_info:
            # Klick auf den iCal-Link, falls nötig. Bei Direktlink funktioniert manchmal goto
            # page.click("text=iCal")  # nur nötig, wenn die Datei nicht automatisch startet
            pass  # Bei Direktlink startet der Download sofort
        download = download_info.value
        download.save_as(str(OUTPUT_FILE))

        print(f"iCal erfolgreich gespeichert: {OUTPUT_FILE}")

        browser.close()

if __name__ == "__main__":
    download_ical()
