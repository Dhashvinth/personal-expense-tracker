from faker import Faker
import random
import pandas as pd

fake = Faker()

random.seed(42)
Faker.seed(42)

categories = [
    "Groceries",
    "Stationery",
    "Bills",
    "Subscription",
    "Investment",
    "Transportation",
]

payment_modes = [
    "UPI",
    "Cash",
    "Credit Card",
]


def generate_month(month, year, entries):

    start = pd.Timestamp(year, month, 1)
    end = start + pd.offsets.MonthEnd(1)

    data = []

    for _ in range(entries):

        payment = random.choice(payment_modes)
        amount = round(random.uniform(100, 4000), 2)

        cashback = 0

        if payment == "UPI":
            cashback = round(amount * 0.03, 2)

        elif payment == "Credit Card":
            cashback = round(amount * 0.02, 2)

        row = {
            "Date": fake.date_between_dates(start, end),
            "Category": random.choice(categories),
            "Payment_Mode": payment,
            "Description": fake.sentence(nb_words=6),
            "Amount": amount,
            "Cashback": cashback,
        }

        data.append(row)

    return pd.DataFrame(data)


def generate_fake_data():

    frames = []

    for month in range(1, 13):
        frames.append(
            generate_month(
                month,
                2025,
                150,
            )
        )

    return pd.concat(
        frames,
        ignore_index=True,
    )
