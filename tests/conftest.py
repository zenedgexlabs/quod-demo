import random
from datetime import date, timedelta

import pytest

from tinyledger import Ledger, Money, Posting


@pytest.fixture
def books():
    ledger = Ledger()
    for name, kind in [("cash", "asset"), ("bank", "asset"), ("loan", "liability"),
                       ("capital", "equity"), ("sales", "income"), ("rent", "expense")]:
        ledger.open(name, kind)
    return ledger


def busy_ledger(n: int, seed: int = 7) -> Ledger:
    """A ledger with n random, balanced transactions."""
    rng = random.Random(seed)
    ledger = Ledger()
    names = [f"acct{i}" for i in range(40)]
    for i, name in enumerate(names):
        ledger.open(name, ("asset", "liability", "equity", "income", "expense")[i % 5])
    day = date(2024, 1, 1)
    for i in range(n):
        a, b = rng.sample(names, 2)
        m = Money(rng.randint(1, 1_000_000))
        ledger.post(day + timedelta(days=i % 365), f"tx {i}", Posting(a, m), Posting(b, -m))
    return ledger
