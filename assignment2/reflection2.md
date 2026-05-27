# Assignment 2 Reflection

## 1. In Task 2, what might you change if you wanted to find how many prime numbers there are up to some arbitrary number, N?

**Answer:** I would change from a for loop to a while loop with an index < N (while ii <= N).

---

## 2. How did you check that your mortgage calculator was computing the correct values? What was a debugging step you took that you found very useful? Go back in time and give yourself advice; write that advice here.?

**Answer:** First I wrote out the instructions provided so I understood the steps for the process. Using VS Code I set a breakpoint and stepped through each line of the function and calculated what I expected it to be and compared it against my code.

---

## 3. How did you deal with the infinite loop case of the mortgage calculator.

**Answer:** I added a check using an if statement. If months was greater than 1 and the balance was greater than the principal loan amount it indicated the principal loan amount was increasing. I then raised a value error.

---

## 4. What was it like to use the unit tests for this assignment?

**Answer:** I spent a lot of time figuring out the unit tests for assignment one so I did not have any issues with this one. I would complete a task, then test, then move on. Finally testing everything once complete. I didn't have any issues with the unit tests for this assignment.

---

## 5. Describe one thing that you learned while working on this lesson that stood out as useful or interesting.

**Answer:** In the mortgage calculator I struggled with handling the error gracefully. I ended up wrapping the function call with the try except block and raising the error in the function.
