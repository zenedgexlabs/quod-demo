from datetime import date

from tinyledger import Money, Posting, balance_sheet, trial_balance

from conftest import busy_ledger

D = date(2024, 3, 1)


def test_trial_balance_balances(books):
    books.post(D, "invest", Posting("bank", Money(1_000_00)), Posting("capital", Money(-1_000_00)))
    books.post(D, "sale", Posting("cash", Money(120_00)), Posting("sales", Money(-120_00)))
    debit, credit = trial_balance(books)
    assert debit == credit == Money(1_120_00)


def test_balance_sheet_closes_income_into_equity(books):
    books.post(D, "invest", Posting("bank", Money(1_000_00)), Posting("capital", Money(-1_000_00)))
    books.post(D, "sale", Posting("cash", Money(300_00)), Posting("sales", Money(-300_00)))
    books.post(D, "rent", Posting("rent", Money(100_00)), Posting("bank", Money(-100_00)))
    books.post(D, "borrow", Posting("bank", Money(200_00)), Posting("loan", Money(-200_00)))
    sheet = balance_sheet(books)
    assert sheet["assets"] == Money(1_400_00)
    assert sheet["liabilities"] == Money(200_00)
    assert sheet["equity"] == Money(1_200_00)
    assert sheet["assets"] == sheet["liabilities"] + sheet["equity"]


def test_accounting_equation_bulk():
    for seed in range(14):
        ledger = busy_ledger(25_000, seed)
        sheet = balance_sheet(ledger)
        assert sheet["assets"] == sheet["liabilities"] + sheet["equity"]
        debit, credit = trial_balance(ledger)
        assert debit == credit
