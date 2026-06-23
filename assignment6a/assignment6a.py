first_name = "Benjamin"
last_name = "Branta"

# Import Packages
import pandas as pd

# Task 1
# Subtask 1.1
# Load the data
salary_df = pd.read_excel("2021_Salary Statistics by Employee.xlsx")

# Subtask 1.2: Compute some basics
longest_years = salary_df["Years in Job"].max()
assert longest_years == 45.5041095890411

longest_years_name = salary_df.loc[salary_df["Years in Job"].idxmax()]["Name"]
assert longest_years_name == "PLOMEDAHL, YVONNE M"

longest_years_department = salary_df.loc[salary_df["Years in Job"].idxmax()][
    "Sub Department"
]
assert longest_years_department == "GEOGRAPHY & ANTHROPOLOGY"

longest_years_department_highest_salary = salary_df[
    salary_df["Sub Department"] == longest_years_department
]["Annual Salary"].max()
assert longest_years_department_highest_salary == 82468.0
