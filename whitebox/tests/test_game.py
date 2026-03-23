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


def test_pay_rent_transfers_money_to_property_owner():
    """Rent should go to the owner."""
    game = Game(["Tenant", "Owner"])
    tenant = Player("Tenant", balance=200)
    owner = Player("Owner", balance=300)
    prop = Property(("Rent Lot", 1, 100, 25))
    prop.owner = owner

    game.pay_rent(tenant, prop)

    assert tenant.balance == 175
    assert owner.balance == 325


def test_paying_jail_fine_deducts_money_from_player(monkeypatch):
    """Choosing to pay the jail fine should reduce the player's balance."""
    game = Game(["A", "B"])
    player = Player("Jailed", balance=150)
    player.in_jail = True

    monkeypatch.setattr("moneypoly.ui.confirm", lambda prompt: True)
    monkeypatch.setattr(game.dice, "roll", lambda: 4)
    monkeypatch.setattr(game.dice, "describe", lambda: "2 + 2 = 4")
    monkeypatch.setattr(game, "_move_and_resolve", lambda current, roll: None)

    game._handle_jail_turn(player)

    assert player.balance == 100
