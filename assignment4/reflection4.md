# Assignment 4 Reflection - Ben Branta

## 1. Describe the practice of looping over containers in Python, particularly compared to other experiences you've had, such as Excel or R.

**Answer:** The most experience I have is with Python. Looping over containers in Python makes it very intuitive. It doesn't require unique indexing, however, enumerate is a very useful. I haven't had to do this much in R but I just think the syntax is easier in Python.

---

## 2. Do some research. What is None in Python? Why is it the default returned value from functions?

**Answer:** A good test case to me would check that the outputs are correct, corner cases are handled, and inputs are validated. It should check and make sure the function handles errors gracefully. I think a well defined function with a single purpose would perform correctly if it passes the test cases. 

---

## 3. Describe the experimentation you did for the sequences of fizzbuzz for collatz sequences. What did you do? What are your observations?

**Answer:** In assignment 2 I prepared it as a function with control flow so it was an easy conversion. I did add helper functions for input validation and calculating the monthly interest. The input validation was a nice way to improve my mortgage calculator function because it adds many lines of code that detract from the actual purpose of the function. The calculate monthly interest function was a nice way to turn a math equation into a meaningful action that is readable. Equations are up to the reader to interpret so giving it a function name helps a reader understand its purpose. I did not add anything beyond those two because the rest of it was relatively easy to understand.

---

## 4. What was the most difficult part of the text analysis problem, and why? How did you overcome it?

**Answer:** No it does not sufficiently communicate there was an issue. In assignment 2 I used try/except and raised exceptions with text descriptions of the issue. Here I returned None, None but triggered a print statement explaining the issue as well. Adding a text description or a failure code would help.

---

## 5. Name a programming mistake you found yourself making a lot at first in this class, and which you make a lot less now. How did you reduce the number of instances of this mistake, and how might you approach novel mistakes to help your recognize them faster in the future?

**Answer:** I struggle the most with input validation and looking for error cases. In this lesson I created an infinite loop via a helper function. I found that by working with a coding agent and asking for failure cases of my function that it helps prevent creating errors that I didn't even know to think of. It is much more capable of processing these requests and each time it finds a mistake I know to look for it next time.

---

## 6. Describe one thing that you learned while working on this lesson that stood out as useful or interesting.

**Answer:** I struggle the most with input validation and looking for error cases. In this lesson I created an infinite loop via a helper function. I found that by working with a coding agent and asking for failure cases of my function that it helps prevent creating errors that I didn't even know to think of. It is much more capable of processing these requests and each time it finds a mistake I know to look for it next time.