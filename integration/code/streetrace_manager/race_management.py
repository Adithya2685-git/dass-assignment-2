from .crew_management import member_has_role
from .inventory import get_car, mark_car_damaged
from .registration import get_member
from .results import record_result
from .state import StreetRaceState


def _clean_text(value: str) -> str:
    return value.strip()


def create_race(state: StreetRaceState, race_name: str, prize_money: int) -> dict:
    clean_race_name = _clean_text(race_name)
    if not clean_race_name:
        raise ValueError("Race name cannot be empty.")
    if prize_money < 0:
        raise ValueError("Prize money cannot be negative.")
    if clean_race_name in state.races:
        raise ValueError(f"Race '{clean_race_name}' already exists.")

    race = {
        "race_name": clean_race_name,
        "prize_money": prize_money,
        "entries": [],
        "finished": False,
    }
    state.races[clean_race_name] = race
    return race


def enter_race(
    state: StreetRaceState, race_name: str, driver_name: str, car_id: str
) -> bool:
    clean_race_name = _clean_text(race_name)
    clean_driver_name = _clean_text(driver_name)
    clean_car_id = _clean_text(car_id)

    if not validate_race_entry(state, driver_name, car_id):
        return False
    race = state.races.get(clean_race_name)
    if race is None:
        return False
    if race["finished"]:
        return False
    for entry in race["entries"]:
        if entry["driver_name"] == clean_driver_name:
            return False
        if entry["car_id"] == clean_car_id:
            return False
    race["entries"].append(
        {"driver_name": clean_driver_name, "car_id": clean_car_id}
    )
    return True


def validate_race_entry(
    state: StreetRaceState, driver_name: str, car_id: str
) -> bool:
    clean_driver_name = _clean_text(driver_name)
    clean_car_id = _clean_text(car_id)

    if not clean_driver_name or not clean_car_id:
        return False
    if get_member(state, clean_driver_name) is None:
        return False
    if not member_has_role(state, clean_driver_name, "driver"):
        return False
    car = get_car(state, clean_car_id)
    if car is None:
        return False
    return not car["damaged"]


def start_race(state: StreetRaceState, race_name: str, damage_car: bool = False) -> bool:
    clean_race_name = _clean_text(race_name)
    race = state.races.get(clean_race_name)
    if race is None or not race["entries"]:
        return False
    if race["finished"]:
        return False

    winner_entry = race["entries"][0]
    record_result(
        state,
        clean_race_name,
        winner_entry["driver_name"],
        race["prize_money"],
    )

    if damage_car:
        mark_car_damaged(state, winner_entry["car_id"])

    race["finished"] = True
    return True
