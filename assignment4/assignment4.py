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


# Task 3: Collatz Fizzbuzz
# Subtask 3.1 - Generate the sequences of fizzbuzz from collatz
# Write a function collatz_fizzbuzz that takes a positive integer n as an argument
#  and returns a list (finite sequence) of strings of the form 'fizz', 'buzz', 'fizzbuzz', or '',
#  corresponding to the fizzbuzz strings for the terms of the collatz sequence for n
def fizzbuzz(n):
    if n % 3 == 0 and n % 5 == 0:
        return "fizzbuzz"
    elif n % 3 == 0:
        return "fizz"
    elif n % 5 == 0:
        return "buzz"
    else:
        return ""


def collatz_fizzbuzz(n: int) -> list:
    # Initialize the list to store the collatz sequence and the fizzbuzz strings
    # This isn't strictly necessary, but it makes the code clearer
    collatz_seq = []
    fizzbuzz_strings = []

    # Pass n to the collatz_sequence function to get the collatz sequence
    collatz_seq = collatz_sequence(n)

    # For each number in the collatz sequence, compute the corresponding fizzbuzz string and append it to the list
    for num in collatz_seq:
        fizzbuzz_strings.append(fizzbuzz(num))
    return fizzbuzz_strings


collatz_fizzbuzz(1) == [""]
collatz_fizzbuzz(16) == ["", "", "", "", ""]
collatz_fizzbuzz(3) == ["fizz", "buzz", "buzz", "", "", "", "", ""]


# Subtask 3.2 - Count things
# Write a function collatz_fizzbuzz_counts that takes in an integer n as an argument and outputs a dictionary whose
# - keys are the strings 'fizz', 'buzz', 'fizzbuzz', and '' and
# - values are the number of times that key appears in collatz_fizzbuzz(n).
# The keys must appear even if the corresponding value is 0.
def collatz_fizzbuzz_counts(n: int) -> dict:
    # Get the fizzbuzz strings for the collatz sequence of n
    fizzbuzz_strings = collatz_fizzbuzz(n)

    # Initialize a dictionary to count the occurrences of each fizzbuzz string
    counts = {
        "fizz": fizzbuzz_strings.count("fizz"),
        "buzz": fizzbuzz_strings.count("buzz"),
        "fizzbuzz": fizzbuzz_strings.count("fizzbuzz"),
        "": fizzbuzz_strings.count(""),
    }

    return counts


# Validate collatz_fizzbuzz_counts function
assert collatz_fizzbuzz_counts(11) == {"fizzbuzz": 0, "buzz": 4, "fizz": 0, "": 11}


# Subtask 3.2.3 - Experiment
# Write a function collatz_fizzbuzz_experiment that does something, anything, to explore the data generated by collatz_fizzbuzz.
# What's the first integer n for which collatz_fizzbuzz(n) contains m 'fizz's?
def collatz_fizzbuzz_experiment(m: int) -> int:
    # Validate Input and raise exceptions if necessary
    if not isinstance(m, int):
        raise TypeError("m must be an integer")
    if m < 0:
        raise ValueError("m must be non-negative")

    # Initialize current n
    current_n = 1
    while True:  # Loop indefinitely until we find the desired n
        # Get the count of 'fizz' in the collatz_fizzbuzz for current_n
        fizz_count = collatz_fizzbuzz_counts(current_n)["fizz"]
        # Check if the count of 'fizz' is greater than or equal to m
        if fizz_count >= m:  # If it is, return the current n
            return current_n
        # else, increment current_n and continue the loop
        current_n += 1


# Validate collatz_fizzbuzz_experiment function
assert collatz_fizzbuzz_experiment(1) == 3
assert collatz_fizzbuzz_experiment(2) == 6
assert collatz_fizzbuzz_experiment(3) == 12


# Task 4: String Analysis
# Subtask 4.1 Helper Functions
# Write a function non_alpha_chars(s) that takes as input a str of text and returns a
# set of all non-alphabetic characters in that string.
def non_alpha_chars(s: str) -> set:
    non_alpha_set = set()
    for char in s:
        if not char.isalpha():
            non_alpha_set.add(char)
    return non_alpha_set


# Validate non_alpha_chars function
assert non_alpha_chars(
    "This %séntence$$ @#has ’)()()()( *so_ ?+much!!! punctuation.“"
) == {"*", "@", " ", "“", "#", "_", ")", "$", "’", "%", "!", "+", "?", "(", "."}


# Write a function non_space_chars(s) that takes as input a str of text and returns a set of all non-space characters in that string.
# This function is case-sensitive.
# Hint: use .isspace()
def non_space_chars(s: str) -> set:
    non_space_set = set()
    for char in s:
        if not char.isspace():
            non_space_set.add(char)
    return non_space_set


# Validate non_space_chars function
assert non_space_chars("abcd\n\t qwfp") == {"c", "w", "q", "p", "a", "d", "f", "b"}


#  Write a function non_alpha_non_space_chars(s) that takes as input a str of text and returns a set of all non-space non-alphabetic characters in that string.
def non_alpha_non_space_chars(s: str) -> set:
    non_alpha_non_space_set = set()
    for char in s:
        if not char.isalpha() and not char.isspace():
            non_alpha_non_space_set.add(char)
    return non_alpha_non_space_set


# Validate non_alpha_non_space_chars function
assert non_alpha_non_space_chars(
    "This %séntence$$ @#has ’)()()()( *so_ ?+much!!! punctuation.“"
) == {"@", ".", "$", "!", "_", ")", "#", "*", "%", "“", "’", "+", "?", "("}


