from slot import *
from lxml import Element


class Location:
    def __init__(self, name: str, slots: list(Slot) = []) -> None:
        self.name = name
        self.slots = slots

    def __str__(self) -> str:
        return (
            "Location: "
            + self.name
            + "\n"
            + "Slots:"
            + "\n\t"
            + "\n\t".join([str(slot) for slot in self.slots])
        )

    @staticmethod
    def parse_location(el: Element):
        table = el.find("table").find("tbody").findall("tr")
        l = Location(el.find("h3").text)
        slots = [Slot.parse_slot(t, l) for t in table]

    def slot_by_time(self, day: int, time: int):
        for slot in self.slots:
            if slot.day == day and slot.time == time:
                return slot
        return -1

    def slot_by_index(self, index: int):
        return self.slots[index]
