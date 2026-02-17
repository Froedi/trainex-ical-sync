import os
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright

USERNAME = os.getenv("TRAINEX_USER")
PASSWORD = os.getenv("TRAINEX_PASS")

LOGIN_URL = "https://trex.phwt.de/phwt-trainex/"
ICAL_URL = "https://trex.phwt.de/phwt-trainex/cfm/einsatzplan/einsatzplan_listenansicht_iCal.cfm?TokCF19=0T1328959301&IDphp17=3P959301&sec18m=7S289593011328959301&1771328959448&utag=17&umonat=2&ujahr=2026&ics=1"

OUTPUT_FILE = Path("trainex.studienplan.ics")

def download_ical():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # --- Login ---
        page.goto(LOGIN_URL)
        page.wait_for_selector("#Login", timeout=60000)
        page.fill("#Login", USERNAME)
        page.fill("#Passwort", PASSWORD)
        page.click("#btnanm")
        page.wait_for_load_state("networkidle")

        # --- Session-Cookies auslesen ---
        cookies = context.cookies()
        session_cookies = {cookie['name']: cookie['value'] for cookie in cookies}

        browser.close()

    # --- Download der iCal-Datei mit requests ---
    response = requests.get(ICAL_URL, cookies=session_cookies)
    response.raise_for_status()  # Fehler falls Download fehlschlägt
    OUTPUT_FILE.write_bytes(response.content)
    print(f"iCal erfolgreich gespeichert: {OUTPUT_FILE}")

if __name__ == "__main__":
    download_ical()
