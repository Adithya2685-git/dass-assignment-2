"""White-box tests for bank behavior."""

from moneypoly.bank import Bank
from moneypoly.player import Player


def test_give_loan_reduces_bank_funds():
    """Emergency loans should come out of the bank's balance."""
    bank = Bank()
    player = Player("Borrower")
    opening_balance = bank.get_balance()

    paid = bank.give_loan(player, 300)

    assert paid == 300
    assert player.balance == 1800
    assert bank.get_balance() == opening_balance - 300
