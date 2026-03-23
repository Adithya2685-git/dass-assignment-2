"""White-box tests for card deck edge cases."""

from moneypoly.cards import CardDeck


def test_cards_remaining_is_zero_for_empty_deck():
    """Empty decks should report zero remaining cards."""
    deck = CardDeck([])

    assert deck.cards_remaining() == 0


def test_repr_handles_empty_deck():
    """Representing an empty deck should not crash."""
    deck = CardDeck([])

    assert repr(deck) == "CardDeck(0 cards, next=end)"
