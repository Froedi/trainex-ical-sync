import os
from pathlib import Path
import asyncio
from playwright.async_api import async_playwright

USERNAME = os.getenv("TRAINEX_USER")
PASSWORD = os.getenv("TRAINEX_PASS")

LOGIN_URL = "https://trex.phwt.de/phwt-trainex/"
ICAL_PAGE_URL = "https://trex.phwt.de/phwt-trainex/cfm/einsatzplan/einsatzplan_listenansicht_iCal.cfm?TokCF19=0T1328959301&IDphp17=3P959301&sec18m=7S289593011328959301&1771328959448&utag=17&umonat=2&ujahr=2026&ics=1"

OUTPUT_FILE = Path("./trainex.studienplan.ics")

async def download_ical():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        # Login
        await page.goto(LOGIN_URL)
        await page.fill("#Login", USERNAME)
        await page.fill("#Passwort", PASSWORD)
        await page.click("#btnanm")
        await page.wait_for_load_state("networkidle")

        # Direktlink im Browser klicken
        html = f'<a id="ical_link" href="{ICAL_PAGE_URL}">Download iCal</a>'
        await page.set_content(html)

        # Download abfangen
        async with page.expect_download() as download_info:
            await page.click("#ical_link")
        download = await download_info.value
        await download.save_as(str(OUTPUT_FILE))

        print(f"iCal erfolgreich gespeichert: {OUTPUT_FILE}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(download_ical())
