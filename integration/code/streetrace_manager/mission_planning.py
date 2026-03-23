from .crew_management import get_available_members
from .inventory import get_car
from .maintenance import schedule_repair
from .state import StreetRaceState


def _clean_text(value: str) -> str:
    return value.strip()


def _normalize_roles(required_roles: list[str]) -> list[str]:
    roles = []
    for role in required_roles:
        clean_role = _clean_text(role).lower()
        if clean_role and clean_role not in roles:
            roles.append(clean_role)
    return roles


def create_mission(
    state: StreetRaceState, mission_name: str, required_roles: list[str]
) -> dict:
    clean_mission_name = _clean_text(mission_name)
    normalized_roles = _normalize_roles(required_roles)

    if not clean_mission_name:
        raise ValueError("Mission name cannot be empty.")
    if not normalized_roles:
        raise ValueError("Mission must require at least one role.")
    if clean_mission_name in state.missions:
        raise ValueError(f"Mission '{clean_mission_name}' already exists.")

    mission = {
        "mission_name": clean_mission_name,
        "required_roles": normalized_roles,
        "started": False,
        "completed": False,
    }
    state.missions[clean_mission_name] = mission
    return mission


def validate_mission_roles(state: StreetRaceState, required_roles: list[str]) -> bool:
    normalized_roles = _normalize_roles(required_roles)
    if not normalized_roles:
        return False
    available_roles = {
        member["role"] for member in get_available_members(state)
    }
    return all(role in available_roles for role in normalized_roles)


def start_mission(
    state: StreetRaceState,
    mission_name: str,
    required_roles: list[str],
    car_id: str | None = None,
) -> bool:
    clean_mission_name = _clean_text(mission_name)
    mission = state.missions.get(clean_mission_name)
    if mission is None:
        return False
    if mission["started"]:
        return False

    normalized_roles = _normalize_roles(required_roles)
    if normalized_roles and normalized_roles != mission["required_roles"]:
        return False
    if not validate_mission_roles(state, mission["required_roles"]):
        return False

    if car_id is not None:
        car = get_car(state, car_id)
        if car is None:
            return False
        if car["damaged"] and not schedule_repair(state, car_id):
            return False

    mission["started"] = True
    return True
