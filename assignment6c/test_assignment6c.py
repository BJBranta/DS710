# Assignment 6c Unit Tests
# authors: silviana amethyst and Mckenzie West
#
# This checker is provided to DS710 students as a basic correctness check.

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


assignment_number = "6c"


def default_code_filename():
    return f"assignment{assignment_number}"


def checker_add_filename_extension(ext, name):
    if name.endswith(ext):
        return name
    if ext.startswith("."):
        return name + ext
    return name + "." + ext


with_dotpy = lambda name: checker_add_filename_extension("py", name)


student_code_filename = None

if len(sys.argv) > 2:
    for N in range(2, len(sys.argv)):
        argname = sys.argv[N]
        if argname.endswith(".py") and "test_" not in argname:
            student_code_filename = Path(argname).stem
            break

if not student_code_filename:
    student_code_filename = default_code_filename()


def student_code_exists():
    try:
        with open(with_dotpy(student_code_filename), "r", encoding="utf8"):
            return True
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"unable to read your code file to run unit tests. Ensure that your "
            f"code file is in the same folder as this checker, and that it's "
            f"called `{with_dotpy(default_code_filename())}`"
        ) from e


@pytest.fixture(scope="module")
def student_code():
    try:
        from importlib import import_module

        try:
            sys.modules.pop(student_code_filename)
            imported_student_code = import_module(student_code_filename)
        except Exception:
            imported_student_code = import_module(student_code_filename)
    except ImportError as e:
        raise ImportError(
            f"Bad import, or missing specified file {student_code_filename}. "
            f"Is your file named {student_code_filename}, and are you running "
            f"this checker from the same location as {student_code_filename}?"
        ) from e

    print(f"testing code from file `{with_dotpy(student_code_filename)}`")
    yield imported_student_code
    print("done with testing")


@pytest.fixture(scope="module")
def submitted_source_code_as_lines():
    with open(with_dotpy(student_code_filename), "r", encoding="utf8") as f:
        return f.readlines()


def find_files_with_ending(file_ending, allow_previous=False):
    found_files = []
    for f in os.listdir("."):
        if os.path.isfile(f) and f.endswith(file_ending):
            if allow_previous or not f.startswith("previous_"):
                found_files.append(f)
    return found_files

# a function that finds files ending with a certain name that start with the students last name -- 
# hopefully will ensure students use the correct naming scheme.
def find_files_student_name_and_ending(name, file_ending,allow_previous=False):
    return [file for file in find_files_with_ending(file_ending,allow_previous) if file.lower().startswith(name.lower())]


def remove_file_if_exists(filename):
    Path(filename).unlink(missing_ok=True)


possible_generated_files = [
    "assign6c_task2-1.png",
    "assign6c_task2-3.png",
    "assign6c_task2-4.png",
    "gdp_narrative.csv",
    "gdp_measures.csv",
]

for p in possible_generated_files:
    found_files = find_files_with_ending(p)
    for f in found_files:
        if not f.startswith(("solution", "solutions")):
            remove_file_if_exists(f)


if len(sys.argv) > 2:
    loc = student_code_filename.find(f"assignment{assignment_number}")
    canvas_filename_jargon = student_code_filename[:loc].split("_")
else:
    canvas_filename_jargon = [""]

assistive_grading_mode = canvas_filename_jargon != [""]


@pytest.fixture(scope="class", autouse=True)
def test_verify_no_breakpoints(submitted_source_code_as_lines):
    for line in submitted_source_code_as_lines:
        line_before_hash = line.split("#")[0]
        assert "breakpoint(" not in line_before_hash, (
            "Please remove breakpoints from your code before submitting."
        )


@pytest.fixture(scope="class", autouse=True)
def test_verify_no_hardcoded_paths(submitted_source_code_as_lines):
    import string

    for line in submitted_source_code_as_lines:
        line_before_hash = line.split("#")[0]
        for A in string.ascii_uppercase:
            assert not (A + ":/" in line_before_hash), (
                "In this class we do not accept the use of hardcoded paths. "
                "Remove the hardcoded path and try again."
            )
        assert "/Users" not in line_before_hash, (
            "In this class we do not accept the use of hardcoded paths."
        )
        assert "/Volumes" not in line_before_hash, (
            "In this class we do not accept the use of hardcoded paths."
        )


@pytest.fixture(scope="class", autouse=True)
def test_verify_no_global_keyword(submitted_source_code_as_lines):
    for line in submitted_source_code_as_lines:
        line_before_hash = line.split("#")[0]
        assert "global " not in line_before_hash, "Do not use the global keyword"


