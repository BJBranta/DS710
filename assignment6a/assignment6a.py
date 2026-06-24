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


# Subtask 1.3 - Write some functions
# Subtask 1.3.1
# For a given department, what is the "working title" of the highest-paid person?
def title_highest_paid(df: pd.DataFrame, deptname: str) -> str:
    dept_df = df[df["Sub Department"] == deptname]
    highest_paid_working_title = dept_df.loc[dept_df["Annual Salary"].idxmax()][
        "Working Title"
    ]
    return str(highest_paid_working_title)


# Validate title_highest_paid
assert title_highest_paid(salary_df, "MATHEMATICS") == "PROFESSOR"
assert (
    title_highest_paid(salary_df.iloc[0:3], "ACADEMIC AFFAIRS")
    == "DIR MGMT, ANALYTICS, REPORTING"
)
assert (
    title_highest_paid(salary_df.iloc[100:105], "ALUMNI RELATIONS")
    == "ATHLETICS/CORP DEVELOP SPEC"
)


# Subtask 1.3.2
# For a given annual pay (a number), how many people make within a given range of that pay?
def num_ppl_within_pay(df: pd.DataFrame, target_pay: int, pay_range: int) -> int:
    min_val = target_pay - pay_range
    max_val = target_pay + pay_range
    return sum((df["Annual Salary"] >= min_val) & (df["Annual Salary"] <= max_val))


# Validate num_ppl_within_pay


# Subtask 1.3.3
# Which (sub) department has the most employees?
def largest_department(df: pd.DataFrame) -> str:
    largest_dept = df["Sub Department"].value_counts().idxmax()
    return str(largest_dept)


# Validate largest_department
assert largest_department(salary_df) == "INTERCOLLEGIATE ATHLETICS"
assert largest_department(salary_df.iloc[0:300]) == "ADVISING, RETEN & CAREER CNTR"


# Subtask 1.3.4
# Which (sub) department has the fewest employees? Return all of the department names as a series.
def smallest_department(df: pd.DataFrame) -> pd.Series:
    dept_employee_cnt = df["Sub Department"].value_counts()
    min_employees = dept_employee_cnt.min()
    dept_cnt_boolean_series = dept_employee_cnt == min_employees
    return dept_cnt_boolean_series[dept_cnt_boolean_series].index.to_series()


# Subtask 1.3.5
# What is the ratio of the higest paid employee's salary to that of the lowest paid employee?
def max_pay_ratio(df: pd.DataFrame) -> int:
    highest_paid = df["Annual Salary"].max()
    lowest_paid = df["Annual Salary"].min()
    return highest_paid / lowest_paid


# Validate max_pay_ratio
assert max_pay_ratio(salary_df) == 9.746381540781993
assert max_pay_ratio(salary_df.iloc[1000:]) == 5.145001117603857


# Task 2
# Subtask 2.1: Load the data
housing_master_df = pd.read_csv("HPI_master.csv")

# Subtask 2.2: Select the data
# Make a new variable housing_df, containing only the records in the set for which the "level" is "MSA", and "hpi_flavor" is "all-transactions".
housing_df = housing_master_df[
    (housing_master_df["level"] == "MSA")
    & (housing_master_df["hpi_flavor"] == "all-transactions")
]

# Validate housing_df has 62849 rows
assert housing_df.shape[0] == 62849


# Subtask 2.3: Functions for housing data
# Subtask 2.3.1
# For a given pair of a year and period (two integers in a tuple), which city / place had the highest price index (index_nsa)?
def place_with_highest_price(df: pd.DataFrame, time: tuple) -> str:
    yr, period = time
    yr_period_df = df[(df["yr"] == yr) & (df["period"] == period)]
    city_high_price_index = yr_period_df.loc[yr_period_df["index_nsa"].idxmax()][
        "place_name"
    ]
    return str(city_high_price_index)


# Validate place_with_highest_price
assert (
    place_with_highest_price(housing_df, (2022, 1))
    == "Austin-Round Rock-Georgetown, TX"
)


# Subtask 2.3.2
# For a given placename (string), in what (year,period) did the price index first go above a given price (float)?
def time_price_first_above(df: pd.DataFrame, place: str, price: float) -> tuple:
    matching = df[(df["place_name"] == place) & (df["index_nsa"] > price)]
    row = matching.loc[matching.index[0]]
    return (row["yr"], row["period"])


# Validate time_price_first_above
assert time_price_first_above(housing_df, "Orlando-Kissimmee-Sanford, FL", 200) == (
    2005,
    2,
)
assert time_price_first_above(housing_df, "Eau Claire, WI", 200) == (2016, 2)


# Subtask 2.3.3
# For a given placename (string) and a pair of years & periods (two pairs of integers), what was the price change ratio?
def price_ratio(df: pd.DataFrame, place: str, t1: tuple, t2: tuple) -> float:
    year_1, period_1 = t1
    year_2, period_2 = t2

    price_2_df = df[
        (df["place_name"] == place) & (df["yr"] == year_2) & (df["period"] == period_2)
    ]
    price_2 = price_2_df["index_nsa"].squeeze()

    price_1_df = df[
        (df["place_name"] == place) & (df["yr"] == year_1) & (df["period"] == period_1)
    ]
    price_1 = price_1_df["index_nsa"].squeeze()
    return price_2 / price_1


# Validate price_ration
# print(price_ratio(housing_df, "Kokomo, IN", (1999, 1), (2000, 3)))
# print(price_ratio(housing_df, "Eau Claire, WI", (2000, 1), (2020, 1)))
