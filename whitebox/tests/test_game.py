"""Game tests."""

from moneypoly.game import Game
from moneypoly.player import Player
from moneypoly.property import Property


def test_buy_property_allows_purchase_when_balance_equals_price():
    """Exact balance should still allow a purchase."""
    game = Game(["A", "B"])
    player = Player("Buyer", balance=100)
    prop = Property(("Lot", 1, 100, 10))

    result = game.buy_property(player, prop)

    assert result is True
    assert player.balance == 0
    assert prop.owner == player
