from .inventory import update_cash
from .reputation import add_reputation
from .state import StreetRaceState


def record_result(
    state: StreetRaceState, race_name: str, driver_name: str, prize_money: int
) -> dict:
    update_rankings(state, driver_name)
    award_prize_money(state, prize_money)
    return {
        "race_name": race_name,
        "driver_name": driver_name,
        "prize_money": prize_money,
    }


def update_rankings(state: StreetRaceState, driver_name: str) -> int:
    current_points = state.rankings.get(driver_name, 0) + 1
    state.rankings[driver_name] = current_points
    add_reputation(state, 5)
    return current_points


def award_prize_money(state: StreetRaceState, prize_money: int) -> int:
    return update_cash(state, prize_money)


def get_rankings(state: StreetRaceState) -> dict[str, int]:
    return dict(state.rankings)
