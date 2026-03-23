from streetrace_manager.crew_management import assign_role
from streetrace_manager.inventory import (
    add_car,
    add_part,
    mark_car_damaged,
    update_cash,
)
from streetrace_manager.maintenance import repair_vehicle, schedule_repair
from streetrace_manager.mission_planning import create_mission, start_mission
from streetrace_manager.race_management import create_race, enter_race, start_race
from streetrace_manager.registration import register_member
from streetrace_manager.state import create_state


def test_registered_driver_can_enter_race():
    state = create_state()
    register_member(state, "Mia", "driver")
    add_car(state, "RX7", "Mazda RX-7")
    create_race(state, "Dock Sprint", 500)

    entered = enter_race(state, "Dock Sprint", "Mia", "RX7")

    assert entered is True
    assert state.races["Dock Sprint"]["entries"] == [
        {"driver_name": "Mia", "car_id": "RX7"}
    ]


def test_unregistered_driver_cannot_enter_race():
    state = create_state()
    add_car(state, "RX7", "Mazda RX-7")
    create_race(state, "Dock Sprint", 500)

    entered = enter_race(state, "Dock Sprint", "Ghost", "RX7")

    assert entered is False


def test_non_driver_role_cannot_enter_race():
    state = create_state()
    register_member(state, "Ken", "mechanic")
    add_car(state, "RX7", "Mazda RX-7")
    create_race(state, "Dock Sprint", 500)

    entered = enter_race(state, "Dock Sprint", "Ken", "RX7")

    assert entered is False


def test_damaged_car_cannot_enter_race():
    state = create_state()
    register_member(state, "Mia", "driver")
    add_car(state, "RX7", "Mazda RX-7")
    mark_car_damaged(state, "RX7")
    create_race(state, "Dock Sprint", 500)

    entered = enter_race(state, "Dock Sprint", "Mia", "RX7")

    assert entered is False


def test_finishing_race_updates_results_cash_rankings_and_reputation():
    state = create_state()
    register_member(state, "Mia", "driver")
    add_car(state, "RX7", "Mazda RX-7")
    create_race(state, "Dock Sprint", 500)
    enter_race(state, "Dock Sprint", "Mia", "RX7")

    started = start_race(state, "Dock Sprint")

    assert started is True
    assert state.races["Dock Sprint"]["finished"] is True
    assert state.cash_balance == 500
    assert state.rankings == {"Mia": 1}
    assert state.reputation == 5
    assert state.race_results == [
        {
            "race_name": "Dock Sprint",
            "driver_name": "Mia",
            "prize_money": 500,
            "ranking_points": 1,
        }
    ]


def test_start_mission_succeeds_when_required_roles_are_available():
    state = create_state()
    register_member(state, "Mia", "driver")
    register_member(state, "Ken", "mechanic")
    create_mission(state, "Night Delivery", ["driver", "mechanic"])

    started = start_mission(state, "Night Delivery", ["driver", "mechanic"])

    assert started is True
    assert state.missions["Night Delivery"]["started"] is True


def test_start_mission_fails_when_required_role_is_missing():
    state = create_state()
    register_member(state, "Mia", "driver")
    create_mission(state, "Night Delivery", ["driver", "mechanic"])

    started = start_mission(state, "Night Delivery", ["driver", "mechanic"])

    assert started is False
    assert state.missions["Night Delivery"]["started"] is False


def test_damaged_car_can_be_scheduled_and_repaired_when_mechanic_and_parts_exist():
    state = create_state()
    register_member(state, "Ken", "mechanic")
    add_car(state, "RX7", "Mazda RX-7")
    mark_car_damaged(state, "RX7")
    add_part(state, "tire", 2)
    update_cash(state, 500)

    scheduled = schedule_repair(state, "RX7")
    repaired = repair_vehicle(state, "RX7", "tire")

    assert scheduled is True
    assert repaired is True
    assert state.cars["RX7"]["damaged"] is False
    assert state.parts["tire"] == 1
    assert state.cash_balance == 400
    assert state.repairs == [{"car_id": "RX7", "status": "completed"}]


def test_repair_scheduling_fails_without_available_mechanic():
    state = create_state()
    register_member(state, "Mia", "driver")
    add_car(state, "RX7", "Mazda RX-7")
    mark_car_damaged(state, "RX7")

    scheduled = schedule_repair(state, "RX7")

    assert scheduled is False


def test_mission_with_car_requirement_fails_if_repair_cannot_be_scheduled():
    state = create_state()
    register_member(state, "Mia", "driver")
    register_member(state, "Ken", "mechanic")
    add_car(state, "RX7", "Mazda RX-7")
    create_mission(state, "Rescue Run", ["driver", "mechanic"])

    started = start_mission(state, "Rescue Run", ["driver", "mechanic"], "RX7")

    assert started is False
    assert state.missions["Rescue Run"]["started"] is False


def test_registered_member_role_can_be_changed_before_race_entry():
    state = create_state()
    register_member(state, "Mia", "mechanic")
    assign_role(state, "Mia", "driver")
    add_car(state, "RX7", "Mazda RX-7")
    create_race(state, "Dock Sprint", 500)

    entered = enter_race(state, "Dock Sprint", "Mia", "RX7")

    assert entered is True
