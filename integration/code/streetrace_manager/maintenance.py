from .crew_management import get_available_members
from .inventory import add_part, get_car, repair_car, update_cash
from .state import StreetRaceState


def schedule_repair(state: StreetRaceState, car_id: str) -> bool:
    if get_car(state, car_id) is None:
        return False
    return any(member["role"] == "mechanic" for member in get_available_members(state))


def repair_vehicle(state: StreetRaceState, car_id: str, part_name: str) -> bool:
    if not repair_car(state, car_id):
        return False
    add_part(state, part_name, -1)
    update_cash(state, -100)
    return True