@pytest.fixture(scope="class", autouse=True)
def test_verify_no_input_function(submitted_source_code_as_lines):
    for line in submitted_source_code_as_lines:
        line_before_hash = line.split("#")[0]
        assert "input()" not in line_before_hash, "Do not use the `input()` function"


@pytest.fixture(scope="class", autouse=True)
def test_verify_no_dot_show(submitted_source_code_as_lines):
    for line in submitted_source_code_as_lines:
        line_before_hash = line.split("#")[0]
        assert ".show()" not in line_before_hash, (
            "Do not leave `.show()` in your submitted code; rely on file saving."
        )


@pytest.mark.skipif(
    not student_code_exists(),
    reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist",
)
class TestTask0:
    def test_has_first_last_name(self, student_code):
        assert isinstance(student_code.first_name, str)
        assert isinstance(student_code.last_name, str)


@pytest.mark.skipif(
    not student_code_exists(),
    reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist",
)
class TestTask1Reading:
    def test_climate_df_all_shape(self, student_code):
        assert student_code.climate_df_all.shape == (709514, 124)

    def test_climate_df_shape(self, student_code):
        assert student_code.climate_df.shape == (709514, 10)

    def test_climate_df_columns(self, student_code):
        climate_df = student_code.climate_df
        wanted_columns = [
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
        for c in wanted_columns:
            assert c in climate_df.columns


class TestTask1Cleaning:
    def test_have_temp_converter(self, student_code):
        assert callable(student_code.temp_converter)

    def test_temp_converter_floaty_string(self, student_code):
        assert student_code.temp_converter("0.14") == 0.14

    def test_temp_converter_string_with_s(self, student_code):
        assert student_code.temp_converter("0.14s") == 0.14

    def test_temp_converter_already_nan(self, student_code):
        assert np.isnan(student_code.temp_converter(np.nan))

    def test_have_precip_converter(self, student_code):
        assert callable(student_code.precip_converter)

    def test_precip_converter_trace(self, student_code):
        assert student_code.precip_converter("T") == 0.0001

    def test_precip_converter_already_nan(self, student_code):
        assert np.isnan(student_code.precip_converter(np.nan))


class TestTask2Plotting:
    def test_have_plot_daily_snow_depth(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name,'assign6c_task2-1.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign6c_task2-1.png' and starts with your last name."



    def test_have_function_winter_bin(self, student_code):
        assert callable(student_code.winter_bin)

    def test_winter_bin_years(self, student_code):
        assert student_code.winter_bin(pd.to_datetime("1995-06-01 23:59:00")) == 1995
        assert student_code.winter_bin(pd.to_datetime("1995-07-01 23:59:00")) == 1996

    def test_have_winter_column(self, student_code):
        assert "WINTER" in student_code.daily_df.columns

    def test_max_daily_snowfall_values(self, student_code):
        max_daily_snowfall = student_code.max_daily_snowfall
        assert max_daily_snowfall.shape == (27,)
        assert max_daily_snowfall.loc[2019] == 25.0

    def test_have_plot_max_daily_snowfall(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name,'assign6c_task2-3.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign6c_task2-3.png' and starts with your last name."


    def test_yearly_precipitation_values(self, student_code):
        yearly_precipitation = student_code.yearly_precipitation
        assert round(yearly_precipitation.loc[1997], 4) == round(20.3245, 4)
        assert round(yearly_precipitation.loc[1998], 4) == round(17.3732, 4)
        assert yearly_precipitation.shape == (27,)

    def test_have_plot_yearly_precipitation(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name,'assign6c_task2-4.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign6c_task2-4.png' and starts with your last name."


GDP_FILENAME = "assignment6c_data/gdp_report.pdf"


@pytest.fixture(scope="module")
def raw_gdp_text(student_code):
    return student_code.read_gdp_pdf(GDP_FILENAME)


@pytest.fixture(scope="module")
def narrative_df(raw_gdp_text, student_code):
    return student_code.parse_narrative(raw_gdp_text)


@pytest.fixture(scope="module")
def measures_df(raw_gdp_text, student_code):
    return student_code.parse_related_measures(raw_gdp_text)


@pytest.fixture(scope="module")
def process_gdp_result(student_code):
    return student_code.process_gdp(GDP_FILENAME)


@pytest.fixture(scope="module")
def gdp_summary_result(student_code, process_gdp_result):
    narrative_df, measures_df = process_gdp_result
    return student_code.gdp_summary(narrative_df, measures_df)


@pytest.mark.skipif(
    not student_code_exists(),
    reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist",
)
class TestTask3GDPFunctions:
    def test_have_read_gdp_pdf(self, student_code):
        assert callable(student_code.read_gdp_pdf)

    def test_have_process_gdp(self, student_code):
        assert callable(student_code.process_gdp)

    def test_have_parse_narrative(self, student_code):
        assert callable(student_code.parse_narrative)

    def test_have_parse_related_measures(self, student_code):
        assert callable(student_code.parse_related_measures)

    def test_have_gdp_summary(self, student_code):
        assert callable(student_code.gdp_summary)

    def test_verify_yes_if_name_is_main(self, submitted_source_code_as_lines):
        found_if_name_is_main = False
        for line in submitted_source_code_as_lines:
            line_before_hash = line.split("#")[0]
            if "if __name__ " in line_before_hash:
                found_if_name_is_main = True
        assert found_if_name_is_main, (
            'make sure to use the `if __name__ == "__main__"` construct'
        )


class TestTask3GDPText:
    def test_raw_text_is_string(self, raw_gdp_text):
        assert isinstance(raw_gdp_text, str)

    def test_raw_text_has_expected_content(self, raw_gdp_text):
        assert "Real GDP and Related Measures" in raw_gdp_text
        assert "GDP by industry" in raw_gdp_text
        assert "Technical Notes" in raw_gdp_text
        assert len(raw_gdp_text) > 10000


class TestTask3GDPNarrative:
    def test_narrative_df_exists(self, narrative_df):
        assert isinstance(narrative_df, pd.DataFrame)

    def test_narrative_df_columns(self, narrative_df):
        expected = [
            "section",
            "sentence",
            "mentions_percent",
            "percent_values",
            "mentions_billion",
            "billion_values",
        ]
        for c in expected:
            assert c in narrative_df.columns

    def test_narrative_df_sections(self, narrative_df):
        assert "GDP by industry" in narrative_df["section"].values
        assert "Annual estimates" in narrative_df["section"].values
        assert "Technical Notes" in narrative_df["section"].values

    def test_narrative_df_percent_and_billion_counts(self, narrative_df):
        assert narrative_df["mentions_percent"].sum() > 10
        assert narrative_df["mentions_billion"].sum() >= 3

    def test_narrative_value_columns_are_lists(self, narrative_df):
        assert narrative_df["percent_values"].map(type).eq(list).all()
        assert narrative_df["billion_values"].map(type).eq(list).all()


class TestTask3GDPMeasures:
    def test_measures_df_exists(self, measures_df):
        assert isinstance(measures_df, pd.DataFrame)
        assert not measures_df.empty

    def test_measures_df_columns(self, measures_df):
        expected = [
            "measure",
            "advance_estimate",
            "second_estimate",
            "third_estimate",
        ]
        for c in expected:
            assert c in measures_df.columns

    def test_real_gdp_row(self, measures_df):
        row = measures_df.loc[measures_df["measure"] == "Real GDP"].iloc[0]
        assert row["advance_estimate"] == 1.4
        assert row["second_estimate"] == 0.7
        assert row["third_estimate"] == 0.5

    def test_real_gdi_row(self, measures_df):
        row = measures_df.loc[measures_df["measure"] == "Real GDI"].iloc[0]
        assert pd.isna(row["advance_estimate"])
        assert pd.isna(row["second_estimate"])
        assert row["third_estimate"] == 2.6


class TestTask3GDPProcessAndSummary:
    def test_process_gdp_returns_two_dataframes(self, process_gdp_result):
        narrative_df, measures_df = process_gdp_result
        assert isinstance(narrative_df, pd.DataFrame)
        assert isinstance(measures_df, pd.DataFrame)

    def test_wrote_gdp_narrative_csv(self, process_gdp_result):
        assert os.path.exists("gdp_narrative.csv")

    def test_wrote_gdp_measures_csv(self, process_gdp_result):
        assert os.path.exists("gdp_measures.csv")

    def test_summary_keys(self, gdp_summary_result):
        expected = {
            "num_sentences",
            "num_sentences_with_percent",
            "num_sentences_with_billion",
            "most_discussed_section",
            "real_gdp_third_estimate",
            "largest_downward_revision",
        }
        assert expected.issubset(gdp_summary_result.keys())

    def test_summary_values(self, gdp_summary_result):
        assert gdp_summary_result["num_sentences_with_percent"] > 10
        assert gdp_summary_result["num_sentences_with_billion"] >= 3
        assert gdp_summary_result["real_gdp_third_estimate"] == 0.5
        assert gdp_summary_result["largest_downward_revision"] == "Current-dollar GDP"
