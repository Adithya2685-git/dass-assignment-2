from .state import StreetRaceState


def add_car(state: StreetRaceState, car_id: str, model: str) -> dict:
    car = {"car_id": car_id, "model": model, "damaged": False}
    state.cars[car_id] = car
    return car


def get_car(state: StreetRaceState, car_id: str) -> dict | None:
    return state.cars.get(car_id)


def mark_car_damaged(state: StreetRaceState, car_id: str) -> bool:
    car = get_car(state, car_id)
    if car is None:
        return False
    car["damaged"] = True
    return True


def repair_car(state: StreetRaceState, car_id: str) -> bool:
    car = get_car(state, car_id)
    if car is None:
        return False
    car["damaged"] = False
    return True


def update_cash(state: StreetRaceState, amount: int) -> int:
    state.cash_balance += amount
    return state.cash_balance


def add_part(state: StreetRaceState, part_name: str, quantity: int) -> int:
    current_quantity = state.parts.get(part_name, 0)
    state.parts[part_name] = current_quantity + quantity
    return state.parts[part_name]
