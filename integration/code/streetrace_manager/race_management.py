from .crew_management import member_has_role
from .inventory import get_car, mark_car_damaged
from .registration import get_member
from .results import record_result
from .state import StreetRaceState


def create_race(state: StreetRaceState, race_name: str, prize_money: int) -> dict:
    race = {
        "race_name": race_name,
        "prize_money": prize_money,
        "entries": [],
        "finished": False,
    }
    state.races[race_name] = race
    return race


def enter_race(
    state: StreetRaceState, race_name: str, driver_name: str, car_id: str
) -> bool:
    if not validate_race_entry(state, driver_name, car_id):
        return False
    race = state.races.get(race_name)
    if race is None:
        return False
    race["entries"].append({"driver_name": driver_name, "car_id": car_id})
    return True


def validate_race_entry(
    state: StreetRaceState, driver_name: str, car_id: str
) -> bool:
    if get_member(state, driver_name) is None:
        return False
    if not member_has_role(state, driver_name, "driver"):
        return False
    car = get_car(state, car_id)
    if car is None:
        return False
    return not car["damaged"]


def start_race(state: StreetRaceState, race_name: str, damage_car: bool = False) -> bool:
    race = state.races.get(race_name)
    if race is None or not race["entries"]:
        return False

    winner_entry = race["entries"][0]
    record_result(
        state,
        race_name,
        winner_entry["driver_name"],
        race["prize_money"],
    )

    if damage_car:
        mark_car_damaged(state, winner_entry["car_id"])

    race["finished"] = True
    return True
