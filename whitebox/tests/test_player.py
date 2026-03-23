"""White-box tests for player movement behavior."""

from moneypoly.config import GO_SALARY, STARTING_BALANCE
from moneypoly.player import Player


def test_move_awards_salary_when_passing_go():
    """Passing Go should increase balance even when the player does not land on 0."""
    player = Player("A")
    player.position = 39

    new_position = player.move(2)

    assert new_position == 1
    assert player.balance == STARTING_BALANCE + GO_SALARY
