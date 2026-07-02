first_name = "Benjamin"
last_name = "Branta"

# Import Packages
import matplotlib.pyplot as plt
import numpy as np


# Task 1: Does my array contain a certain value?
# Subtask 1.1 - Determine wheather an array contains a value exactly.
def has_zeros(arr: np.ndarray) -> bool:
    # If arr has any entries which are exactly equal to zero.
    if np.any(arr == 0):
        return True
    # If arr has no entries which are exactly equal to zero.
    return False


# Validate has_zeros
assert has_zeros(np.array([0, 0, 0, 1, 1, 1, 13, 3, 3, 3])) == True
assert has_zeros(np.array([[0, 0, 0], [1, 1, 1], [13, 3, 3]])) == True
assert has_zeros(np.array([1, 1, 1, 13, 3, 3, 3])) == False
assert has_zeros(np.array([[1, 1, 1], [13, 3, 3]])) == False

assert has_zeros(np.array([0.000001, -0.000001])) == False
assert has_zeros(np.array([[1, 2, 3, 4], [1e-1, 1e-2, 1e-3, 1e-4]])) == False


# Subtask 1.2 - Determine whether an array contains a value approximately
def has_approximate_zeros(arr: np.ndarray, tol: float) -> bool:
    # if any elements absolute value is less than tol return true
    if np.any(np.abs(arr) <= tol):
        return True
    # if zero elements absolute value is less than tol return False
    return False


# Validate has_approximate_zeros
assert (
    has_approximate_zeros(np.array([0, 0, 1e-10, 1, 1, 1, 13, 3, 3, 3]), 1e-7) == True
)
assert (
    has_approximate_zeros(np.array([[0, 1e-10, 1e-5], [1, 1, 1], [13, 3, 3]]), 1e-7)
    == True
)
assert has_approximate_zeros(np.array([-1e-8, 1, 1, 13, 3, 3, 3]), 1e-7) == True
assert has_approximate_zeros(np.array([[-2e-9, 1, 1], [13, 3, 3]]), 1e-9) == False

assert has_approximate_zeros(np.array([0.000001, -0.000001]), 1e-10) == False
assert (
    has_approximate_zeros(np.array([[1, 2, 3, 4], [1e-1, 1e-2, 1e-3, 1e-4]]), 1e-10)
    == False
)


# Task 2: Array of prime numbers
# Write a function primes(lower, upper) which produces a numpy 1-d array of the prime numbers between lower and upper,
# inclusive [] of the lower bound and exclusive () of the upper bound. The output must be sorted in increasing order.
# Copy over is_prime() from lesson 3b
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
        raise ValueError("Input is an integer but not positive")

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


# Do not construct the array iteratively. Instead use a list and convert to np.ndarray
def primes(lower, upper) -> np.ndarray:
    primes_list = []
    # range naturally includes lower bound and excludes upper bound
    [primes_list.append(i) for i in range(lower, upper) if is_prime(i)]
    primes_list.sort()  # sort method default is increasing order
    return np.array(primes_list)


# Validate primes.
assert np.all(primes(2, 7) == np.array([2, 3, 5]))
assert np.all(primes(2, 8) == np.array([2, 3, 5, 7]))
assert np.all(primes(2, 9) == np.array([2, 3, 5, 7]))
try:
    primes(-2, 7)
except ValueError as e:
    assert str(e) == "Input is an integer but not positive"
try:
    primes(-1.5, 7)  # this one is getting caught by the range function
except TypeError as e:
    assert str(e) == "'float' object cannot be interpreted as an integer"


# Task 3: Column Statistics
def column_statistics(arr: np.ndarray) -> np.ndarray:
    # Using vstack to create the output array
    return np.vstack(
        (
            arr.mean(axis=0),  # calculate mean down rows
            arr.min(axis=0),  # calculate min down rows
            arr.max(axis=0),  # calculate max down rows
            (arr == 0).sum(axis=0),  # calc zero cnt down rows
        )
    )


# Validate Column Statistics
assert np.allclose(
    column_statistics(np.array([[1, 0, 3], [4, 5, -1]])),
    np.array(
        [
            [2.5, 2.5, 1],
            [1, 0, -1],
            [4, 5, 3],
            [0, 1, 0],
        ]
    ),
)


