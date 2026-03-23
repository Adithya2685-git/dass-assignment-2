from .state import StreetRaceState


def _clean_text(value: str) -> str:
    return value.strip()


def add_car(state: StreetRaceState, car_id: str, model: str) -> dict:
    clean_car_id = _clean_text(car_id)
    clean_model = _clean_text(model)

    if not clean_car_id:
        raise ValueError("Car id cannot be empty.")
    if not clean_model:
        raise ValueError("Car model cannot be empty.")
    if clean_car_id in state.cars:
        raise ValueError(f"Car '{clean_car_id}' already exists.")

    car = {"car_id": clean_car_id, "model": clean_model, "damaged": False}
    state.cars[clean_car_id] = car
    return car


def get_car(state: StreetRaceState, car_id: str) -> dict | None:
    clean_car_id = _clean_text(car_id)
    return state.cars.get(clean_car_id)


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
    if state.cash_balance + amount < 0:
        raise ValueError("Cash balance cannot go below zero.")
    state.cash_balance += amount
    return state.cash_balance


def add_part(state: StreetRaceState, part_name: str, quantity: int) -> int:
    clean_part_name = _clean_text(part_name).lower()
    if not clean_part_name:
        raise ValueError("Part name cannot be empty.")
    if quantity == 0:
        raise ValueError("Part quantity cannot be zero.")

    current_quantity = state.parts.get(clean_part_name, 0)
    new_quantity = current_quantity + quantity
    if new_quantity < 0:
        raise ValueError(f"Not enough '{clean_part_name}' parts in inventory.")

    state.parts[clean_part_name] = new_quantity
    return state.parts[clean_part_name]
