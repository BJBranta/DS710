first_name = "Benjamin"
last_name = "Branta"


# Task 1: Practice with Tuples
#   Subtask 1.1: Finding Maximums
#     Write a function called maximums(tuple_list) that takes in a list of
#     numeric tuples (tuples of any positive length, including a tuple with
#     a single element). This function returns a new list containing the maximum
#     elements from each of the tuples in tuple_list.
def maximums(tuple_list):
    max_list = []
    for tup in tuple_list:
        max_list.append(max(tup))
    return max_list


# Validated maximums function
assert maximums([(1, 2, 3), (4, 5, 6)]) == [3, 6]
assert maximums(
    [(4.1, -3, 6), (-6, 2.0001, 10), (9 / 5, -5, 8 / 9), (-2, -7, 2, 7, 8, 2)]
) == [6, 10, 1.8, 8]
assert maximums([(1.1, 1.2, -1.3)]) == [1.2]
assert maximums([(0,)]) == [0]  # it's not a tuple without the comma


# Subtask 1.2 Averaging the Maximums
#   Write a function called avg_of_maximums(tuple_list) that takes in an arbitrary
#   list of numeric tuples of arbitrary size, and returns the average of the maximum
#   values of each tuple.
def avg_of_maximums(tuple_list):
    max_list = maximums(tuple_list)
    return sum(max_list) / len(max_list)


# Validate avg_of_maximums function
assert avg_of_maximums([(1, 2, 3), (4, 5, 6)]) == 4.5
assert (
    avg_of_maximums(
        [
            (4.1, -3, 6),
            (-6, 2.0001, 10),
            (1.8, -5, 0.8888888888888888),
            (-2, -7, 2, 7, 8, 2),
        ]
    )
    == 6.45
)
assert avg_of_maximums([(1.1, 1.2, -1.3)]) == 1.2
assert avg_of_maximums([(0,)]) == 0.0


# Task 2: Collatz Sequences
#  Subtask 2.1
#   Write a function collatz_sequence that computes the sequence of numbers leading to 1,
#   starting from an arbitrary positive integer n.
def collatz_sequence(n: int) -> list:
    # Validate Input
    if n <= 0:
        raise ValueError("Input must be a positive integer.")
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")

    # Compute Collatz Sequence
    sequence = []
    while n != 1:
        sequence.append(n)  # Append the current value of n to the sequence
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
    sequence.append(1)  # Append the final element, which is 1
    return sequence


# Validate collatz_sequence function
assert collatz_sequence(1) == [1]
assert collatz_sequence(16) == [16, 8, 4, 2, 1]
assert collatz_sequence(11) == [11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
for n in collatz_sequence(5):  # Test with a positive number
    assert isinstance(n, int)

try:
    collatz_sequence(0.5)
except TypeError:
    pass
else:
    raise AssertionError("Expected TypeError for float input")

try:
    collatz_sequence("2")
except TypeError:
    pass
else:
    raise AssertionError("Expected TypeError for string input")

try:
    collatz_sequence(0)
except ValueError:
    pass
else:
    raise AssertionError("Expected ValueError for zero input")

try:
    collatz_sequence(-1)
except ValueError:
    pass
else:
    raise AssertionError("Expected ValueError for negative input")
