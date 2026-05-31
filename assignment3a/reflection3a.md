# Assignment 3a Reflection - Ben Branta

## 1. Describe a mistake you made or error message you got while solving the problems, and how you will recognize in the future that you made the mistake again.

**Answer:** In advanced fizzbuzz I did not have a validation check for if n = 0. The test case fizzbuzz__adv(0) created an infinite loop from my valuation(0, 3) call. In valuation I don't have a check if n = 0. If n = 0 then my while loop permanently evaluates to true causing the infinite loop.

This was recognizable because when I test run my script it never completes. I think this breaks down into a validation problem and its a skill I haven't completely grasped yet. It is something I think about every time now.

---

## 2. What makes a good test case for determining if a function works correctly? How do you know that your functions perform correctly?

**Answer:** A good test case to me would check for valid inputs. It should check and make sure the function cannot error/crash the program or return incorrect information due to type conflicts. A good test case also validates outputs based on known inputs. If my function should return x^2 my test case should test for different values of x against the expected output. Using these two approaches to testing a function I think it should perform correctly.

---

## 3. Did you make any changes to your mortgage calculator other than package it into a function?

**Answer:** In assignment 2 I prepared it as a function with control flow so it was an easy conversion. I did add helper functions for input validation and calculating the monthly interest. The input validation was a nice way to improve my mortgage calculator function because it adds many lines of code that detract from the actual purpose of the function. The calculate monthly interest function was a nice way to turn a math equation into a meaningful action that is readable. Equations are up to the reader to interpret so giving it a function name helps a reader understand its purpose. I did not add anything beyond those two because the rest of it was relatively easy to understand.

---

## 4. Does the returning of None, None in the infinite loop sufficiently communicate to the caller that there was an issue with the inputs? What might be done differently?

**Answer:** No it does not sufficiently communicate there was an issue. In assignment 2 I used try/except and raised exceptions with text descriptions of the issue. Here I returned None, None but triggered a print statement explaining the issue as well. Adding a text description or a failure code would help.

---

## 5. Describe one thing that you learned while working on this lesson that stood out as useful or interesting.

**Answer:** I struggle the most with input validation and looking for error cases. In this lesson I created an infinite loop via a helper function. I found that by working with a coding agent and asking for failure cases of my function that it helps prevent creating errors that I didn't even know to think of. It is much more capable of processing these requests and each time it finds a mistake I know to look for it next time.
