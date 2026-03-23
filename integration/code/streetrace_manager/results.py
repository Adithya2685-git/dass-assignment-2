from .inventory import update_cash
from .reputation import add_reputation
from .state import StreetRaceState


def _clean_text(value: str) -> str:
    return value.strip()


def record_result(
    state: StreetRaceState, race_name: str, driver_name: str, prize_money: int
) -> dict:
    clean_race_name = _clean_text(race_name)
    clean_driver_name = _clean_text(driver_name)

    if not clean_race_name:
        raise ValueError("Race name cannot be empty.")
    if not clean_driver_name:
        raise ValueError("Driver name cannot be empty.")
    if prize_money < 0:
        raise ValueError("Prize money cannot be negative.")

    new_points = update_rankings(state, clean_driver_name)
    award_prize_money(state, prize_money)
    result = {
        "race_name": clean_race_name,
        "driver_name": clean_driver_name,
        "prize_money": prize_money,
        "ranking_points": new_points,
    }
    state.race_results.append(result)
    return result


def update_rankings(state: StreetRaceState, driver_name: str) -> int:
    clean_driver_name = _clean_text(driver_name)
    current_points = state.rankings.get(clean_driver_name, 0) + 1
    state.rankings[clean_driver_name] = current_points
    add_reputation(state, 5)
    return current_points


def award_prize_money(state: StreetRaceState, prize_money: int) -> int:
    if prize_money < 0:
        raise ValueError("Prize money cannot be negative.")
    return update_cash(state, prize_money)


def get_rankings(state: StreetRaceState) -> dict[str, int]:
    return dict(sorted(state.rankings.items(), key=lambda item: item[1], reverse=True))
