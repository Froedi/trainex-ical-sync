import os
import requests

# GitHub Secrets
USERNAME = os.getenv("TRAINEX_USER")
PASSWORD = os.getenv("TRAINEX_PASS")

# Direkte ICS URL
STUNDENPLAN_URL = "https://trex.phwt.de/phwt-trainex//cfm/einsatzplan/einsatzplan_listenansicht_iCal.cfm?TokCF19=0T1320846724&IDphp17=3P846724&sec18m=7S208467241320846724&1771320846877&utag=17&umonat=2&ujahr=2026&ics=1"

def download_ical():
    response = requests.get(STUNDENPLAN_URL, auth=(USERNAME, PASSWORD))
    response.raise_for_status()
    with open("stundenplan.ics", "wb") as f:
        f.write(response.content)
    print("iCal erfolgreich aktualisiert!")

if __name__ == "__main__":
    download_ical()
