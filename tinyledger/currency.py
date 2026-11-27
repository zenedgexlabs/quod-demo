from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal

from .money import Money

# Units of each currency per 1 USD.
RATES: dict[str, Decimal] = {
    "USD": Decimal("1"),
    "EUR": Decimal("0.92"),
    "GBP": Decimal("0.79"),
    "JPY": Decimal("151.20"),
    "INR": Decimal("83.40"),
}


def convert(amount: Money, to: str, rates: dict[str, Decimal] = RATES) -> Money:
    """Converts through USD, rounding half to even to the cent."""
    if amount.currency == to:
        return amount
    try:
        usd = Decimal(amount.cents) / rates[amount.currency]
        cents = (usd * rates[to]).quantize(Decimal("1"), rounding=ROUND_HALF_EVEN)
    except KeyError as e:
        raise ValueError(f"no rate for {e.args[0]}") from None
    return Money(int(cents), to)
