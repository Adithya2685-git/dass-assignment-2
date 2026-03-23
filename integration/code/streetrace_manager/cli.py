from .state import create_state


def main() -> None:
    state = create_state()
    print("StreetRace Manager")
    print(f"Members: {len(state.members)}")
    print(f"Cars: {len(state.cars)}")
