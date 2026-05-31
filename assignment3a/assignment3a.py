first_name = "Benjamin"  # put your first name here, inside the ""
last_name = "Branta"  # put your last name here, inside the ""

# Importing the datetime module to use for Task 3
from datetime import datetime


# Task 1 - Prime Numbers, Revisited
# Subtask 1.1: A function 'is_prime'
# Write a function is_prime that takes in an integer n and returns True if n is prime and False if n is not prime.
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


# Validating is_prime()
assert not is_prime(0)
assert not is_prime(1)
assert is_prime(2)
assert is_prime(3)
assert not is_prime(10)


# Subtask 1.2: Counting Primes
# Write a function called num_primes_to that take as an argument an integer n and returns the number of prime numbers less than or equal to n.
def num_primes_to(n):
    """
    Counts the number of prime numbers less than or equal to n.

    Parameters
    ----------
    n : int
        The number up to which to count prime numbers.

    Returns
    -------
    int
        The number of prime numbers less than or equal to n.
    """
    prime_count = 0  # Initialize count of prime numbers
    for i in range(1, n + 1):  # Loop through numbers from 1 to n
        if is_prime(i):  # Check if i is prime using the is_prime function
            prime_count += 1  # Increment count if i is prime
    return prime_count


# Validating num_primes_to(n)
# print(num_primes_to(100))  # Verify result
assert num_primes_to(-5) == 0
assert num_primes_to(2) == 1
assert num_primes_to(3) == 2
assert num_primes_to(10) == 4


# Task 2 - Advanced Fizzbuzz
# Subtask 2.1: valuation
# Write a function called valuation that take as an argument two postive integers n and d and returns the highest power of d that divides n.
# Specifically valuation(n,d) must be the largest non-negative integer p such that n is divisible by d**p.
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


# Validating valuation(n, d)
# try:
#     valuation(8, 1)
# except ValueError as e:
#     print(e)
assert valuation(8, 2) == 3
assert valuation(8, 3) == 0
assert valuation(8, 4) == 1
assert valuation(50, 2) == 1
assert valuation(50, 5) == 2
assert valuation(50, 3) == 0
assert valuation(n=50, d=3) == 0
assert valuation(d=2, n=64 * 3) == 6


# Subtask 2.2: fizzbuzz_adv
# Write a function fizzbuzz_adv that takes a positive integer n, and returns the advanced fizzbuzz string.
# If the input number is not a positive integer, the function returns the string "invalid".
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
    if n <= 0:  # Check if n is not a positive integer
        return "invalid"
    if not isinstance(n, int):  # Check if n is not an integer
        return "invalid"

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


# Validating fizzbuzz_adv(n)
assert fizzbuzz_adv(3) == "fizz1"
assert fizzbuzz_adv(25) == "buzz2"
assert fizzbuzz_adv(75) == "fizz1buzz2"
assert fizzbuzz_adv(1) == ""
assert fizzbuzz_adv(0) == "invalid"
assert fizzbuzz_adv(3.1415) == "invalid"
assert fizzbuzz_adv(-15) == "invalid"


# Task 3 - Time Until Midnight
# Write a function called minutes_to_midnight(time) that takes between zero and one arguments, and returns the integer whole number of minutes left in the current day (until midnight), taking into account seconds.
def minutes_to_midnight(time=None):
    """
    Returns the integer whole number of minutes left in the current day until midnight.

    Parameters
    ----------
    time : datetime, optional
        A datetime object representing the current time. If None, the current system time is used.
        example: datetime.fromisoformat('2011-11-04T00:05:23'

    Returns
    -------
    int
        The integer whole number of minutes left until midnight.
    """
    if time is None:  # If no time is provided, use the current system time
        time = datetime.now()

    # Calculate total seconds until midnight
    seconds_until_midnight = (
        (23 - time.hour) * 3600 + (59 - time.minute) * 60 + (60 - time.second)
    )
    # Convert seconds to minutes and round down to the nearest whole number
    minutes_until_midnight = seconds_until_midnight // 60
    return minutes_until_midnight


# Validating minutes_to_midnight(time)
# print(minutes_to_midnight())  # Verify result with current system time
assert minutes_to_midnight(datetime.fromisoformat("2011-11-04T05:23:47")) == 1440 - 324
#                                                              HH MM SS

assert minutes_to_midnight(datetime.fromisoformat("2011-11-04T23:59:00")) == 1
assert minutes_to_midnight(datetime.fromisoformat("2011-11-04T23:59:01")) == 0
assert minutes_to_midnight(datetime.fromisoformat("2011-11-04T23:59:59")) == 0

assert minutes_to_midnight(datetime.fromisoformat("2011-11-04T00:00:00")) == 1440
assert minutes_to_midnight(datetime.fromisoformat("2011-11-04T00:00:01")) == 1440 - 1


# Task 4 - Mortgage Calculator, Revisited
# Refactor your code from mortgage calculator. You may possibly use several other functions.
def input_validation(principal, monthly_payment, annual_rate):
    # Value and type validation
    if principal <= 0:
        return ValueError("Principal loan amount must be greater than zero.")
    if not isinstance(principal, (int, float)):
        return TypeError("Principal loan amount must be numeric type int or float.")
    if annual_rate < 0:
        return ValueError("Interest rate cannot be negative.")
    if not isinstance(annual_rate, (int, float)):
        return TypeError("Interest rate must be numeric type int or float.")
    if monthly_payment <= 0:
        return ValueError("Monthly payment must be greater than zero.")
    if not isinstance(monthly_payment, (int, float)):
        return TypeError("Monthly payment must be numeric type int or float.")
    return "valid"


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


def amortization(principal, monthly_payment, annual_rate):
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
    # Validate inputs, tell user what went wrong, return None, None if validation failed
    validation_result = input_validation(principal, monthly_payment, annual_rate)
    if isinstance(validation_result, ValueError) or isinstance(
        validation_result, TypeError
    ):
        print("Input Validation Error:", validation_result)
        return None, None

    balance = principal
    total_paid = 0.0
    months = 0

    while balance > 0:
        interest = calculate_monthly_interest(annual_rate, balance)
        balance += interest  # Add interest to balance
        if balance < monthly_payment:  # Check the remaining balance
            total_paid += balance  # Pay off the remaining balance
            balance = 0.0  # Set balance to zero
        else:
            total_paid += monthly_payment  # Add monthly payment to total paid
            balance -= monthly_payment  # Subtract monthly payment from balance
        months += 1  # Increment month count
        # Check if balance is increasing
        if months > 1 and balance > principal:
            print("Error: Monthly payment is too low to ever pay off the loan.")
            return None, None
    return months, total_paid  # Return total months and total amount paid


# Validating amortization(principal, monthly_payment, annual_rate)
test_case_months, test_case_paid = amortization(
    principal=500, monthly_payment=100, annual_rate=0.05
)
# print(test_case_months, test_case_paid)  # Verify result
assert test_case_months == 6
assert (test_case_paid - 506.346103) < 0.00001
assert (506.346103 - test_case_paid) < 0.00001

test_case_months, test_case_paid = amortization(500, 1, 0.05)
assert test_case_months is None
assert test_case_paid is None
