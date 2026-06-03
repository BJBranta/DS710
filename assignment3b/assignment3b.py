first_name = "Benjamin"
last_name = "Branta"


# Task 1 - Is prime, Revisited
# Write a function is_prime(), that tells you if a number is prime or not,
#  and which raises for non-integer and non-positive inputs.
def is_prime(n):
    """
    Checks if a number n is prime.

    Parameters
    ----------
    n : int
        The number to check if it is prime.

    Returns
    -------
    bool
        True if n is prime, False if n is not prime.
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if isinstance(n, int) and n <= 0:
        raise ValueError("Input is a an integer but not positive")

    if n <= 1:  # if n = 0 or n = 1, it is not prime
        return False
    for q in range(2, n):  # loop through numbers from 2 to n-1
        if (
            n % q == 0
        ):  # if n is divisible by any number between 2 and n-1, it is not prime
            return False
    return (
        True  # if we reach this point the prime checks passed and we should return True
    )


# is_prime() validation
assert is_prime(41) == True  # returns True
assert is_prime(24) == False  # returns False
try:
    is_prime(-0.1)  # raises a TypeError
except TypeError as e:
    assert str(e) == "Input must be an integer"

try:
    is_prime(3.14159)  # raises a TypeError
except TypeError as e:
    assert str(e) == "Input must be an integer"

try:
    is_prime(-1)  # raises a ValueError
except ValueError as e:
    assert str(e) == "Input is a an integer but not positive"

try:
    is_prime(0)  # raises a ValueError
except ValueError as e:
    assert str(e) == "Input is a an integer but not positive"

assert is_prime(1) == False
print("All task 1 tests passed!")


# Task 2 - Fizzbuzz advanced, revisited
def valuation(n, d):
    """
    Returns the highest power of d that divides n.

    Parameters
    ----------
    n : int
        The positive integer to check for divisibility.
    d : int
        The positive base number to check divisibility against.

    Returns
    -------
    int
        The highest power of d that divides n.
    """
    if d == 1:
        raise ValueError(
            "d must be greater than 1"
        )  # if d is 1, then 1^p divides n for all p resulting in infinite loop.

    exponent = 1  # Initialize power to 1, n^0 is always 1
    while n % (d ** (exponent)) == 0:  # Check if n is divisible by d^(exponent)
        exponent += 1  # Increment exponent if n is divisible by d^(exponent)
    return exponent - 1  # Subtract 1 to get the highest power that divides n


def fizzbuzz_adv(n):
    """
    Returns the advanced fizzbuzz string for a positive integer n.

    Parameters
    ----------
    n : int
        A positive integer.

    Returns
    -------
    str
        The advanced fizzbuzz string for n, or "invalid" if n is not a positive integer.
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if isinstance(n, int) and n <= 0:
        raise ValueError("Input is a an integer but not positive")

    power_of_3 = valuation(n, 3)  # Get the highest power of 3 that divides n
    power_of_5 = valuation(n, 5)  # Get the highest power of 5 that divides n
    if n % 3 == 0 and n % 5 == 0:
        return f"fizz{power_of_3}buzz{power_of_5}"
    elif n % 3 == 0:
        return f"fizz{power_of_3}"
    elif n % 5 == 0:
        return f"buzz{power_of_5}"
    else:  # n is not divisible by 3 or 5
        return ""


# fizzbuzz_adv() validation
fizzbuzz_adv(3) == "fizz1"
fizzbuzz_adv(25) == "buzz2"
fizzbuzz_adv(75) == "fizz1buzz2"
fizzbuzz_adv(1) == ""
fizzbuzz_adv(17) == ""
try:
    fizzbuzz_adv(0)
except ValueError as e:
    assert str(e) == "Input is a an integer but not positive"
try:
    fizzbuzz_adv(-1)
except ValueError as e:
    assert str(e) == "Input is a an integer but not positive"
try:
    fizzbuzz_adv(-0.0123)
