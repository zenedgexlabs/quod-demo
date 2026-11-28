from __future__ import annotations

import csv
import io
from datetime import date

from .ledger import Ledger, Posting
from .money import Money


def read_csv(ledger: Ledger, text: str) -> int:
    """Posts one transaction per row of `date,memo,debit_account,credit_account,amount[,currency]`.
    Semicolon-separated files (common in European exports) are accepted too.
    Returns the number of transactions posted."""
    n = 0
    delimiter = ";" if text.count(";") > text.count(",") else ","
    for row in csv.reader(io.StringIO(text), delimiter=delimiter):
        if not row or row[0].startswith("#"):
            continue
        when, memo, debit, credit, amount, *rest = (c.strip() for c in row)
        money = Money.parse(amount, rest[0] if rest else "USD")
        ledger.post(date.fromisoformat(when), memo, Posting(debit, money), Posting(credit, -money))
        n += 1
    return n
