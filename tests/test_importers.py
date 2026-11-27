from tinyledger import Money, read_csv

CSV = """\
# date,memo,debit,credit,amount
2024-01-02,owner invests,bank,capital,"1,000.00"
2024-01-05,coffee sale,cash,sales,4.50
2024-01-31,january rent,rent,bank,800
"""


def test_read_csv(books):
    assert read_csv(books, CSV) == 3
    assert books.balance("bank") == Money(200_00)
    assert books.balance("cash") == Money(4_50)


def test_semicolon_separated(books):
    assert read_csv(books, "2024-01-02;owner invests;bank;capital;1000.00\n") == 1
    assert books.balance("bank") == Money(1_000_00)


def test_blank_lines_and_comments(books):
    assert read_csv(books, "\n# nothing\n\n") == 0


def test_currency_column(books):
    read_csv(books, "2024-02-01,eu sale,cash,sales,10.00,EUR\n")
    assert books.balance("cash", "EUR") == Money(10_00, "EUR")
    assert books.balance("cash") == Money(0)


def test_read_csv_bulk(books):
    rows = "".join(
        f"2024-03-{1 + i % 28:02d},sale {i},cash,sales,{i % 500}.{i % 100:02d}\n" for i in range(280_000)
    )
    assert read_csv(books, rows) == 280_000
    assert books.balance("cash").cents == -books.balance("sales").cents
