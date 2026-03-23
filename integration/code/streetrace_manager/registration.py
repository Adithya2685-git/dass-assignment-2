from .state import StreetRaceState


def _clean_value(value: str) -> str:
    return value.strip()


def register_member(state: StreetRaceState, name: str, role: str) -> dict:
    clean_name = _clean_value(name)
    clean_role = _clean_value(role).lower()

    if not clean_name:
        raise ValueError("Member name cannot be empty.")
    if not clean_role:
        raise ValueError("Member role cannot be empty.")
    if clean_name in state.members:
        raise ValueError(f"Member '{clean_name}' is already registered.")

    member = {
        "name": clean_name,
        "role": clean_role,
        "skills": {},
        "available": True,
    }
    state.members[clean_name] = member
    return member


def get_member(state: StreetRaceState, name: str) -> dict | None:
    clean_name = _clean_value(name)
    return state.members.get(clean_name)


def list_members(state: StreetRaceState) -> list[dict]:
    return [
        state.members[name]
        for name in sorted(state.members)
    ]
