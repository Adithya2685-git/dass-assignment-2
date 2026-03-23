from .state import StreetRaceState


def add_reputation(state: StreetRaceState, amount: int) -> int:
    state.reputation += amount
    if state.reputation < 0:
        state.reputation = 0
    return get_reputation(state)


def get_reputation(state: StreetRaceState) -> int:
    return state.reputation
