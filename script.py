import os
from pathlib import Path
from playwright.sync_api import sync_playwright

USERNAME = os.getenv("TRAINEX_USER")
PASSWORD = os.getenv("TRAINEX_PASS")

# Links für die Navigation
LOGIN_URL = "https://trex.phwt.de/phwt-trainex/"
TRAINEX_HOME = "https://trex.phwt.de/phwt-trainex/navigation/TraiNex"
FRAMESET_URL = "https://trex.phwt.de/phwt-trainex/navigation/frameset.cfm?TokCF19=0T1328665717&IDphp17=3P665717&sec18m=7S286657171328665717&1771328665718&area=Kursraum"
STUNDENPLAN_URL = "https://trex.phwt.de/phwt-trainex/cfm/einsatzplan/einsatzplan_stundenplan.cfm?1771328707813&TokCF19=0T1328707811&IDphp17=3P707811&sec18m=7S287078111328707811&area=Kursraum&subarea=studienplan"
LISTENANSICHT_URL = "https://trex.phwt.de/phwt-trainex/cfm/einsatzplan/einsatzplan_listenansicht_kt.cfm?TokCF19=0T1328945370&IDphp17=3P945370&sec18m=7S289453701328945370&1771328945409&anf_dat=%7Bts%20%272026%2D02%2D16%2000%3A00%3A00%27%7D&kid_fremd=207&kid_sec_stud=19614078"

OUTPUT_FILE = Path("stundenplan.ics")

def download_ical():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        # --- LOGIN ---
        page.goto(LOGIN_URL)
        page.wait_for_selector("#Login", timeout=60000)
        page.fill("#Login", USERNAME)
        page.fill("#Passwort", PASSWORD)
        page.click("#btnanm")
        page.wait_for_load_state("networkidle")

        # --- Navigation durch die Seiten ---
        page.goto(TRAINEX_HOME)
        page.goto(FRAMESET_URL)
        page.goto(STUNDENPLAN_URL)
        page.goto(LISTENANSICHT_URL)
        page.wait_for_load_state("networkidle")

        # --- Download iCal ---
        # Wir gehen davon aus, dass der iCal-Link sichtbar ist
        with page.expect_download() as download_info:
            # Klick auf den iCal-Link, evtl. Text anpassen falls anders
            page.click("text=iCal")

        download = download_info.value
        download.save_as(OUTPUT_FILE)

        browser.close()
        print(f"iCal erfolgreich gespeichert: {OUTPUT_FILE}")

if __name__ == "__main__":
    download_ical()