except TypeError as e:
    assert str(e) == "Input must be an integer"
try:
    fizzbuzz_adv(0.0123)
except TypeError as e:
    assert str(e) == "Input must be an integer"
try:
    fizzbuzz_adv(0.1)
except TypeError as e:
    assert str(e) == "Input must be an integer"
print("All task 2 tests passed!")


# Task 2 - Filename Extension Verification
# Subtask 2.1: Filename checker
# Create a function add_filename_extension(name,ext) that accepts
#   1. the base filename of the file.
#   2. a file extension/type such as 'py', 'csv', or '.txt'
# The checker should return 'name' if it already includes the correct suffix, or 'name + ext'
#  if name does not include the correct suffix, adding the dot if necessary.
def add_filename_extension(name, ext):
    """
    Adds the file extension ext to the filename name if it does not already have it.

    Parameters
    ----------
    name : str
        The base filename of the file.
    ext : str
        The file extension/type such as 'py', 'csv', or '.txt'.

    Returns
    -------
    str
        The filename with the correct extension.
    """
    # Validate inputs are strings
    if not isinstance(name, str) or not isinstance(ext, str):
        raise TypeError("Both name and ext must be strings")

    # Remove leading dot from ext if it exists to standardize
    ext = ext.lstrip(".")

    # Check if name already ends with the correct extension, if so return name
    if name.endswith("." + ext):
        return name

    # If name does not end with the correct extension, add the extension to the name and return it
    return f"{name}.{ext}"


# add_filename_extension() validation
assert add_filename_extension("my_csv", "csv") == "my_csv.csv"
assert add_filename_extension("my_csv", ".csv") == "my_csv.csv"
assert add_filename_extension("my_csv.csv", "csv") == "my_csv.csv"
assert add_filename_extension("my_csv.csv", "py") == "my_csv.csv.py"  # this is failing
assert add_filename_extension("my_csv.csv", ".py") == "my_csv.csv.py"
print("All filename extension tests passed!")


# Subtask 2.2: Curry for specific filetypes
# Use your function from Subtask 2.1 and the process of currying to create two lambdas add_csv(name)
# and add_txt(name). The output of each lambda should be a string.
add_csv = lambda name: add_filename_extension(name, "csv")
add_txt = lambda name: add_filename_extension(name, "txt")

# add_csv() and add_txt() validation
assert add_csv("foo") == "foo.csv"
assert add_txt("foo.bar") == "foo.bar.txt"
assert add_txt("foo") == "foo.txt"
assert add_txt("foo.txt.txt") == "foo.txt.txt"
print("All curried filename extension tests passed!")


# Task 3 - Mortgage Calculator, Revisited
def format_csv(a, b, c, d):
    if a == "Month":
        return f"{a},{b},{c},{d}\n"
    else:
        return f"{a},{b:.2f},{c:.2f},{d:.2f}\n"


def input_validation(principal, monthly_payment, annual_rate):
    # Value and type validation
    if principal <= 0:
        raise ValueError("Principal loan amount must be greater than zero.")
    if not isinstance(principal, (int, float)):
        raise TypeError("Principal loan amount must be numeric type int or float.")
    if annual_rate < 0:
        raise ValueError("Interest rate cannot be negative.")
    if not isinstance(annual_rate, (int, float)):
        raise TypeError("Interest rate must be numeric type int or float.")
    if monthly_payment <= 0:
        raise ValueError("Monthly payment must be greater than zero.")
    if not isinstance(monthly_payment, (int, float)):
        raise TypeError("Monthly payment must be numeric type int or float.")
    return True  # If all checks pass return True.


def calculate_monthly_interest(annual_rate, balance):
    """
    Converts an annual interest rate to a monthly interest rate.

    Parameters
    ----------
    annual_rate : float
        The annual interest rate as a number between 0 and 1, 1 being 100%).
    balance : float
        The current loan balance.

    Returns
    -------
    float
        The monthly interest rate as a number between 0 and 1.
    """
    return (annual_rate / 12) * balance


