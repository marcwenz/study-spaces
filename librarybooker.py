import requests
from auth import manc_session
from slotfinder import Slot, SlotFinder

url = "https://www.library.manchester.ac.uk/locations-and-opening-hours/study-spaces/booking/register/?"

url2 = "https://www.library.manchester.ac.uk/locations-and-opening-hours/study-spaces/booking/register/?event=HfIL3WT5"

headers = {
    "state": "do",
    "event": "VrQwSeb6",
    "firstname": "Marc",
    "surname": "Wenzlawski",
    "email": "marc.wenzlawski@student.manchester.ac.uk",
    "notes": "",
}

session = manc_session()

# slot_finder = SlotFinder(session)


res = session.post(url, headers=headers)

print(res.text)
