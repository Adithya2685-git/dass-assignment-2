"""White-box tests for player movement behavior."""

from moneypoly.config import GO_SALARY, STARTING_BALANCE
from moneypoly.player import Player
from moneypoly.property import Property


def test_move_awards_salary_when_passing_go():
    """Passing Go should increase balance even when the player does not land on 0."""
    player = Player("A")
    player.position = 39

    new_position = player.move(2)

    assert new_position == 1
    assert player.balance == STARTING_BALANCE + GO_SALARY


def test_net_worth_includes_owned_property_value():
    """Owned property value should count toward net worth."""
    player = Player("Owner", balance=200)
    prop = Property(("Lot", 1, 100, 10))
    prop.owner = player
    player.add_property(prop)

    assert player.net_worth() == 300
