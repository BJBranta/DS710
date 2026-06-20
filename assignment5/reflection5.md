# Assignment 5 Reflection - Ben Branta

## 1. How does working with NumPy compare to working with vanilla Python? Compare looping especially.

**Answer:** Working with NumPy adds a little complexity to make managing large datasets more efficient with regards to looping. Instead of looping over every row, computing something, and appending Numpy enables vectorization to compute over the entire dataset.

---

## 2. Compare plotting in this assignment to previous plotting experiences you may have had, especially R and Excel.

**Answer:** I found plotting in R to be really good. The structure of using ggplot2 was intuitive and a great way to build out plots. Matplotlib with Python I would consider less intuitive and potentially less powerful. For me it is just not as intuitive when it comes to the structure of it. With Python I have used other plotting libraries which create interactive plots and those are where I believe Python plotting has the advantage over R. However, I did not get the chance to look for or try interactive plotting in R. Excel is a great introduction to plotting. It is easier to see what is being selected for each axis. Many of the custom configuration pieces do not exist so an Excel plot is very limited and you get what you get.

---

## 3. Why isn't the average of the bus wait times exactly 15? Will it ever be? When we randomly sample from a distribution, do we ever expect to see the mean exactly?

**Answer:** The average of the bus wait times is not exactly 15 because the data set is pseudo-random data set. As the sample size increases the mean should narrow down to 15 but it will never be exactly 15. 

---

## 4. What was the hardest Task in this assignment? Why?

**Answer:** The hardest task in this assignment was Task 4. I have used Pandas more than Numpy on its own and a lot of this task made me think of how to solve it using Pandas. First, I tried several different methods of importing the csv data and each time I was just wishing to use Pandas read_csv(). Then sorting the values in descending order without the strings required research online. Finally, plotting was a little more difficult because I didn't directly have a nice 'y' and 'x' columns to plot.

---

## 5. Describe one thing that stood out to you as useful from this assignment.

**Answer:** The one thing that stands out as useful from this assignment is Numpy's ability to structure data and transform it efficiently. The vectorization functions like mean, min, max, and sum are much easier to manage when using Numpy. I will also add I found psuedo-random number generation to be a significant feature. I suspect generating random number data sets with defined distributions will be a big help in learning statistics in the future.