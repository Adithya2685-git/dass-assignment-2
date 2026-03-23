from .registration import get_member, list_members
from .state import StreetRaceState


def _clean_text(value: str) -> str:
    return value.strip()


def assign_role(state: StreetRaceState, name: str, role: str) -> bool:
    member = get_member(state, name)
    if member is None:
        return False
    clean_role = _clean_text(role).lower()
    if not clean_role:
        return False
    member["role"] = clean_role
    return True


def update_skill(
    state: StreetRaceState, name: str, skill_name: str, level: int
) -> bool:
    member = get_member(state, name)
    if member is None:
        return False
    clean_skill = _clean_text(skill_name).lower()
    if not clean_skill:
        return False
    if level < 0:
        return False
    member["skills"][clean_skill] = level
    return True


def get_available_members(state: StreetRaceState) -> list[dict]:
    available_members = [
        member for member in list_members(state)
        if member["available"]
    ]
    return available_members


def member_has_role(state: StreetRaceState, name: str, role: str) -> bool:
    member = get_member(state, name)
    if member is None:
        return False
    clean_role = _clean_text(role).lower()
    return member["role"] == clean_role
