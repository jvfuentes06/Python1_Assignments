from datetime import date

KINDS = ["expense", "income"]
CATEGORIES = ["food", "rent", "transport", "utilities", "leisure", "health", "salary", "other"]
CURRENCIES = ("EUR", "USD", "GBP")


def fail(message):
    print("Error:", message)
    raise SystemExit(1)

import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
commands = parser.add_subparsers(dest="command", required=True)

add = commands.add_parser("add")
commands.add_parser("summary")
add.add_argument("--date", required=True)
add.add_argument("--kind", required=True)
add.add_argument("--category", required=True)
add.add_argument("--amount", required=True)
add.add_argument("--currency", default="EUR")

commands.add_parser("list")

args = parser.parse_args()

file = Path("budget.json")
transactions = json.loads(file.read_text()) if file.exists() else []

if args.command == "add":
    kind = args.kind.strip().lower()
    category = args.category.strip().lower()
    currency = args.currency.strip().upper()

    try:
        amount = float(args.amount)
    except ValueError:
        fail(f"amount must be a number (got {args.amount!r}).")
    if amount <= 0:
        fail(f"amount must be > 0 (got {args.amount}).")

    try:
        date.fromisoformat(args.date)
    except ValueError:
        fail(f"date must be a real date as YYYY-MM-DD (got {args.date!r}).")

    if kind not in KINDS:
        fail(f"kind must be one of {', '.join(KINDS)} (got {kind!r}).")
    if category not in CATEGORIES:
        fail(f"category must be one of {', '.join(CATEGORIES)} (got {category!r}).")
    if currency not in CURRENCIES:
        fail(f"currency must be one of {', '.join(CURRENCIES)} (got {currency!r}).")

    transaction = {
        "id": f"T{len(transactions) + 1:03d}",
        "date": args.date,
        "kind": kind,
        "category": category,
        "amount": amount,
        "currency": currency,
    }
    transactions.append(transaction)
    file.write_text(json.dumps(transactions))
    print("Added", transaction["id"])

    transaction = {
        "id": f"T{len(transactions) + 1:03d}",
        "date": args.date,
        "kind": args.kind,
        "category": args.category,
        "amount": amount,
    }
    transactions.append(transaction)
    file.write_text(json.dumps(transactions))
    print("Added", transaction["id"])

elif args.command == "summary":
    income = 0
    expense = 0
    for t in transactions:
        if t["kind"] == "income":
            income += t["amount"]
        else:
            expense += t["amount"]
    print(f"Income:  {income:.2f}")
    print(f"Expense: {expense:.2f}")
    print(f"Balance: {income - expense:.2f}")

