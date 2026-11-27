import pytest

from tinyledger import Money


def test_parse_rounds_half_to_even():
    assert Money.parse("1.005").cents == 100
    assert Money.parse("1.015").cents == 102
    assert Money.parse("1,234.50").cents == 123450


def test_arithmetic():
    assert Money(150) + Money(50) == Money(200)
    assert Money(150) - Money(200) == Money(-50)
    assert -Money(5) == Money(-5)


def test_currency_mismatch():
    with pytest.raises(ValueError):
        Money(1, "USD") + Money(1, "EUR")


def test_str():
    assert str(Money(123456)) == "1,234.56 USD"
    assert str(Money(-5, "EUR")) == "-0.05 EUR"


@pytest.mark.parametrize("cents", [0, 1, 99, 100, 101, 9_999, 1_000_003])
@pytest.mark.parametrize("ratios", [[1], [1, 1], [1, 1, 1], [3, 7], [1, 2, 3, 4]])
def test_allocate_never_loses_a_cent(cents, ratios):
    parts = Money(cents).allocate(ratios)
    assert sum(p.cents for p in parts) == cents


def test_allocate_bulk():
    # Every split of every amount up to 70,000 cents into 2 to 7 equal parts.
    for cents in range(70_000):
        for k in range(2, 8):
            parts = Money(cents).allocate([1] * k)
            assert sum(p.cents for p in parts) == cents
            assert max(p.cents for p in parts) - min(p.cents for p in parts) <= 1
