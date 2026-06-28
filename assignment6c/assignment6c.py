first_name = "Benjamin"
last_name = "Branta"


# Import Libraries
import pandas as pd

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

# Subtask 1.2: Select columns of interest
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
climate_df = climate_df_all[column_filter]

# Check
assert climate_df.shape == (709514, 10)


# Subtask 1.3.1: Convert Date
# I was not getting a warning and I wasn't getting the assign method to work.
# climate_df = climate_df.assign(climate_df["DATE"] = pd.to_datetime(climate_df["DATE"]))
climate_df["DATE"] = pd.to_datetime(climate_df["DATE"])

# Subtask 1.3.2: Remove spaces around strings
climate_df["REPORT_TYPE"] = climate_df["REPORT_TYPE"].str.strip()


# Subtask 1.3.3: Cleaning DailyMaximumDryBulbTemperature, DailyMinimumDryBulbTemperature
def temp_converter(t):
    if isinstance(t, str):
        return float(t.strip("s"))
    if isinstance(t, (int, float)):
        return float(t)
    return t


climate_df["DailyMaximumDryBulbTemperature"] = climate_df[
    "DailyMaximumDryBulbTemperature"
].map(temp_converter)

climate_df["DailyMinimumDryBulbTemperature"] = climate_df[
    "DailyMinimumDryBulbTemperature"
].map(temp_converter)


# Subtask 1.3.4: Cleaning DailyPrecipitation
def precip_converter(p):
    if isinstance(p, str):
        if "T" in p:
            return 0.0001
        return float(p.strip("s"))
    if isinstance(p, (int, float)):
        return float(p)
    return p


climate_df["DailyPrecipitation"] = climate_df["DailyPrecipitation"].map(
    precip_converter
)


# Subtask 1.3.5: Cleaning DailySnowDepth and DailySnowfall
climate_df["DailySnowDepth"] = climate_df["DailySnowDepth"].map(precip_converter)
climate_df["DailySnowfall"] = climate_df["DailySnowfall"].map(precip_converter)


# Subtask 1.3.6: Verification
climate_df["REPORT_TYPE"] = climate_df["REPORT_TYPE"].astype(object)
# climate_df.dtypes
