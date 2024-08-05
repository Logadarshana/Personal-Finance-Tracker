import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ['date', 'amount', 'category', 'description']
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            'date': date, 
            'amount': amount, 
            'category': category, 
            'description': description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
            print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print('No transactions found in the given date range')
        else:
            print(f"Transactions from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}")
            print(
                filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(cls.FORMAT)})
            )

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${total_income - total_expense:.2f}")

        return filtered_df

def get_amount():
    while True:
        try:
            return float(input("Enter the amount: "))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def get_category():
    while True:
        category = input("Enter the category (Income/Expense): ").strip().title()
        if category in ["Income", "Expense"]:
            return category
        print("Invalid category. Please enter either 'Income' or 'Expense'.")

def get_date(prompt, allow_default=False):
    while True:
        date_str = input(prompt).strip()
        if allow_default and date_str == "":
            return datetime.today().strftime(CSV.FORMAT)
        try:
            datetime.strptime(date_str, CSV.FORMAT)
            return date_str
        except ValueError:
            print("Invalid date format. Please enter in dd-mm-yyyy format.")

def get_description():
    return input("Enter the description: ")

def add():
    CSV.initialize_csv()
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or press Enter for today's date: ", 
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df.set_index("date", inplace=True)
    
    income_df = df[df["category"] == "Income"].resample("D").sum()
    expense_df = df[df["category"] == "Expense"].resample("D").sum()
    
    df["net_savings"] = df.apply(lambda row: row["amount"] if row["category"] == "Income" else -row["amount"], axis=1)
    df["cumulative_net_savings"] = df["net_savings"].cumsum()

    plt.figure(figsize=(14, 7))
    
    bar_width = 0.4
    income_bar = plt.bar(income_df.index, income_df["amount"], width=bar_width, label="Income", color="g", align='center')
    expense_bar = plt.bar(expense_df.index, expense_df["amount"], width=bar_width, label="Expense", color="r", align='edge')
    
    plt.plot(df.index, df["cumulative_net_savings"], label="Cumulative Net Savings", color="b", linewidth=2)

    plt.xlabel("Date")
    plt.ylabel("Amount in Rupees")
    plt.title("Income, Expenses, and Cumulative Net Savings Over Time")
    plt.legend()
    plt.grid(True)
    
    # Adding data labels to bars
    for bar in income_bar:
        height = bar.get_height()
        if height != 0:
            plt.annotate(f'{height:.2f}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),  # 3 points vertical offset
                         textcoords="offset points",
                         ha='center', va='bottom')

    for bar in expense_bar:
        height = bar.get_height()
        if height != 0:
            plt.annotate(f'{height:.2f}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, -9),  # 10 points vertical offset down
                         textcoords="offset points",
                         ha='center', va='top')

    plt.show()

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if not df.empty:
                plot_choice = input("Do you want to see a plot? (y/n): ").lower()
                if plot_choice == "y":
                    plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")

if __name__ == "__main__":
    main()








