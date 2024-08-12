from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expenses"}


def get_date(
    prompt, allow_default=False
):  # allow_default means that upon hitting enter, the current date is inoutted
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date. Please enter the date in dd-mm-yyyy.")
        return get_date(prompt, allow_default=False)  # Recursion to get a correct date


def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount should be greater than zero.")
        return "%2f" % amount
    except ValueError as e:
        print(e)
        return get_amount()  # Recursion to get a correct amount


def get_category():
    category = input("Enter the category ('I' for Income|'E' for Expenses): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]

    print("Invalid category. Pleae enter 'I' for Income or 'E' for Expenses")
    return get_category()


def get_description():
    return input("Enter a description (optional): ")
