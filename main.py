import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from data_entry import get_amount, get_category, get_date, get_description


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    """
    Checking for a CSV file. If none, initialize a CSV file.
    """

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }

        """
        Create a CSV writer to write a dictionary for the CSV file.
        """
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully.")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        """
        Create a Mask
        """
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]  # Locates all rows that the Mask matches

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(
                f"\nTransactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )
            """
            Prints a summary of total income and expenses for the specified date range.
            """
            total_income = filtered_df[filtered_df["category"] == "Income"][
                "amount"
            ].sum()
            total_expenses = filtered_df[filtered_df["category"] == "Expenses"][
                "amount"
            ].sum()
            print("\nSummary:")
            print(f"Total Income: {total_income:.2f}")
            print(f"Total Expenses: {total_expenses:.2f}")
            print(f"Net Savings: {(total_income - total_expenses):.2f}")
        
        return filtered_df


def add():
    CSV.initialize_csv
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) [press ENTER if today]: ",
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expenses_df = (
        df[df["category"] == "Expenses"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    """
    Plots the income and expenses
    """
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expenses_df.index, expenses_df["amount"], label="Expenses", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1. Add a new transaction.")
        print("2. View transactions and summary within a date range.")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("enter the start date (dd-mm-yyyy): ")
            end_date = get_date("enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...", end="\n\n")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
