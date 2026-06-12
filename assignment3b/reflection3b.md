# Assignment 3b Reflection - Ben Branta

## 1. What are some different error types and why did you choose the specific ones you chose for fizzbuzz_adv and amortization?

**Answer:** Some different error types are: ValueError, TypeError, NameError, SyntaxError, IndexError, KeyError, AttributeError, ZeroDivisionError, AssertionError.

In advanced fizzbuzz and amortization I chose ValueError and TypeError. TypeError was used to first identify if the input value was of the correct type. ValueError was used to then validate the value was correct. In this case the value was correct if it was greater than or equal to zero.

---

## What is the value of currying a function like add_filename_extension? How did you use this function in amortization?

**Answer:** Currying provides value by using a function and giving it a more defined purpose. This reduces repeating code making it easier to maintain. This also improves code readability. In amortization we start with a function named add_filename_extension. We curry the function and name it add_csv. This re-purposed the existing function and made it easier to understand exactly what this new function is doing.

---

## What other changes did you make to amortization beyond the requirements of this assignment?

**Answer:** I added a helper functions for input validation and calculating the monthly interest. The input validation function helps consolidate the validation code outside of the amortization function to make it easier to understand the purpose of the amortization function. I added a helper function named calculate_monthly_interest to pull the calculation out and give it a function name, making it easier to understand what the calculation is doing.

---

## 4. Why might we want to use a function as an argument for another function?

**Answer:** One good reason to use a function as an argument for another function is it can make the code more flexible. The example from the book was passing string methods as a list to a function to clean strings. In this case, we could write five lines of hard-coded string methods, but by writing one line that reads a list of string methods the code is more flexible.

---

## 5. Describe one thing that you learned while working on this lesson that stood out as useful or interesting.

**Answer:** Currying stood out as useful and interesting. In the past I would have likely made an add_csv and an add_txt function with all of the content of add_filename_extension in each one. Currying is useful because it reduces duplicate code. It was interesting because it made me think about creating flexible code. Instead of the specific thing I should take a step back and ask myself how can I make it general which likely leads to easier to maintain.
