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
    if not isinstance(name, str) or not isinstance(ext, str):
        raise TypeError("Both name and ext must be strings")

    name = name.split(".")[0]  # Remove the existing extension from name
    ext = ext.lstrip(".")  # Remove leading dot from ext if it exists

    return f"{name}.{ext}"  # Add the extension to the name


# add_filename_extension() validation
assert add_filename_extension("my_csv", "csv") == "my_csv.csv"
assert add_filename_extension("my_csv", ".csv") == "my_csv.csv"
assert add_filename_extension("my_csv.csv", "csv") == "my_csv.csv"
assert add_filename_extension("my_csv.csv", "py") == "my_csv.py"
assert add_filename_extension("my_csv.csv", ".py") == "my_csv.py"
print("All filename extension tests passed!")


# Subtask 2.2: Curry for specific filetypes
# Use your function from Subtask 2.1 and the process of currying to create two lambdas add_csv(name)
# and add_txt(name). The output of each lambda should be a string.
add_csv = lambda name: add_filename_extension(name, "csv")
add_txt = lambda name: add_filename_extension(name, "txt")

# add_csv() and add_txt() validation
assert add_csv("foo") == "foo.csv"
assert add_txt("foo.bar") == "foo.txt"
assert add_txt("foo") == "foo.txt"
assert add_txt("foo.txt.txt") == "foo.txt"
print("All curried filename extension tests passed!")


# Task 3 - Mortgage Calculator, Revisited