# Subtask 4.2 - Reading and Cleanup
# Write a function clean(s).
# Takes as input a string: some text you want to clean
# Does the following: Removes all non-alphabetic non-space characters from the input string, and makes all characters lowercase.
# Returns the resulting string.
# This function should call your non_alpha_non_space_chars function.
# Write a function read_and_clean(filename).
# Takes as input a string: the filename of a text file
# Does the following: reads the text file as a string, removes all non-alphabetic non-space characters, and makes all characters lowercase.
# Returns the resulting string.
# Be sure to read the file in utf-8 encoding!
def clean(s: str) -> str:
    non_alpha_non_space = non_alpha_non_space_chars(s)
    cleaned_string = ""
    for char in s:
        if char not in non_alpha_non_space:
            cleaned_string += char.lower()
    return cleaned_string


def read_and_clean(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()
    return clean(text)


# Validate clean and read_and_clean functions
assert (
    clean("This %séntence$$ @#has ’)()()()( *so_ ?+much!!! punctuation.“")
    == "this séntence has  so much punctuation"
)

assert (
    read_and_clean("example_text.txt")
    == "this is a sentence\nthis is another sentence\nthis sentence talks about a fox and a cat and a dog\nthis sentence has a blue bird in it\nthis sentence is  winning\nthis séntence has  so much punctuation\nthis sentence smiles \nthis sentence is unclear on  to or too\nthis sentence is the end"
)


# Subtask 4.2 - Reading and Cleanup
# Write a function unique_words that accepts as input a string, and returns a set of the unique words in that string. Two words that differ only in case are the same word.
# The function discards all non-alpha non-space characters, including punctuation, and is case-insensitive by lowering all characters.
def unique_words(s: str) -> set:
    cleaned_string = clean(s)
    words = cleaned_string.split()
    unique_word_set = set(words)
    return unique_word_set


# Validate unique_words function
assert unique_words(
    "This %séntence$$ @#has ’)()()()( *so_ *so* **so** ?+much!!! punctuation.“"
) == {"so", "séntence", "much", "punctuation", "has", "this"}


#  Write a function num_unique_words that accepts as input a string, and returns the number of unique words in that string (an integer). Two words that differ only in case are the same word.
#  The function discards all non-alpha non-space characters, including punctuation, and is case-insensitive by lowering all characters.
def num_unique_words(s: str) -> int:
    return len(unique_words(s))


# Validate num_unique_words function
assert (
    num_unique_words(
        "This %séntence$$ @#has ’)()()()( *so_ *so* **so** ?+much!!! punctuation.“"
    )
    == 6
)


# Subtask 4.4 Unique Words from a file
# Write a function unique_words_from_file that accepts as input a filename, and returns a set of the unique words that appear in the text file that has that filename.
# Before counting, the function discards all non-alpha non-space characters, including punctuation, and is case-insensitive by lowering all characters.
def unique_words_from_file(filename: str) -> set:
    cleaned_text = read_and_clean(filename)
    return unique_words(cleaned_text)


# Write a function num_unique_words_from_file that accepts as input a filename and returns the number of unique words that appear in the text file that has that filename.
# Before counting, the function discards all non-alpha non-space characters, including punctuation, and is case-insensitive by lowering all characters.
def num_unique_words_from_file(filename: str) -> int:
    return len(unique_words_from_file(filename))


# Validate unique_words_from_file and num_unique_words_from_file functions
assert unique_words_from_file("example_text.txt") == {
    "the",
    "punctuation",
    "sentence",
    "séntence",
    "and",
    "dog",
    "is",
    "to",
    "a",
    "unclear",
    "in",
    "on",
    "cat",
    "this",
    "winning",
    "much",
    "or",
    "end",
    "fox",
    "it",
    "so",
    "smiles",
    "too",
    "has",
    "blue",
    "about",
    "talks",
    "another",
    "bird",
}

assert num_unique_words_from_file("example_text.txt") == 29


# Subtask 4.5 Word counts
# Write a function word_counts that accepts as input a string, and returns a dictionary where words are keys and the number of instances are values of counts of the words in the string.
# Before counting, the function discards all non-alpha non-space characters, including punctuation, and is case-insensitive by lowering all characters.
def word_counts(s: str) -> dict:
    cleaned_string = clean(s)
    words = cleaned_string.split()
    counts = {}
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts


# Validate word_counts function
assert word_counts(
    "This %séntence$$ @#has ’)()()()( *so_ *so* **so** ?+much!!! punctuation.“"
) == {"this": 1, "séntence": 1, "has": 1, "so": 3, "much": 1, "punctuation": 1}


# Subtask 4.6 Word counts from a file
# Write a function word_counts_from_file that accepts as input a filename (a string), and returns a dictionary where words are keys and the values are counts of those words in the text file.
# Before counting, the function discards all non-alpha non-space characters, including punctuation, and is case-insensitive by lowering all characters.
def word_counts_from_file(filename: str) -> dict:
    cleaned_text = read_and_clean(filename)
    return word_counts(cleaned_text)


# Validate word_counts_from_file function
assert word_counts_from_file("example_text.txt") == {
    "this": 9,
    "is": 5,
    "a": 5,
    "sentence": 8,
    "another": 1,
    "talks": 1,
    "about": 1,
    "fox": 1,
    "and": 2,
    "cat": 1,
    "dog": 1,
    "has": 2,
    "blue": 1,
    "bird": 1,
    "in": 1,
    "it": 1,
    "winning": 1,
    "séntence": 1,
    "so": 1,
    "much": 1,
    "punctuation": 1,
    "smiles": 1,
    "unclear": 1,
    "on": 1,
    "to": 1,
    "or": 1,
    "too": 1,
    "the": 1,
    "end": 1,
}
