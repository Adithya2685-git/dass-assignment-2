from .registration import get_member, list_members
from .state import StreetRaceState


def assign_role(state: StreetRaceState, name: str, role: str) -> bool:
    member = get_member(state, name)
    if member is None:
        return False
    member["role"] = role
    return True


def update_skill(
    state: StreetRaceState, name: str, skill_name: str, level: int
) -> bool:
    member = get_member(state, name)
    if member is None:
        return False
    member["skills"][skill_name] = level
    return True


def get_available_members(state: StreetRaceState) -> list[dict]:
    return [member for member in list_members(state) if member["available"]]


def member_has_role(state: StreetRaceState, name: str, role: str) -> bool:
    member = get_member(state, name)
    if member is None:
        return False
    return member["role"] == role
