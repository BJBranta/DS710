# Assignment 6b Reflection - Ben Branta

## 1. Describe the process for plotting from pandas DataFrames, and using the tools/libraries you selected. Why did you choose the libraries you used?

**Answer:** Plotting from pandas DataFrames first requires filtering the dataframe to form the data you intend to visualize as columns. Filtering may not be required but typically some cleaning, like removing NaN, is necessary. Once you have a clean and formatted DataFrame plotting it was as simple as picking the plot and passing the DataFrame, the column for the x-axis, and the column for the y-axis. The required arguments are plot type dependent. Additional arguments are available to improve the plot such as categorizing by color and shape.

---

## 2. The violin plot for faculty salaries had many violins. How did you prompt an AI tool to help you to make the plot look nice? What adjustments did you need to make to the code given?

**Answer:** First I structed the plot as much as I could on my own. This got me to having a violin plot with everything on it. This helps me frame the context for the LLM to achieve the result I'm looking for. For this problem I used ChatGPT and the prompt I used is below. With this prompt I let the LLM return suggestions on how to make the plot look nice. In this approach it allows me to choose which ones to add or to ask specific follow up question about a suggestion. I had to make the figure wider, sort the violin plots by median salary to help make a comparison, and add a title. It suggested a single color and removing the legend which were not necessary so I left those out. I did not have to ask it to revise the code because after the initial prompt I tell it exactly what I want. Usually this helps prevent strange things being changed I didn't ask about.

'''
PROMPT: Subtask 1.4.2 sns.violinplot( data=salary_df[salary_df['Empl Class Code']=='FA'], x="Sub Department", y="Annual Salary", hue="Sub Department", ) Let's make another violin plot. This time, let's compare academic departments for faculty (filter using ['Empl Class Code']=='FA'). There are many violins, so the axis labels will certainly overlap if not rotated. Rotate the x-labels 90 degrees. What other ways can I make this easier to understand in less than 5 seconds
'''

---

## 3. Think about Tasks 1.6 and 2.4. What questions did you want to answer with visualizations? Which two (or more) LLMs did you ask about visualizations? Choose one of the two Tasks, copy and paste the exact prompt(s) you used, and compare how the two responses differed — in code structure, library choices, plot aesthetics, or explanation style. What are your takeaways from the comparison?
If you want to dive deeper, try searching YouTube for videos comparing these models on coding tasks and note whether your experience agrees with what reviewers found.

**Answer:** This will be about Task 1.6. I used ChatGPT (free version, no extra thinking or code/data analysis tools included) and Claude Sonnet 4.6 using Medium thinking. I wanted to view the relationship between "Years in Job", "Pay Basis", and "Annual Salary". I wanted to see how "Years in Job" compared to "Annual Salary" based on "Pay Basis". I was targeting a linear regression scatter plot but did not ask for it specifically.

My first prompt was,
'''
In the attached data set I am interested in understanding the relationships between "Years in Job", "Pay Basis", and "Annual Salary".

You are an expert in data visualizations using Python, Pandas, Matplotlib, and Seaborn. For this you should use seaborn.

What type of visualization do you suggest to help answer my question?
'''

Claude provided one option saying the right visualizatin is a FacetGrid of scatter plots with regression lines using sns.lmplot(). ChatGPT actually gave me options from a generic scatter plot, scatter plot with regression lines, Faceted scatter plots (it recommended / marked as Excellent), and provided complementary plots.

My prompt limited their library choices so ChatGPT did not deviate from the ones I included in the prompt. Claude did include matplotlib.ticker so it did deviate from the prompt slightly.

In code structure Claude was much more detailed including everything needed and even expanded on how the plot looked by setting titles, labels, subtitle, and ticks. ChatGPT basically returned the sns.lmpplot() function only.

The returned plots were similar but Claude had a better looking plot.

For Task 2.4 I used Claude and Gemini with similar results, where Claude provided better results.

For this comparison Claude stands out as providing the best end result with the least amount of re-prompting or extra context.
---

## 4. Describe something you learned in this lesson that you may find useful in later work.

**Answer:** In this lesson I focused on using the Seaborn library because I haven't used it before. I wanted to understand how it was compared to Plotly. Using Seaborn was an intuitive and better looking plot than using generic panda plots. I didn't search for interactivity, but for statistical analysis and data exploration I found Seaborn to be an excellent library.