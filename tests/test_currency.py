from decimal import Decimal

import pytest

from tinyledger import Money, convert
from tinyledger.currency import RATES


def test_same_currency_is_identity():
    assert convert(Money(123), "USD") == Money(123)


def test_usd_to_eur():
    assert convert(Money(10_000), "EUR") == Money(9_200, "EUR")


def test_cross_rate_through_usd():
    assert convert(Money(7_900, "GBP"), "EUR") == Money(9_200, "EUR")


def test_unknown_currency():
    with pytest.raises(ValueError):
        convert(Money(1), "XYZ")


def test_round_trip_bulk():
    # Converting there and back loses at most a couple of cents to rounding.
    for cents in range(0, 3_000_000, 15):
        for cur in ("EUR", "GBP", "INR"):
            back = convert(convert(Money(cents), cur), "USD")
            assert abs(back.cents - cents) <= 2, (cents, cur, back)


def test_rates_are_positive():
    assert all(r > Decimal(0) for r in RATES.values())
