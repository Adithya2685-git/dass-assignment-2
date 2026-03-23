"""White-box tests for dice behavior."""

from moneypoly.dice import Dice


def test_roll_uses_full_six_sided_range(monkeypatch):
    """Dice.roll should request values from 1 through 6 for both dice."""
    calls = []

    def fake_randint(low, high):
        calls.append((low, high))
        return 6

    monkeypatch.setattr("moneypoly.dice.random.randint", fake_randint)

    dice = Dice()
    total = dice.roll()

    assert calls == [(1, 6), (1, 6)]
    assert total == 12
