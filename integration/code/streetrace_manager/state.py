from dataclasses import dataclass, field


@dataclass
class StreetRaceState:
    members: dict[str, dict] = field(default_factory=dict)
    cars: dict[str, dict] = field(default_factory=dict)
    parts: dict[str, int] = field(default_factory=dict)
    tools: dict[str, int] = field(default_factory=dict)
    cash_balance: int = 0
    races: dict[str, dict] = field(default_factory=dict)
    missions: dict[str, dict] = field(default_factory=dict)
    rankings: dict[str, int] = field(default_factory=dict)
    repairs: list[dict] = field(default_factory=list)
    reputation: int = 0


def create_state() -> StreetRaceState:
    return StreetRaceState()
