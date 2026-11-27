from __future__ import annotations

from .ledger import Ledger
from .money import Money


def trial_balance(ledger: Ledger, currency: str = "USD") -> tuple[Money, Money]:
    """Total debits and total credits (as a positive amount). Equal in a
    well-formed ledger."""
    debit = credit = 0
    for b in ledger.balances(currency).values():
        if b.cents >= 0:
            debit += b.cents
        else:
            credit -= b.cents
    return Money(debit, currency), Money(credit, currency)


def balance_sheet(ledger: Ledger, currency: str = "USD") -> dict[str, Money]:
    """Assets, liabilities and equity, with net income closed into equity."""
    sums = {k: 0 for k in ("asset", "liability", "equity", "income", "expense")}
    for name, b in ledger.balances(currency).items():
        sums[ledger.accounts[name]] += b.cents
    net_income = -(sums["income"] + sums["expense"])
    return {
        "assets": Money(sums["asset"], currency),
        "liabilities": Money(-sums["liability"], currency),
        "equity": Money(-sums["equity"] + net_income, currency),
    }