def format_tsv(a, b, c, d):
    if a == "Month":
        return f"{a}\t{b}\t{c}\t{d}\n"  # use \t separators not commas
    else:
        return f"{a}\t{b:.2f}\t{c:.2f}\t{d:.2f}\n"  # use \t separators not commas


def format_aligned(a, b, c, d):
    if a == "Month":
        return (
            f"{a:>7}{b:>13}{c:>13}{d:>13}\n"  # right align text with specified widths
        )
    else:
        return f"{a:>7}{b:>13.2f}{c:>13.2f}{d:>13.2f}\n"  # right align text with specified widths and 2 decimal places


def amortization(
    principal, monthly_payment, annual_rate, filename=None, format_function=format_csv
):
    """
    Calculates the amortization schedule for a mortgage.

    Parameters
    ----------
    principal : float
        The initial loan amount.
    monthly_payment : float
        The fixed monthly payment amount.
    annual_rate : float
        The annual interest rate as a number between 0 and 1, 1 being 100%).

    Returns
    -------
    int, float
            1. the number of months it took to pay off the loan,
            2. the total amount paid (unrounded)

    """
    input_validation(principal, monthly_payment, annual_rate)

    balance = principal
    total_paid = 0.0
    months = 0
    file_rows = None  # Using a list to store text for the file

    if filename is not None:
        file_rows = [
            format_function("Month", "Payment", "Interest", "Balance")
        ]  # Adding header row to file

    while balance > 0:
        interest = calculate_monthly_interest(annual_rate, balance)
        balance += interest
        if balance < monthly_payment:
            payment = balance  # If the remaining balance is less than the monthly payment, we only need to pay the remaining balance
            total_paid += balance
            balance = 0.0
        else:
            payment = monthly_payment  # If the remaining balance is greater than or equal to the monthly payment, we pay the full monthly payment
            total_paid += monthly_payment
            balance -= monthly_payment
        months += 1
        if months > 1 and balance > principal:
            raise ValueError(
                "Error: Monthly payment is too low to ever pay off the loan."
            )
        if file_rows is not None:
            file_rows.append(
                format_function(months, payment, interest, balance)
            )  # Adding row for current month to file, using format_function to format the row text

    if file_rows is not None:  # Writing to the file
        with open(
            add_txt(filename), "w"
        ) as output_file:  # using add_txt to ensure the file has a .txt extension
            output_file.writelines(file_rows)

    return months, total_paid


# amortization() validation
# print(amortization(500, 500, 0.05))  # no filename passed, no file written
# amortization(500, 100, 0.05)  # no filename passed, no file written
# amortization(
#     500, 1, 0.05, "exception_should_have_been_raised.txt"
# )  # ValueError exception raised, no file written
# amortization(500, 500, 0.05, "am_table_500_500_5.txt")
# amortization(500, 100, 0.05, "am_table_500_100_5")


# Subtask 3.2 - Write your own format functions
# Subtask 3.2.1 - format_tsv
# Write a format function called format_tsv that behaves very similarly to format_csv but instead uses tab as a separator instead of comma.
# def format_tsv(a, b, c, d):
#     if a == "Month":
#         return f"{a}\t{b}\t{c}\t{d}\n"  # use \t separators not commas
#     else:
#         return f"{a}\t{b:.2f}\t{c:.2f}\t{d:.2f}\n"  # use \t separators not commas
# amortization(500, 100, 0.05, "am_table_500_100_5", format_tsv)


# Subtask 3.2.2 - format_aligned
# def format_aligned(a, b, c, d):
#     if a == "Month":
#         return (
#             f"{a:>7}{b:>13}{c:>13}{d:>13}\n"  # right align text with specified widths
#         )
#     else:
#         return f"{a:>7}{b:>13.2f}{c:>13.2f}{d:>13.2f}\n"  # right align text with specified widths and 2 decimal places
# amortization(500, 100, 0.05, "am_table_500_100_5", format_aligned)
