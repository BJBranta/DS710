first_name = "Benjamin"
last_name = "Branta"


# Import Libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Task 1: Reading and Cleaning Local Climatology Data
# Subtask 1.1: Load and merge local climate data from multiple files
climate_filenames = [
    "1950.csv",
    "1960.csv",
    "1970.csv",
    "1973.csv",
    "1980.csv",
    "1990.csv",
    "2000.csv",
    "2010.csv",
    "2020.csv",
]

climate_df_all = pd.DataFrame()
for filename in climate_filenames:
    df = pd.read_csv(filename, low_memory=False)
    climate_df_all = pd.concat([climate_df_all, df])

# Check
assert climate_df_all.shape == (709514, 124)


# Function for Task 1 data cleaning
def temp_converter(t):
    if isinstance(t, str):
        return float(t.strip("s"))
    if isinstance(t, (int, float)):
        return float(t)
    return t


# Function for Task 1 data cleaning
def precip_converter(p):
    if isinstance(p, str):
        if "T" in p:
            return 0.0001
        return float(p.strip("s"))
    if isinstance(p, (int, float)):
        return float(p)
    return p


# Column filter list
column_filter = [
    "STATION",
    "DATE",
    "REPORT_TYPE",
    "SOURCE",
    "DailyAverageWindSpeed",
    "DailyMaximumDryBulbTemperature",
    "DailyMinimumDryBulbTemperature",
    "DailyPrecipitation",
    "DailySnowDepth",
    "DailySnowfall",
]

# Subtask 1.2: Select columns of interest
# Subtask 1.3.1: Convert Date
# Subtask 1.3.2: Remove spaces around strings
# Subtask 1.3.3: Cleaning DailyMaximumDryBulbTemperature, DailyMinimumDryBulbTemperature
# Subtask 1.3.4: Cleaning DailyPrecipitation
# Subtask 1.3.5: Cleaning DailySnowDepth and DailySnowfall
# fmt: off
climate_df = (
    climate_df_all[column_filter]
    .assign(
        DATE=lambda climate_df_all: (
            pd.to_datetime(climate_df_all["DATE"])
        ),
        REPORT_TYPE=lambda climate_df_all: (
            climate_df_all["REPORT_TYPE"]
            .str.strip()      # remove whitespace
            .astype(object)   # set as object
        ),
        DailyMaximumDryBulbTemperature=lambda climate_df_all: (
            climate_df_all["DailyMaximumDryBulbTemperature"]
            .map(temp_converter)
        ),
        DailyMinimumDryBulbTemperature=lambda climate_df_all: (
            climate_df_all["DailyMinimumDryBulbTemperature"]
            .map(temp_converter)
        ),
        DailyPrecipitation=lambda climate_df_all: (
            climate_df_all["DailyPrecipitation"]
            .map(precip_converter)
        ),
        DailySnowDepth=lambda climate_df_all: (
            climate_df_all["DailySnowDepth"]
            .map(precip_converter)
        ),
        DailySnowfall=lambda climate_df_all: (
            climate_df_all["DailySnowfall"]
            .map(precip_converter)
        ),
    )
)
# fmt: on

# Subtask 1.3.6: Verification
assert climate_df.shape == (709514, 10)
# for v in climate_df['REPORT_TYPE'].unique():
#     print(f'"{v}"')
# climate_df.dtypes


# Task 2: Plots of Climate Data
# Subtask 2.1: Create daily_df
daily_df = climate_df[climate_df["REPORT_TYPE"] == "SOD"].reset_index(drop=True)

# Subtask 2.2: Plot daily snow depth
fig, ax = plt.subplots()
sns.lineplot(
    data=daily_df,
    x="DATE",
    y="DailySnowDepth",
    label="Daily Snow Depth",
    ax=ax,
)
ax.set_ylabel("Daily Snow Depth (Inches)")
ax.legend()
fig.savefig(
    f"{last_name}_{first_name}_assign6c_task2-1.png",
    dpi=300,
    bbox_inches="tight",
)


# Subtask 2.3: Plot max snow depth each year
# Subtask 2.3.1: Bin the dates into winters
def winter_bin(d: pd.Timestamp) -> int:
    month = d.month
    year = d.year
    if month >= 7:
        return year + 1
    return year


