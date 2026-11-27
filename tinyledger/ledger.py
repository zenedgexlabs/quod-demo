from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date

from .money import Money

KINDS = ("asset", "liability", "equity", "income", "expense")


@dataclass(frozen=True)
class Posting:
    account: str
    amount: Money  # positive = debit, negative = credit


@dataclass
class Transaction:
    when: date
    memo: str
    postings: list[Posting]


@dataclass
class Ledger:
    accounts: dict[str, str] = field(default_factory=dict)  # name -> kind
    transactions: list[Transaction] = field(default_factory=list)

    def open(self, name: str, kind: str) -> None:
        if kind not in KINDS:
            raise ValueError(f"unknown account kind {kind!r}")
        if name in self.accounts:
            raise ValueError(f"account {name!r} already open")
        self.accounts[name] = kind

    def post(self, when: date, memo: str, *postings: Posting) -> Transaction:
        if len(postings) < 2:
            raise ValueError("a transaction needs at least two postings")
        for p in postings:
            if p.account not in self.accounts:
                raise KeyError(f"unknown account {p.account!r}")
        by_currency: dict[str, int] = defaultdict(int)
        for p in postings:
            by_currency[p.amount.currency] += p.amount.cents
        if any(by_currency.values()):
            raise ValueError(f"unbalanced transaction {memo!r}: {dict(by_currency)}")
        tx = Transaction(when, memo, list(postings))
        self.transactions.append(tx)
        return tx

    def balance(self, account: str, currency: str = "USD") -> Money:
        total = 0
        for tx in self.transactions:
            for p in tx.postings:
                if p.account == account and p.amount.currency == currency:
                    total += p.amount.cents
        return Money(total, currency)

    def balances(self, currency: str = "USD") -> dict[str, Money]:
        totals: dict[str, int] = {name: 0 for name in self.accounts}
        for tx in self.transactions:
            for p in tx.postings:
                if p.amount.currency == currency:
                    totals[p.account] += p.amount.cents
        return {name: Money(c, currency) for name, c in totals.items()}
