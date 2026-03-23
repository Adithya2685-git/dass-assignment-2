from .state import StreetRaceState


def register_member(state: StreetRaceState, name: str, role: str) -> dict:
    member = {
        "name": name,
        "role": role,
        "skills": {},
        "available": True,
    }
    state.members[name] = member
    return member


def get_member(state: StreetRaceState, name: str) -> dict | None:
    return state.members.get(name)


def list_members(state: StreetRaceState) -> list[dict]:
    return list(state.members.values())
