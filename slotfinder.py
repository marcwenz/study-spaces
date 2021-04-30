from requests.sessions import Session
from auth import manc_session
from lxml import etree
from slot import *
from location import *


class SlotFinder:
    url = "https://www.library.manchester.ac.uk/locations-and-opening-hours/study-spaces/booking/"

    def __init__(self, session: Session) -> None:
        self.study_page = etree.HTML(session.get(self.url).text)
        self.session = session
        el = self.study_page.xpath("//div[@class='event']")
        self.locations = [Location.parse_location(e) for e in el]

    def location_by_name(self, name: str) -> Location:
        for location in self.locations:
            if location.name == name:
                return location
        return -1

    def location_by_index(self, index: int) -> Location:
        return self.locations[index]

    def book_all_location(self, location: Location) -> list(int):
        for slot in location.slots:
            pass

    def free_slots(self) -> list(Slot):
        free = []
        for location in self.loctations:
            for slot in location.slots:
                if not slot.is_full:
                    free.append(slot)

        return free

    def book_slot(self, slot: Slot) -> bool:
        if slot.is_full:
            return
        url2 = self.url + "register/?event=" + slot.event_id
        res = self.session.get(url2)
        h = etree.HTML(res.text)
        try:
            first = h.xpath("//input[@id='firstname']")[0].get("value")
            sur = h.xpath("//input[@id='surname']")[0].get("value")
            email = h.xpath("//input[@id='email']")[0].get("value")
        except IndexError:
            already_registered = (
                etree.tostring(h)
                .decode("utf-8")
                .find("You are already signed up for this event.")
            )
            if already_registered:
                return
            else:
                raise ValueError("Unknown error")

        url2 = self.url + "register/?"

        payload = {
            "state": "do",
            "event": slot.event_id,
            "firstname": first,
            "surname": sur,
            "email": email,
            "notes": "",
        }

        res = self.session.post(url2, data=payload)

        print(res.text)


if __name__ == "__main__":
    session = manc_session()
    s = SlotFinder(session)

    s.book_slot(s.location_by_index(3).slot_by_index(-1))