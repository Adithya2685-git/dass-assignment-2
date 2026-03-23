from .crew_management import get_available_members
from .inventory import add_part, get_car, repair_car, update_cash
from .state import StreetRaceState


def _clean_text(value: str) -> str:
    return value.strip()


def schedule_repair(state: StreetRaceState, car_id: str) -> bool:
    clean_car_id = _clean_text(car_id)
    car = get_car(state, clean_car_id)
    if car is None or not car["damaged"]:
        return False

    mechanic_available = any(
        member["role"] == "mechanic"
        for member in get_available_members(state)
    )
    if not mechanic_available:
        return False

    for repair in state.repairs:
        if repair["car_id"] == clean_car_id and repair["status"] == "scheduled":
            return True

    state.repairs.append({"car_id": clean_car_id, "status": "scheduled"})
    return True


def repair_vehicle(state: StreetRaceState, car_id: str, part_name: str) -> bool:
    clean_car_id = _clean_text(car_id)
    clean_part_name = _clean_text(part_name)

    car = get_car(state, clean_car_id)
    if car is None or not car["damaged"]:
        return False

    if not any(member["role"] == "mechanic" for member in get_available_members(state)):
        return False

    add_part(state, clean_part_name, -1)
    update_cash(state, -100)
    if not repair_car(state, clean_car_id):
        return False

    for repair in state.repairs:
        if repair["car_id"] == clean_car_id and repair["status"] == "scheduled":
            repair["status"] = "completed"
            break
    else:
        state.repairs.append({"car_id": clean_car_id, "status": "completed"})

    return True