# fmt: off
daily_df = (
    daily_df
    .assign(
        WINTER=lambda daily_df: (
            daily_df["DATE"]
            .map(winter_bin)
        ),
    )
)
# fmt: on

# Checks
assert winter_bin(pd.to_datetime("1995-06-01 23:59:00")) == 1995
assert winter_bin(pd.to_datetime("1995-07-01 23:59:00")) == 1996

# Subtask 2.3.2: Compute max daily snowfall for each year
max_daily_snowfall = daily_df.pivot(columns=["WINTER"]).DailySnowDepth.max()

# Checks
assert max_daily_snowfall.shape == (27,)
assert max_daily_snowfall.loc[2019] == 25.0


# Subtask 2.3.3: Plot the max daily snowfall
fig, ax = plt.subplots()
sns.lineplot(
    data=max_daily_snowfall,  # pandas series
    ax=ax,
)
ax.set_ylabel("Max Daily Snowfall (Inches)")
fig.savefig(
    f"{last_name}_{first_name}_assign6c_task2-3.png",
    dpi=300,
    bbox_inches="tight",
)


# Subtask 2.4: Plotting total yearly precipitation
# Subtask 2.4.1: Bin observations into calendar years
# fmt: off
daily_df = (
    daily_df
    .assign(
        YEAR=lambda daily_df: (
            daily_df["DATE"]
            .dt.year
        ),
    )
)
# fmt: on

# Subtask 2.4.2: Sum the precipitations
yearly_precipitation = daily_df.pivot(columns=["YEAR"]).DailyPrecipitation.sum()

# Checks
assert round(yearly_precipitation.loc[1997], 4) == round(20.3245, 4)
assert round(yearly_precipitation.loc[1998], 4) == round(17.3732, 4)
assert yearly_precipitation.shape == (27,)


# Subtask 2.4.3: Plot total yearly precipitation
fig, ax = plt.subplots()
sns.barplot(
    data=yearly_precipitation,  # pandas series
    ax=ax,
)
ax.set_ylabel("Yearly Precipitation (Inches)")
ax.tick_params(axis="x", rotation=90)
fig.savefig(
    f"{last_name}_{first_name}_assign6c_task2-4.png",
    dpi=300,
    bbox_inches="tight",
)


# Subtask 3: Functions
def read_gdp_pdf(filename: str) -> str:
    import pypdf

    reader = pypdf.PdfReader(filename)
    raw_text = "\n".join(page.extract_text() for page in reader.pages)
    return raw_text


def get_percent_values(sentence):
    values = []
    tokens = sentence.split()
    for i, token in enumerate(tokens):
        if token.lower().rstrip(".,;:") == "percent" and i > 0:
            try:
                values.append(float(tokens[i - 1]))
            except ValueError:
                pass
    return values


def get_billion_values(sentence):
    values = []
    tokens = sentence.split()
    for i, token in enumerate(tokens):
        if token.lower().rstrip(".,;:") == "billion" and i > 0:
            try:
                values.append(float(tokens[i - 1].lstrip("$")))
            except ValueError:
                pass
    return values


def mentions_percent(sentence):
    tokens = sentence.split()
    for token in tokens:
        cleaned = token.lower().rstrip(".,;:")
        if cleaned == "percent" or cleaned == "%":
            return True
    return False


def split_sentences(text, min_length=20):
    """Split text on periods and return non-trivial fragments."""
    fragments = text.split(".")
    return [f.strip() for f in fragments if len(f.strip()) >= min_length]


