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


def test_find_winner_returns_richest_player():
    """Winner should be the player with the highest net worth."""
    game = Game(["A", "B"])
    rich = Player("Rich", balance=2000)
    poor = Player("Poor", balance=100)
    game.players = [rich, poor]

    winner = game.find_winner()

    assert winner == rich


def test_unmortgage_keeps_property_mortgaged_when_player_cannot_pay():
    """Failed unmortgage should not clear the mortgage state."""
    game = Game(["A", "B"])
    owner = Player("Owner", balance=10)
    prop = Property(("Lot", 1, 100, 10))
    prop.owner = owner
    owner.add_property(prop)
    prop.is_mortgaged = True

    result = game.unmortgage_property(owner, prop)

    assert result is False
    assert prop.is_mortgaged is True


def test_trade_transfers_cash_to_seller():
    """Trade payment should move cash from buyer to seller."""
    game = Game(["Seller", "Buyer"])
    seller = Player("Seller", balance=100)
    buyer = Player("Buyer", balance=200)
    prop = Property(("Trade Lot", 1, 50, 5))
    prop.owner = seller
    seller.add_property(prop)

    result = game.trade(seller, buyer, prop, 60)

    assert result is True
    assert seller.balance == 160
    assert buyer.balance == 140
    assert prop.owner == buyer
