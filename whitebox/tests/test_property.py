"""White-box tests for property and property-group behavior."""

from moneypoly.player import Player
from moneypoly.property import Property, PropertyGroup


def test_full_group_bonus_requires_all_properties_same_owner():
    """Rent should not double unless one owner holds the entire group."""
    group = PropertyGroup("Brown", "brown")
    owner = Player("Owner")
    other = Player("Other")
    first = Property(("First", 1, 60, 2), group)
    second = Property(("Second", 3, 60, 4), group)
    first.owner = owner
    second.owner = other

    assert group.all_owned_by(owner) is False
    assert first.get_rent() == 2