# Task 4: Sorting and Plotting Counts
# Subtask 4.1: Prep Data
def read_and_structure(filename: str) -> dict:
    result = {}  # initialize result dictionary
    with open(filename, "r", encoding="utf-8") as file:  # open file as read
        for line in file:
            word, count = line.strip().split(",")
            result[word] = int(count)
    return result  # return the cleaned string


word_frequency = read_and_structure("word_frequencies_alice.csv")
frequencies_unsorted = np.array(list(word_frequency.values()))
frequencies_sorted = np.sort(frequencies_unsorted)[::-1]
top_20_counts = frequencies_sorted[:20]
# plot
fig, ax = plt.subplots(1, 1)
ax.bar(
    np.arange(1, 21),  # x-axis
    top_20_counts,  # y-axis
    width=1,
    edgecolor="white",
    linewidth=0.7,
)
ax.set(xlim=(0, 21), xticks=np.arange(1, 21), ylim=(0, max(top_20_counts) + 20))
ax.set_xlabel("Ranked Words (Top 20)")
ax.set_ylabel("Frequency")
fig.savefig(f"{last_name}_{first_name}_assign5_task4.png", dpi=300, bbox_inches="tight")

# fmt: off
# Task 5: Plotting Function Values
# Subtask 5.1 - Make data
x = np.linspace(0, 1, 100)
function_values = np.zeros((5, 100))
function_values[0] = 2 * (x - 1 / 2)
function_values[1] = (3**2 / 2) * (x - 1 / 3) * (x - 2 / 3)
function_values[2] = (4**3 / (2 * 3)) * (x - 1 / 4) * (x - 2 / 4) * (x - 3 / 4)
# I had extra parentheses around the x terms which I think was causing the post submission error.
function_values[3] = (5**4 / (2 * 3 * 4)) * (x - 1 / 5) * (x - 2 / 5) * (x - 3 / 5) * (x - 4 / 5)
# I had extra parentheses around the x terms which I think was causing the post submission error.
function_values[4] = (6**5 / (2 * 3 * 4 * 5)) * (x - 1 / 6) * (x - 2 / 6) * (x - 3 / 6) * (x - 4 / 6) * (x - 5 / 6)

# fmt: on
fig, ax = plt.subplots(1, 1)
labels = ["f1", "f2", "f3", "f4", "f5"]
for i in range(function_values.shape[0]):
    ax.plot(x, function_values[i], label=labels[i])
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
fig.savefig(f"{last_name}_{first_name}_assign5_task5.png", dpi=300, bbox_inches="tight")


# Task 6: Random Data Simulation
# Subtask 6.1 - Generate data
def simulate_busses(mean: int, num_busses: int) -> np.ndarray:
    # Simulate bus arrival times
    exp_d = np.round(np.random.exponential(scale=mean, size=num_busses), 2)
    return exp_d


bus_times = simulate_busses(15, 50)


# Subtask 6.2 - Statisitcs about your data
def mean_wait(bus_times):
    return np.mean(bus_times)


def shortest_wait(bus_times):
    return np.min(bus_times)


def longest_wait(bus_times):
    return np.max(bus_times)


# Subtask 6.3 - Cumulative Wait Times
def cumulative_wait(bus_times: np.ndarray) -> np.ndarray:
    return np.cumsum(bus_times)


# Validate cumulative_wait
assert np.all(
    np.abs(
        cumulative_wait(np.array([11.21, 34.15, 18.89, 23.51]))
        - np.array([11.21, 45.36, 64.25, 87.76])
    )
    < 0.001
)

cum_bus_waits = cumulative_wait(bus_times)

# Subtask 6.4
# Line plot of arrival times
fig, ax = plt.subplots(1, 1)

# x-axis = bus number (1 to N)
bus_numbers = np.arange(1, len(cum_bus_waits) + 1)

ax.plot(bus_numbers, cum_bus_waits)

ax.set_xlabel("Bus Number")
ax.set_ylabel("Arrival Time [Minutes]")

fig.savefig(
    f"{last_name}_{first_name}_assign5_task6_line.png", dpi=300, bbox_inches="tight"
)

# Histogram of wait times
fig, ax = plt.subplots(1, 1)

# choose 5 minute bin widths
bins = np.arange(0, np.max(bus_times) + 5, 5)

ax.hist(bus_times, bins=bins, edgecolor="black")

ax.set_xlabel("Inter-arrival time (minutes)")
ax.set_ylabel("Number of buses")

fig.savefig(
    f"{last_name}_{first_name}_assign5_task6_hist.png", dpi=300, bbox_inches="tight"
)