def parse_narrative(raw_text: str) -> pd.DataFrame:

    HEADINGS = [
        "GDP by industry",
        "Related economic measures",
        "GDP by state",
        "Personal income by state",
        "Annual estimates",
        "Technical Notes",
    ]

    # Identify section chunks so heading_positions = [(index, heading), (index, heading)...]
    stop_index = len(raw_text)
    char_index = 0
    heading_positions = []
    for line in raw_text.splitlines():
        if line.strip() == "Related Interactive Data Tables":
            stop_index = char_index  # stop processing narrative text at start of page 9, store index for later
            break
        if line.strip() in HEADINGS:
            heading_positions.append((char_index, line.strip()))
        char_index += len(line) + 1

    # Process each chunk
    rows = []
    for i, (idx, heading) in enumerate(heading_positions):
        content_start = idx + len(heading)  # section start slice
        content_end = (
            heading_positions[i + 1][0]
            if i + 1 < len(heading_positions)
            else stop_index
        )  # section end slice

        chunk = raw_text[content_start:content_end]  # slice section chunk
        chunk = chunk.replace("U.S.", "US")  # edge case for sentence parser
        chunk = chunk.replace("9.1U.", "9.1U")  # edge case for sentence parser
        blob = " ".join(chunk.splitlines())
        sentences = split_sentences(blob)  # process section chunk into sentences

        # Process each sentence and append to list of dictionaries
        for sentence in sentences:
            rows.append(
                {
                    "section": heading,
                    "sentence": sentence,
                    "mentions_percent": mentions_percent(sentence),
                    "mentions_billion": "billion" in sentence,
                    "percent_values": get_percent_values(sentence),
                    "billion_values": get_billion_values(sentence),
                }
            )

    # Convert list of dictionaries to pandas dataframe
    narrative_df = pd.DataFrame(rows)
    return narrative_df


def parse_related_measures(raw_text):

    # Identify table measures in a list for searching
    measure_labels = [
        "Real GDP",
        "Current-dollar GDP",
        "Real final sales to private domestic purchasers",
        "Real GDI",
        "Average of real GDP and real GDI",
        "Gross domestic purchases price index",
        "PCE price index",
        "PCE price index excluding food and energy",
    ]

    # sort measure labels so my filter below tries longest measure first
    measure_labels = sorted(measure_labels, key=len, reverse=True)

    # Identify index for start and end of table
    table_begins_idx = raw_text.find("Real GDP and Related Measures")
    table_ends_idx = raw_text.rfind("U.S. Bureau of Economic Analysis")

    # Slice the document for the table, parse it line by line
    rows = []
    content_start = table_begins_idx + len(
        "Real GDP and Related Measures"
    )  # section start slice
    content_end = table_ends_idx
    chunk = raw_text[content_start:content_end]  # slice section chunk

    for line in chunk.splitlines():
        for measure in measure_labels:
            if measure in line:
                tokens = line.split()  # splits line into pieces by whitespace
                rows.append(
                    {
                        "measure": measure,  # measure captured
                        "advance_estimate": tokens[-3],  # 3rd from last in line
                        "second_estimate": tokens[-2],  # 2nd from last in line
                        "third_estimate": tokens[-1],  # last in line
                    }
                )
                break  # stop after the first (longest) match

    # create the measures DataFrame
    measures_df = (
        pd.DataFrame(rows)
        .replace("…", pd.NA)  # replace "..." with NA
        .assign(  # make the estimate columns numeric
            advance_estimate=lambda df: pd.to_numeric(df["advance_estimate"]),
            second_estimate=lambda df: pd.to_numeric(df["second_estimate"]),
            third_estimate=lambda df: pd.to_numeric(df["third_estimate"]),
        )
    )
    return measures_df


def gdp_summary(narrative_df, measures_df) -> dict:
    measures_df = measures_df.assign(
        revision=lambda df: df["third_estimate"] - df["second_estimate"]
    )

    gdp_summary = {
        "num_sentences": narrative_df.shape[0],
        "num_sentences_with_percent": sum(narrative_df["mentions_percent"]),
        "num_sentences_with_billion": sum(narrative_df["mentions_billion"]),
        "most_discussed_section": narrative_df["section"].value_counts().index[0],
        "real_gdp_third_estimate": measures_df[measures_df["measure"] == "Real GDP"][
            "third_estimate"
        ].squeeze(),
        "largest_downward_revision": measures_df.loc[
            measures_df["revision"].idxmin(), "measure"
        ],
    }
    return gdp_summary


def process_gdp(filename: str):
    raw_text = read_gdp_pdf(filename)
    narrative_df = parse_narrative(raw_text)
    measures_df = parse_related_measures(raw_text)
    narrative_df.to_csv("gdp_narrative.csv", index=False, na_rep="")
    measures_df.to_csv("gdp_measures.csv", index=False)
    return narrative_df, measures_df


if __name__ == "__main__":
    narrative_df, measures_df = process_gdp("assignment6c_data/gdp_report.pdf")
    print(gdp_summary(narrative_df, measures_df))
