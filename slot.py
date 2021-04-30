from location import Location
from lxml import Element


class Slot:
    def __init__(
        self,
        day: int,
        time: int,
        event_id: str,
        time_string: str,
        is_full: bool,
        location: Location,
    ) -> None:
        self.day = day
        self.time = time
        self.event_id = event_id
        self.time_string = time_string
        self.is_full = is_full
        self.location = location

    def __str__(self) -> str:
        return (
            self.time_string
            + ", event id "
            + self.event_id
            + ", Slot "
            + ("is" if self.is_full else "isn't")
            + " full."
        )

    @staticmethod
    def parse_slot(el: Element, l: Location):
        # print(etree.tostring(el))
        items = el.findall("td")
        time, time_string, day = Time.parse_time(items[0])
        event_id = Slot.parse_event_id(items[-1])
        is_full = Slot.parse_is_full(items[2])
        return Slot(day, time, event_id, time_string, is_full, l)

    @staticmethod
    def parse_event_id(event: Element) -> str:
        id = event.find("a").get("href")[-8:]
        return id

    @staticmethod
    def parse_is_full(event: Element) -> bool:
        full = event.find("img").get("alt")
        if full == "Full":
            return True
        elif full == "Spaces":
            return False
        else:
            raise ValueError("Not a vaild full indicatior")


class Time:
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3

    @staticmethod
    def parse_time(time: Element) -> tuple:
        day, hours = time.text.split(", ")
        return (Time.parse_hours(hours), time.text, Time.parse_day(day))

    @staticmethod
    def parse_day(day: str) -> int:
        if day == "Today":
            return Day.TODAY
        elif day == "Tomorrow":
            return Day.TOMORROW
        else:
            raise ValueError("Not a valid day")

    @staticmethod
    def parse_hours(hours: str) -> int:
        if hours[0] == "0":
            return Time.MORNING
        elif hours[0] == "1":
            hours = hours.split()
            if hours[2][0] == "1":
                return Time.AFTERNOON
            elif hours[2][0] == "2":
                return Time.EVENING
            else:
                raise ValueError("Not a valid time")
        else:
            raise ValueError("Not a valid time")


class Day:
    TODAY = 1
    TOMORROW = 2