import os
from pathlib import Path
from playwright.sync_api import sync_playwright

# --- Umgebungsvariablen ---
USERNAME = os.getenv("TRAINEX_USER")
PASSWORD = os.getenv("TRAINEX_PASS")

# --- URLs ---
LOGIN_URL = "https://trex.phwt.de/phwt-trainex/"
NAV_URL = "https://trex.phwt.de/phwt-trainex/navigation/TraiNex"
FRAMES_URL = "https://trex.phwt.de/phwt-trainex/navigation/frameset.cfm?TokCF19=0T1328665717&IDphp17=3P665717&sec18m=7S286657171328665717&1771328665718&area=Kursraum"
STUNDENPLAN_URL = "https://trex.phwt.de/phwt-trainex/cfm/einsatzplan/einsatzplan_stundenplan.cfm?1771328707813&TokCF19=0T1328707811&IDphp17=3P707811&sec18m=7S287078111328707811&area=Kursraum&subarea=studienplan"
LISTENANSICHT_URL = "https://trex.phwt.de/phwt-trainex/cfm/einsatzplan/einsatzplan_listenansicht_kt.cfm?TokCF19=0T1328945370&IDphp17=3P945370&sec18m=7S289453701328945370&1771328945409&anf_dat=%7Bts%20%272026-02-16%2000:00:00%27%7D&kid_fremd=207&kid_sec_stud=19614078"

OUTPUT_FILE = Path("./trainex.studienplan.ics")

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

        # --- Navigation nach Stundenplan ---
        page.goto(NAV_URL)
        page.wait_for_load_state("networkidle")
        page.goto(FRAMES_URL)
        page.wait_for_load_state("networkidle")
        page.goto(STUNDENPLAN_URL)
        page.wait_for_load_state("networkidle")
        page.goto(LISTENANSICHT_URL)
        page.wait_for_load_state("networkidle")

        # --- Klick auf den iCal-Link, Download abfangen ---
        with page.expect_download() as download_info:
            page.click("text=iCal")  # Der Link auf der Listenansicht-Seite
        download = download_info.value
        download.save_as(str(OUTPUT_FILE))
        print(f"iCal erfolgreich gespeichert: {OUTPUT_FILE}")

        browser.close()


if __name__ == "__main__":
    download_ical()
