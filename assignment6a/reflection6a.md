# Assignment 6a Reflection - Ben Branta

## 1. There are some common patterns we expected you to use in this assignment. Describe a few patterns of working with pandas that you used in this assignment.

**Answer:** The first pattern I used frequently was looking up the index label for the row with the maximum value within a column using idxmax(). I would use that index to then filter the dataframe for the specific row, and then pick the column value of interest. For example in "salary_df.loc[salary_df["Years in Job"].idxmax()]["Name"]" I'm getting the index label for the row where the maximum value in column "Years in Job", filtering the dataframe to capture that row, and grabbing the name of the person. This pattern came up several times in the assignment.

Another common pattern was counting True values in a boolean dataframe. In addition, filtering using conditionals. For example in "sum((df["Annual Salary"] >= min_val) & (df["Annual Salary"] <= max_val))" the conditional logic within sum() is creating a boolean dataframe. This means it is TRUE where the conditions are met and FALSE otherwise. Then using sum() to count the TRUE values. 

---

## 2. Relate these tasks to others in your professional or personal experience.

**Answer:** For work I had to integrate and standup a vehicle subscription service management system. There wasn't any direction on how to do it. I learned Python and used Pandas to manage internal database tables (via .csv exports) and external database tables (via .csv exports) to create an application that synchronized our internal system and the telematics web portal provider platform. In those scripts I had to consistenly read in .csv files, filter and search for matching assets, then sort and perform some functions with the returned dataframes. In another application I parse and store vehicle signal data into pandas dataframes so that I could create line plots, using Plotly, to compare raw vs captured data from a vehicle. In all of these cases the patterns within this assignment were used.

---

## 3. Did you find yourself solving the problems in another language / tool? We know many students come into this class with experience in R, Excel, and others. Compare.

**Answer:** I didn't use another tool. Python and pandas has been my primary experience. I do want to use R more. With pandas I find that the syntax isn't as easy to read. Filtering dataframes can be confusing to read if there are many transformations. R introduced me to the pipe operator and its well designed methods for slicing and analyzing dataframes. I still lean towards Python for its flexibility.

For this assignment I did start using a python notebook on the side to solve the problem and then copy it into the script. I found this to be very helpful when trying different filters and understanding the results I was getting. In addition, VS Code has a plugin called Data Wrangler that I'm finding to be a good replacement for the variable viewer that Spyder does so well.

---

## 4. Pandas takes care of almost all looping for you. Do you find that this devalues the looping we taught earlier in the class? Why or why not?

**Answer:** No I do not think in devalues the looping. In my opinion, Python is a fantastic multi-tool and understanding the fundamentals is very important. Early in my learning path I didn't understand much about run time. I have used loops to iterate over dataframes. What I'm trying to understand is how that when our data multiplies in size the bad habits become points of failure. Without understanding what a loop is doing I wouldn't understand why doing that 1 million times is maybe not the best solution.

---

## 5. What new thing did you notice or learn in this lesson that you think will be useful later?

**Answer:** The article on process timing was significant for me. I found it astonishing that by transforming into numpy arrays we could reduce 30+ seconds of run time to 0.3 seconds of run time. Efficiently processing data so that query and downstream load times are fast is important. Overall this assignment was a good reinforcement of filtering with pandas dataframes and the problems felt like good variations on the common patterns.