from datetime import date

import pytest

from tinyledger import Money, Posting

from conftest import busy_ledger

D = date(2024, 3, 1)


def test_post_and_balance(books):
    books.post(D, "owner invests", Posting("bank", Money(500_00)), Posting("capital", Money(-500_00)))
    books.post(D, "withdraw", Posting("cash", Money(50_00)), Posting("bank", Money(-50_00)))
    assert books.balance("bank") == Money(450_00)
    assert books.balance("cash") == Money(50_00)
    assert books.balance("capital") == Money(-500_00)


def test_unbalanced_is_rejected(books):
    with pytest.raises(ValueError):
        books.post(D, "oops", Posting("cash", Money(1)), Posting("sales", Money(-2)))


def test_unknown_account(books):
    with pytest.raises(KeyError):
        books.post(D, "x", Posting("cash", Money(1)), Posting("nope", Money(-1)))


def test_single_posting_is_rejected(books):
    with pytest.raises(ValueError):
        books.post(D, "x", Posting("cash", Money(0)))


def test_duplicate_account(books):
    with pytest.raises(ValueError):
        books.open("cash", "asset")


def test_balances_sum_to_zero_bulk():
    ledger = busy_ledger(150_000)
    balances = ledger.balances()
    assert sum(b.cents for b in balances.values()) == 0
    for name in list(ledger.accounts)[:12]:
        assert ledger.balance(name) == balances[name]
