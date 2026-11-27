from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_EVEN, Decimal

_CENT = Decimal("0.01")


@dataclass(frozen=True, order=True)
class Money:
    """An amount in one currency, held as integer minor units (cents)."""

    cents: int
    currency: str = "USD"

    @classmethod
    def parse(cls, text: str, currency: str = "USD") -> Money:
        amount = Decimal(text.strip().replace(",", "")).quantize(_CENT, rounding=ROUND_HALF_EVEN)
        return cls(int(amount * 100), currency)

    def _check(self, other: Money) -> None:
        if self.currency != other.currency:
            raise ValueError(f"currency mismatch: {self.currency} vs {other.currency}")

    def __add__(self, other: Money) -> Money:
        self._check(other)
        return Money(self.cents + other.cents, self.currency)

    def __sub__(self, other: Money) -> Money:
        self._check(other)
        return Money(self.cents - other.cents, self.currency)

    def __neg__(self) -> Money:
        return Money(-self.cents, self.currency)

    def allocate(self, ratios: list[int]) -> list[Money]:
        """Splits the amount by ratios without losing a cent; leftovers go to
        the first parts."""
        total = sum(ratios)
        if total <= 0:
            raise ValueError("ratios must sum to a positive number")
        parts = [self.cents * r // total for r in ratios]
        for i in range(self.cents - sum(parts)):
            parts[i % len(parts)] += 1
        return [Money(p, self.currency) for p in parts]

    def __str__(self) -> str:
        sign = "-" if self.cents < 0 else ""
        whole, frac = divmod(abs(self.cents), 100)
        return f"{sign}{whole:,}.{frac:02d} {self.currency}"
