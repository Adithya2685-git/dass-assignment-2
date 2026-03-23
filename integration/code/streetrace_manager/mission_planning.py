from .crew_management import get_available_members
from .maintenance import schedule_repair
from .state import StreetRaceState


def create_mission(
    state: StreetRaceState, mission_name: str, required_roles: list[str]
) -> dict:
    mission = {
        "mission_name": mission_name,
        "required_roles": required_roles,
        "started": False,
    }
    state.missions[mission_name] = mission
    validate_mission_roles(state, required_roles)
    return mission


def validate_mission_roles(state: StreetRaceState, required_roles: list[str]) -> bool:
    available_roles = {
        member["role"] for member in get_available_members(state)
    }
    return all(role in available_roles for role in required_roles)


def start_mission(
    state: StreetRaceState,
    mission_name: str,
    required_roles: list[str],
    car_id: str | None = None,
) -> bool:
    mission = state.missions.get(mission_name)
    if mission is None:
        return False
    if not validate_mission_roles(state, required_roles):
        return False
    if car_id is not None:
        schedule_repair(state, car_id)
    mission["started"] = True
    return True
