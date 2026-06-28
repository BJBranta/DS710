# Assignment 6c Unit Tests
# authors: silviana amethyst and  Mckenzie West
#
#
# This set of unit tests is provided to you as a student in DS710,
# to have a check on whether your code for the assignment
# passes some basic checks for correctness.
#
# This file must be executed from the same path
# as the code it's checking
#
# Note that passing all tests in this checker does *not* imply that you will
# receive a perfect score on the assignment. 
# 
# Your code is still manually graded for both style and correctness.
# The checkers only provide a starting point for the grading process.
#
# Important note:
# The right way to invoke this set of unit tests is 
#
# `pytest test_assignment6c.py`
#
# this set of unit tests requires packages:
# * `pytest`

#


###################
# begin checker
######################




import pandas as pd
import pytest
import numpy as np


###########
#
# first, a bunch of infrastructure to get everything lined up correctly
#
########
assignment_number = "6c" 

def default_code_filename():
    return f"assignment{assignment_number}"


# some code to deal with filename extensions
def checker_add_filename_extension(ext,name):
    if name.endswith(ext):
        return name
    else:
        if ext.startswith('.'):
            return name+ext
        else:
            return name+"."+ext

with_dotpy = lambda name: checker_add_filename_extension('py',name)





# construct the expected filename
import sys

student_code_filename = None

if len(sys.argv)>2:

    for N in range(2,len(sys.argv)):
        argname = sys.argv[N]
        if argname.endswith('.py') and 'test_' not in argname:

            student_code_filename = argname[:-3] # strip off the `.py` with that there -3
            if student_code_filename.startswith('./'):
                student_code_filename = student_code_filename[2:]
            break

if not student_code_filename:
    student_code_filename = default_code_filename()


# a function that tells whether the indicated file actually exists
# used in conditional running of code below
def student_code_exists():

    try:
        with open(with_dotpy(student_code_filename), 'r', encoding='utf8') as f:
            return True
    except FileNotFoundError as e:
        raise FileNotFoundError(f"unable to read your code file to run unit tests.  Ensure that your code file is in the same folder as this checker, and that it's called `{with_dotpy(default_code_filename())}`")








# the following "fixture" allows us to pass the imported library
# to tests later, and refer to the contents in the tests

# the stuff before the `yield` is essentially the setup code
# and the stuff after the `yield` is the teardown.

# see https://stackoverflow.com/questions/26405380/how-do-i-correctly-setup-and-teardown-for-my-pytest-class-with-tests
@pytest.fixture(scope='module')
def student_code():

    # up here in this function is setup code
    try:
        from importlib import import_module, reload

        try: # first, we try to reload, and if it fails then we'll regular load.
            # it's possible (probable) that a student is running this in Spyder, in which case
            # the previous instance of their assignment is still loaded,
            # and we need to REload to overwrite things

            sys.modules.pop(student_code_filename) # delete from the modules list.  might trigger the `except`.
            imported_student_code = import_module(student_code_filename) # might also trigger the `except`.
        except:
            # unable to reload, so we'll just do a fresh import
            imported_student_code = import_module(student_code_filename)


    except ImportError:
        raise ImportError(f"Bad import, or missing specified file {student_code_filename}.  Is your file named {student_code_filename}, and are you running this checker from the same location as {student_code_filename}?")

    print(f"testing code from file `{with_dotpy(student_code_filename)}`")


    # imported_student_code = pytest.importorskip(student_code_filename, reason=f"unable to import your code from file named {student_code_filename}")
    yield imported_student_code


    # teardown code goes here
    print("done with testing")




@pytest.fixture(scope='module')
def submitted_source_code():
    with open(with_dotpy(student_code_filename), 'r', encoding='utf8') as f:
        return f.read()

@pytest.fixture(scope='module')
def submitted_source_code_as_lines():
    with open(with_dotpy(student_code_filename), 'r', encoding='utf8') as f:
        return f.readlines()







# a function that finds files ending with a certain name
def find_files_with_ending(file_ending,allow_previous=False):
    """ 
    returns a list of files that end with a given string
    """
    import os
    found_files = []
    for f in os.listdir('.'):
        if os.path.isfile(f) and f.endswith(file_ending):
            if allow_previous or not f.startswith('previous_'):
                found_files.append(f)

    return found_files

# a function that finds files ending with a certain name that start with the students last name -- 
# hopefully will ensure students use the correct naming scheme.
def find_files_student_name_and_ending(name, file_ending,allow_previous=False):
    return [file for file in find_files_with_ending(file_ending,allow_previous) if file.lower().startswith(name.lower())]


from pathlib import Path

def remove_file_if_exists(filename):
    Path(filename).unlink(missing_ok=True)


possible_generated_files = [
    'assign6c_task2-1.png',
	'assign6c_task2-3.png',
	'assign6c_task2-4.png']


for p in possible_generated_files:
    found_files = find_files_with_ending(p)
    for f in found_files:
        remove_file_if_exists(f)





###
#
#  this next block is so that the unit tests can run on a truncated data set when doing assistive grading.
#
##  


# Make this prettier
if len(sys.argv)>2:
    loc = student_code_filename.find(f"assignment{assignment_number}")
    canvas_filename_jargon = student_code_filename[:loc].split('_')
else:
    canvas_filename_jargon = [""]



# This assignment requires a very large text file.
# For auto-grading we're going to use a truncated one.


import os

if canvas_filename_jargon != [""]:
    assistive_grading_mode = True
else:
    assistive_grading_mode = False













############
#
# begin actual tests!!!!!!!!!!!!
#
#############



# universal tests


@pytest.fixture(scope='class',autouse=True)
def test_verify_no_re(submitted_source_code_as_lines):

    for line in submitted_source_code_as_lines:
        line_before_hash = line.split('#')[0]

        student_imported_re = False
        if "import re" in line_before_hash:
            import string
            loc = line_before_hash.find("import re")
            next_char = line_before_hash[loc+len("import re")]
            if next_char in string.whitespace:
                student_imported_re = True
                break

        if "from re import" in line_before_hash:
            student_imported_re = True
            break
        
        if "regex=True" in line_before_hash:
            student_imported_re = True
            break

    assert not student_imported_re, "It looks like you imported the regular expression library.  In this course, we do not allow the use of regular expressions."



@pytest.fixture(scope='class',autouse=True)
def test_verify_no_breakpoints(submitted_source_code_as_lines):
    '''Verifies that the student does not use a `breakpoint` which would stop the checker in its tracks.
    '''

    for line in submitted_source_code_as_lines:
        line_before_hash = line.split('#')[0]

        assert not ("breakpoint(" in line_before_hash) , "Please remove breakpoints from your code before submitting."


@pytest.fixture(scope='class',autouse=True)
def test_verify_no_hardcoded_paths(submitted_source_code_as_lines):
    '''
    Verifies the student does not use hardcoded paths in their submission, as they will not work on our computers.
    
    Here we verify that you are not including global paths to file locations.
    Note that this test will fail even if the line is commented.
    Make sure to delete all referenes to global paths before submitting.
    '''

    import string

    for line in submitted_source_code_as_lines:
        line_before_hash = line.split('#')[0]
        
        for A in string.ascii_uppercase:
            assert not (A+":/" in line_before_hash), "In this class we do not accept the use of hardcoded paths.  remove the hardcoded path and try again.  most tests were skipped until this issue is corrected."
        assert not ("/Users" in line_before_hash), "In this class we do not accept the use of hardcoded paths.  remove the hardcoded path and try again.  most tests were skipped until this issue is corrected."
        assert not ("/Volumes" in line_before_hash), "In this class we do not accept the use of hardcoded paths.  remove the hardcoded path and try again.  most tests were skipped until this issue is corrected."



@pytest.fixture(scope='class',autouse=True)
def test_verify_no_global_keyword(submitted_source_code_as_lines):
    '''
    Verifies that the student does not use `global`, which has the potential to break the checkers.
    '''
    for line in submitted_source_code_as_lines:
        line_before_hash = line.split('#')[0]

        assert not ("global " in line_before_hash), "Do not use the global keyword"


@pytest.fixture(scope='class',autouse=True)
def test_verify_no_input_function(submitted_source_code_as_lines):
    '''
    Verifies that the student does not use `input()`, which breaks computer-assisted grading.
    '''
    for line in submitted_source_code_as_lines:
        line_before_hash = line.split('#')[0]

        assert not ("input()" in line_before_hash), "Do not use the `input()` function"

@pytest.fixture(scope='class',autouse=True)
def test_verify_no_dot_show(submitted_source_code_as_lines):
    '''
    Verifies that the student does not use `input()`, which breaks computer-assisted grading.
    '''
    for line in submitted_source_code_as_lines:
        line_before_hash = line.split('#')[0]

        assert not (".show()" in line_before_hash), "Do not leave `.show()` in your submitted code; we will reject it.  rely on file saving instead of .show()"







@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask0:


    def test_has_first_last_name(self, student_code):
        '''
        checks if you have the variables `first_name` and `last_name`.
        it cannot possibly check if these are defined correctly,
        just that they are both strings.
        '''

        assert isinstance(student_code.first_name, str) and "please define the variable `first_name` in your source code"
        assert isinstance(student_code.last_name, str) and "please define the variable `last_name` in your source code"




















# task 1 tests


# this suite is conditional on finding the code file specified.
#
# https://stackoverflow.com/questions/38966785/it-is-possible-to-skip-fail-test-in-setup-using-pytest
@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask1Reading:

    def test_climate_df_all_shape(self, student_code):
        assert student_code.climate_df_all.shape==(709514, 124)

    def test_climate_df_shape(self, student_code):
        assert student_code.climate_df.shape==(709514, 10)

    def test_climate_df_columns(self, student_code):
        climate_df = student_code.climate_df

        wanted_columns = ['STATION', 'DATE', 'REPORT_TYPE', 'SOURCE', 'DailyAverageWindSpeed', 'DailyMaximumDryBulbTemperature', 'DailyMinimumDryBulbTemperature', 'DailyPrecipitation','DailySnowDepth','DailySnowfall']

        for c in wanted_columns:
            assert c in climate_df.columns





class TestTask1Cleaning:

    def test_have_temp_converter(self, student_code):
        assert callable(student_code.temp_converter)


    def test_temp_converter_floaty_string(self, student_code):
        temp_converter = student_code.temp_converter
        assert temp_converter('0.14') == 0.14


    def test_temp_converter_string_with_s(self, student_code):
        temp_converter = student_code.temp_converter
        assert temp_converter('0.14s') == 0.14


    def test_temp_converter_already_float(self, student_code):
        temp_converter = student_code.temp_converter
        assert temp_converter(0.14) == 0.14


    def test_temp_converter_inty_string(self, student_code):
        temp_converter = student_code.temp_converter
        assert isinstance(temp_converter('1'), float)
        assert temp_converter('1') == 1.0

    def test_temp_converter_already_nan(self, student_code):
        temp_converter = student_code.temp_converter
        assert np.isnan(temp_converter(np.nan))



    def test_have_precip_converter(self, student_code):
        assert callable(student_code.precip_converter)

    def test_precip_converter_floaty_string(self, student_code):
        precip_converter = student_code.precip_converter
        assert precip_converter('0.14') == 0.14

    def test_precip_converter_floaty_string_with_s(self, student_code):
        precip_converter = student_code.precip_converter
        assert precip_converter('0.14s') == 0.14

    def test_precip_converter_trace(self, student_code):
        precip_converter = student_code.precip_converter
        assert precip_converter('T') == 0.0001


    def test_precip_converter_already_float(self, student_code):
        precip_converter = student_code.precip_converter
        assert precip_converter(0.14) == 0.14

    def test_precip_converter_inty_string_is_float(self, student_code):
        precip_converter = student_code.precip_converter
        assert isinstance(precip_converter('1'), float)

    def test_precip_converter_already_nan(self, student_code):
        precip_converter = student_code.precip_converter
        assert np.isnan(precip_converter(np.nan))




class TestTask2Plotting:


    def test_have_plot_daily_snow_depth(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name,'assign6c_task2-1.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign6c_task2-1.png' and starts with your last name."



    def test_have_function_winter_bin(self, student_code):
        assert callable(student_code.winter_bin)



    def test_winter_bin_years(self, student_code):
        winter_bin = student_code.winter_bin
        assert winter_bin(pd.to_datetime('1995-06-01 23:59:00')) == 1995
        assert winter_bin(pd.to_datetime('1995-07-01 23:59:00')) == 1996


    def test_have_winter_column(self, student_code):
        daily_df = student_code.daily_df

        assert 'WINTER' in daily_df.columns




    def test_have_max_daily_snowfall(self, student_code):
        assert isinstance(student_code.max_daily_snowfall,pd.Series)


    def test_max_daily_snowfall_values(self, student_code):
        max_daily_snowfall = student_code.max_daily_snowfall

        assert max_daily_snowfall.shape != (26,) and "Does your winter_bin function correctly on the month of January?  If 1996 is missing, check that."

        assert max_daily_snowfall.shape == (27,)
        assert max_daily_snowfall.loc[2019] == 25.0


    def test_have_plot_max_daily_snowfall(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name,'assign6c_task2-3.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign6c_task2-3.png' and starts with your last name."


    def test_yearly_precipitation_values(self, student_code):
        yearly_precipitation = student_code.yearly_precipitation

        assert round(yearly_precipitation.loc[1997],4) == round(20.3245,4)
        assert round(yearly_precipitation.loc[1998],4) == round(17.3732,4)
        assert yearly_precipitation.shape == (27,)

    def test_have_plot_yearly_precipitation(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name,'assign6c_task2-4.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign6c_task2-4.png' and starts with your last name."

















# task 3 tests



@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask3HaveFunctions:

    def test_have_read_fine_foods(self, student_code):
        assert callable(student_code.read_fine_foods)

    def test_read_fine_foods_excerpts(self, student_code):
        read_fine_foods = student_code.read_fine_foods
        
        amazon_df = read_fine_foods('finefoods_excerpts.txt') # this should succeed

        assert amazon_df.shape[0] == 9883



    def test_have_process_foods(self, student_code):
        assert callable(student_code.process_foods)

    def test_have_analyze_by_product(self, student_code):
        assert callable(student_code.analyze_by_product)

    def test_have_summary_stats(self, student_code):
        assert callable(student_code.summary_stats)


    def test_verify_yes_if_name_is_main(self, submitted_source_code_as_lines):
        '''
        Verifies that the student does not use `input()`, which breaks computer-assisted grading.
        '''
        found_if_name_is_main = False

        for line in submitted_source_code_as_lines:
            line_before_hash = line.split('#')[0]

            if "if __name__ " in line_before_hash:
                found_if_name_is_main = True

        assert found_if_name_is_main, 'make sure to use the `if __name__ == "__main__" construct as described in Subtask 1.2'






# modules for the next class of unit tests

@pytest.fixture(scope='module')
def process_foods_result_excerpts(student_code):
    return student_code.process_foods("finefoods_excerpts.txt")

@pytest.fixture(scope='module')
def amazon_df_excerpts(process_foods_result_excerpts):
    return process_foods_result_excerpts[0]

@pytest.fixture(scope='module')
def product_df_excerpts(process_foods_result_excerpts):
    return process_foods_result_excerpts[1]

@pytest.fixture(scope='module')
def summary_stats_excerpts(student_code,amazon_df_excerpts):
    return student_code.summary_stats(amazon_df_excerpts)






@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask3FineFoodsExcerpts:


        

    def test_have_amazon_df(self,amazon_df_excerpts):
        '''
        Verifies the existence of a pandas dataframe called `amazon_reviews`.
        '''
        assert isinstance(amazon_df_excerpts, pd.DataFrame)

    def test_amazon_df_num_rows(self,amazon_df_excerpts):
        '''
        Verifies that the number of amazon reviews that the student collected is within a certain range. 
        '''
        amazon_df = amazon_df_excerpts

        assert amazon_df.shape[0] > 9882 and "Your data frame is missing entries!"
        assert amazon_df.shape[0] < 9884 and "Your data frame has too many entries!"


    def test_amazon_df_required_column_names(self,amazon_df_excerpts):
        amazon_df = amazon_df_excerpts

        assert "productId" in amazon_df.columns
        assert "userId" in amazon_df.columns
        assert "profileName" in amazon_df.columns
        assert "helpfulness" in amazon_df.columns
        assert "score" in amazon_df.columns
        assert "time" in amazon_df.columns
        assert "summary" in amazon_df.columns
        assert "text" in amazon_df.columns
        assert "numVotesHelpful" in amazon_df.columns
        assert "numVotesTotal" in amazon_df.columns
        assert "reviewHelpfulnessScore" in amazon_df.columns
        assert "reviewLength" in amazon_df.columns
        assert "hasColonInText" in amazon_df.columns

        
    def test_amazon_df_column_types(self, amazon_df_excerpts):
        amazon_df = amazon_df_excerpts

        assert amazon_df["productId"].dtype == 'O'
        assert amazon_df["userId"].dtype == 'O'
        assert amazon_df["profileName"].dtype == 'O'
        assert amazon_df["helpfulness"].dtype == 'O'
        assert amazon_df["score"].dtype == 'float64'
        assert amazon_df["time"].dtype in ['O','datetime64']
        assert amazon_df["summary"].dtype == 'O'
        assert amazon_df["text"].dtype == 'O'
        assert amazon_df["numVotesHelpful"].dtype == 'int64'
        assert amazon_df["numVotesTotal"].dtype == 'int64'
        assert amazon_df["reviewHelpfulnessScore"].dtype == 'float64'
        assert amazon_df["reviewLength"].dtype == 'int64'
        assert amazon_df["hasColonInText"].dtype == 'bool'


    def test_amazon_df_last_review_not_empty(self,amazon_df_excerpts):
        """
        assures the last review isn't empty. this is a common symptom of splitting on a marker, when the marker occurs at the end of a string.
        """

        amazon_df = amazon_df_excerpts

        import numpy as np
        assert  not( np.all(amazon_df.iloc[-1] == "") or np.all(amazon_df.iloc[-1].isna()) ) 


    def test_amazon_df_index_type(self, amazon_df_excerpts):
        amazon_df = amazon_df_excerpts

        assert amazon_df.index.dtype == 'int64'

    def test_amazon_df_row_0(self, amazon_df_excerpts):
        """
        checks the values of entries for the 0th row of amazon_df
        """

        amazon_df = amazon_df_excerpts

        assert amazon_df["productId"].iloc[0] == 'B001E4KFG0'
        assert amazon_df["userId"].iloc[0] == 'A3SGXH7AUHU8GW'
        assert amazon_df["profileName"].iloc[0] == 'delmartian'
        assert amazon_df["helpfulness"].iloc[0] == '1/1'
        assert amazon_df["score"].iloc[0] == 5.0
        assert amazon_df["time"].iloc[0] == '1303862400'
        assert amazon_df["summary"].iloc[0] == 'Good Quality Dog Food'
        assert amazon_df["text"].iloc[0] == 'I have bought several of the Vitality canned dog food products and have found them all to be of good quality. The product looks more like a stew than a processed meat and it smells better. My Labrador is finicky and she appreciates this product better than  most.'
        assert amazon_df["numVotesHelpful"].iloc[0] == 1
        assert amazon_df["numVotesTotal"].iloc[0] == 1
        assert amazon_df["reviewHelpfulnessScore"].iloc[0] == 1.0
        assert amazon_df["reviewLength"].iloc[0] == 263
        assert amazon_df["hasColonInText"].iloc[0] == False

    def test_amazon_df_row_5(self, amazon_df_excerpts):
        """
        checks the values of entries for the 5th row of amazon_df
        """
        
        amazon_df = amazon_df_excerpts

        assert amazon_df["productId"].iloc[5] == 'B006K2ZZ7K'
        assert amazon_df["userId"].iloc[5] == 'ADT0SRK1MGOEU'
        assert amazon_df["profileName"].iloc[5] == 'Twoapennything'
        assert amazon_df["helpfulness"].iloc[5] == '0/0'
        assert amazon_df["score"].iloc[5] == 4.0
        assert amazon_df["time"].iloc[5] == '1342051200'
        assert amazon_df["summary"].iloc[5] == 'Nice Taffy'
        assert amazon_df["text"].iloc[5] == 'I got a wild hair for taffy and ordered this five pound bag. The taffy was all very enjoyable with many flavors: watermelon, root beer, melon, peppermint, grape, etc. My only complaint is there was a bit too much red/black licorice-flavored pieces (just not my particular favorites). Between me, my kids, and my husband, this lasted only two weeks! I would recommend this brand of taffy -- it was a delightful treat.'
        assert amazon_df["numVotesHelpful"].iloc[5] == 0
        assert amazon_df["numVotesTotal"].iloc[5] == 0
        assert pd.isna(amazon_df["reviewHelpfulnessScore"].iloc[5])
        assert amazon_df["reviewLength"].iloc[5] == 416
        assert amazon_df["hasColonInText"].iloc[5] == True


    def test_amazon_df_row_10(self, amazon_df_excerpts):
        """
        checks the values of entries for the 10th row of amazon_df
        """
        
        amazon_df = amazon_df_excerpts

        assert amazon_df["productId"].iloc[10] == 'B0001PB9FE'
        assert amazon_df["userId"].iloc[10] == 'A3HDKO7OW0QNK4'
        assert amazon_df["profileName"].iloc[10] == 'Canadian Fan'
        assert amazon_df["helpfulness"].iloc[10] == '1/1'
        assert amazon_df["score"].iloc[10] == 5.0
        assert amazon_df["time"].iloc[10] == '1107820800'
        assert amazon_df["summary"].iloc[10] == 'The Best Hot Sauce in the World'
        assert amazon_df["text"].iloc[10] == "I don't know if it's the cactus or the tequila or just the unique combination of ingredients, but the flavour of this hot sauce makes it one of a kind!  We picked up a bottle once on a trip we were on and brought it back home with us and were totally blown away!  When we realized that we simply couldn't find it anywhere in our city we were bummed.<br /><br />Now, because of the magic of the internet, we have a case of the sauce and are ecstatic because of it.<br /><br />If you love hot sauce..I mean really love hot sauce, but don't want a sauce that tastelessly burns your throat, grab a bottle of Tequila Picante Gourmet de Inclan.  Just realize that once you taste it, you will never want to use any other sauce.<br /><br />Thank you for the personal, incredible service!"
        assert amazon_df["numVotesHelpful"].iloc[10] == 1
        assert amazon_df["numVotesTotal"].iloc[10] == 1
        assert amazon_df["reviewHelpfulnessScore"].iloc[10] == 1.0
        assert amazon_df["reviewLength"].iloc[10] == 779
        assert amazon_df["hasColonInText"].iloc[10] == False


    def test_amazon_df_row_20(self, amazon_df_excerpts):
        """
        checks the values of entries for the 20th row of amazon_df
        """
        
        amazon_df = amazon_df_excerpts

        assert amazon_df["productId"].iloc[20] == 'B001GVISJM'
        assert amazon_df["userId"].iloc[20] == 'A1WO0KGLPR5PV6'
        assert amazon_df["profileName"].iloc[20] == 'mom2emma'
        assert amazon_df["helpfulness"].iloc[20] == '0/0'
        assert amazon_df["score"].iloc[20] == 5.0
        assert amazon_df["time"].iloc[20] == '1313452800'
        assert amazon_df["summary"].iloc[20] == 'Always fresh'
        assert amazon_df["text"].iloc[20] == "My husband is a Twizzlers addict.  We've bought these many times from Amazon because we're government employees living overseas and can't get them in the country we are assigned to.  They've always been fresh and tasty, packed well and arrive in a timely manner."
        assert amazon_df["numVotesHelpful"].iloc[20] == 0
        assert amazon_df["numVotesTotal"].iloc[20] == 0
        assert pd.isna(amazon_df["reviewHelpfulnessScore"].iloc[20])
        assert amazon_df["reviewLength"].iloc[20] == 262
        assert amazon_df["hasColonInText"].iloc[20] == False



    def test_amazon_df_row_last(self, amazon_df_excerpts):
        """
        checks the values of entries for the last row (-1) of amazon_df
        """
        
        amazon_df = amazon_df_excerpts

        assert amazon_df["productId"].iloc[-1] == 'B0048IC328'
        assert amazon_df["userId"].iloc[-1] == 'A375ZA7IJH2ZGQ'
        assert amazon_df["profileName"].iloc[-1] == 'Jihan S.'
        assert amazon_df["helpfulness"].iloc[-1] == '3/7'
        assert amazon_df["score"].iloc[-1] == 2.0
        assert amazon_df["time"].iloc[-1] == '1317772800'
        assert amazon_df["summary"].iloc[-1] == "If you can't handle caffeine, this is not for you."
        assert amazon_df["text"].iloc[-1] == "Yes, it's probably healthier than 5-Hour Energy or Starbucks shots but if you're looking to avoid a caffeine overload, this is still not for you. Most energy drinks cannot be made w/ out a high dosage of caffeine. I believe the caffeine content of 1 Guayaki shot is 150 mL - probably lower than other un-healthy energy shot drinks but I believe most other people avoid the top brands b/c they contain too much caffeine and/or sugar. If you do not react well to caffeine, Guayaki is not a good buy either. I definitely feel an energy boost w/ 1 full Guayaki shot but not w/ out all the other caffeine side effects - irritability, nervousness, mood-swings. Caffeine overdose is why I stopped drinking coffee. But it looks even organic energy drinks are still not safe.<br /><br />Now you're NOT sensitive to caffeine, then it's a great buy. It's not loaded w/ sugar. The taste is easy and pleasant. It's not loaded w/ a bunch of chemicals like 5-Hour shots or Starbucks drinks. And the energy boost lasts for about 4 to 5 hours. Takes about 5 to 7 minutes to kick in but all this probably depends on your body/weight.<br /><br />Side note - if you want to feel energized during the day, have a protein drink first thing in the morning and stay away for heavy, fattening foods during the day that will make you feel sluggish and sleepy!"
        assert amazon_df["numVotesHelpful"].iloc[-1] == 3
        assert amazon_df["numVotesTotal"].iloc[-1] == 7
        assert amazon_df["reviewHelpfulnessScore"].iloc[-1] == 0.42857142857142855
        assert amazon_df["reviewLength"].iloc[-1] == 1333
        assert amazon_df["hasColonInText"].iloc[-1] == False




    def test_product_df_shape(self, product_df_excerpts):
        product_df = product_df_excerpts

        assert product_df.shape[0] == 1411
        assert product_df.shape[1] == 8

    def test_product_df_index_datatype(self, product_df_excerpts):
        product_df = product_df_excerpts
        assert product_df.index.dtype == 'O' and "the index for `product_df` should be 'O' for object (string)"

    def test_product_df_column_names(self, product_df_excerpts):
        product_df = product_df_excerpts

        assert "numReviews" in product_df.columns
        assert "averageScore" in product_df.columns
        assert "num1" in product_df.columns
        assert "num2" in product_df.columns
        assert "num3" in product_df.columns
        assert "num4" in product_df.columns
        assert "num5" in product_df.columns
        assert "recommendationScore" in product_df.columns

    def test_product_df_data_types(self, product_df_excerpts):
        product_df = product_df_excerpts
        
        assert product_df["numReviews"].dtype == 'int64'
        assert product_df["averageScore"].dtype == 'float64'
        assert product_df["num1"].dtype == 'int64'
        assert product_df["num2"].dtype == 'int64'
        assert product_df["num3"].dtype == 'int64'
        assert product_df["num4"].dtype == 'int64'
        assert product_df["num5"].dtype == 'int64'
        assert product_df["recommendationScore"].dtype == 'float64'

    def test_product_df_row_B000LR4HYW(self, product_df_excerpts):
        product_df = product_df_excerpts

        assert product_df["numReviews"]["B000LR4HYW"] == 1
        assert product_df["averageScore"]["B000LR4HYW"] == 4.0
        assert product_df["num1"]["B000LR4HYW"] == 0
        assert product_df["num2"]["B000LR4HYW"] == 0
        assert product_df["num3"]["B000LR4HYW"] == 0
        assert product_df["num4"]["B000LR4HYW"] == 1
        assert product_df["num5"]["B000LR4HYW"] == 0

        # there is no check on the value of the `recommendationScore`, as it's made-up

    def test_product_df_row_B006K2ZZ7K(self, product_df_excerpts):
        product_df = product_df_excerpts

        assert product_df["numReviews"]["B006K2ZZ7K"] == 4
        assert product_df["averageScore"]["B006K2ZZ7K"] == 4.75
        assert product_df["num1"]["B006K2ZZ7K"] == 0
        assert product_df["num2"]["B006K2ZZ7K"] == 0
        assert product_df["num3"]["B006K2ZZ7K"] == 0
        assert product_df["num4"]["B006K2ZZ7K"] == 1
        assert product_df["num5"]["B006K2ZZ7K"] == 3


        # there is no check on the value of the `recommendationScore`, as it's made-up


    def test_summary_num_reviews(self,summary_stats_excerpts):
        '''
        Verifies that the average review length is within a certain range. Note that this range changes while grading because a truncated review file is used.
        '''
        summary = summary_stats_excerpts

        assert summary["num_reviews"] > 9882
        assert summary["num_reviews"] < 9884


    def test_summary_avg_length(self,summary_stats_excerpts):
        '''
        Verifies that the average review length is within a certain range. Note that this range changes while grading because a truncated review file is used.
        '''
        summary = summary_stats_excerpts
        
        assert summary["avg_length"] > 414.4
        assert summary["avg_length"] < 414.5


    def test_summary_num_reviews_with_colon(self,summary_stats_excerpts):
        '''
        Verifies that the average review length is within a certain range. Note that this range changes while grading because a truncated review file is used.
        '''
        summary = summary_stats_excerpts

        assert summary["num_reviews_with_colon"] > 913
        assert summary["num_reviews_with_colon"] < 915


    def test_summary_most_reviewed(self,summary_stats_excerpts):
        '''
        Verifies that the average review length is within a certain range. Note that this range changes while grading because a truncated review file is used.
        '''
        summary = summary_stats_excerpts


        assert set(summary["most_reviewed_id"]) == {'B006N3IG4K', 'B003VXFK44'}
        assert summary["most_reviewed_id"].shape == (2,)
        assert summary["times_most_reviewed"] > 454
        assert summary["times_most_reviewed"] < 456


    def test_wrote_all_foods_reviews_csv(self,process_foods_result_excerpts):
        '''
        Looks for a csv called `all_foods_reviews.csv` that has been generated by the code submitted by the student.
        '''
        assert os.path.exists('all_foods_reviews.csv'), 'required output csv file `all_foods_reviews.csv` does not exist'



    def test_wrote_product_review_data_csv(self,process_foods_result_excerpts):
        '''
        Looks for a csv called `product_review_data.csv` that has been generated by the code submitted by the student.
        '''
        assert os.path.exists('product_review_data.csv'), 'required output csv file `product_review_data.csv` does not exist'





















@pytest.fixture(scope='module')
def process_foods_result_full_file(student_code):
    return student_code.process_foods("finefoods.txt")



@pytest.fixture(scope='module')
def amazon_df_full_file(process_foods_result_full_file):
    return process_foods_result_full_file[0]

@pytest.fixture(scope='module')
def product_df_full_file(process_foods_result_full_file):
    return process_foods_result_full_file[1]

@pytest.fixture(scope='module')
def summary_stats_full_file(student_code,amazon_df_full_file):
    return student_code.summary_stats(amazon_df_full_file)




@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
@pytest.mark.skipif(assistive_grading_mode, reason=f"in assistive grading mode, so not testing the entire file")
class TestTask3FineFoodsFullFile:


        


    def test_have_amazon_df(self,amazon_df_full_file):
        '''
        Verifies the existence of a pandas dataframe called `amazon_reviews`.
        '''
        assert isinstance(amazon_df_full_file, pd.DataFrame)

    def test_amazon_df_num_rows(self,amazon_df_full_file):
        '''
        Verifies that the number of amazon reviews that the student is collected is within a certain range. 
        '''
        amazon_df = amazon_df_full_file

        assert amazon_df.shape[0] > 568453 and "Your data frame is missing many entries!"
        assert amazon_df.shape[0] < 568455 and "Your data frame has too many many entries!"


    def test_amazon_df_required_column_names(self,amazon_df_full_file):
        amazon_df = amazon_df_full_file

        assert "productId" in amazon_df.columns
        assert "userId" in amazon_df.columns
        assert "profileName" in amazon_df.columns
        assert "helpfulness" in amazon_df.columns
        assert "score" in amazon_df.columns
        assert "time" in amazon_df.columns
        assert "summary" in amazon_df.columns
        assert "text" in amazon_df.columns
        assert "numVotesHelpful" in amazon_df.columns
        assert "numVotesTotal" in amazon_df.columns
        assert "reviewHelpfulnessScore" in amazon_df.columns
        assert "reviewLength" in amazon_df.columns
        assert "hasColonInText" in amazon_df.columns

        
    def test_amazon_df_column_types(self, amazon_df_full_file):
        amazon_df = amazon_df_full_file

        assert amazon_df["productId"].dtype == 'O'
        assert amazon_df["userId"].dtype == 'O'
        assert amazon_df["profileName"].dtype == 'O'
        assert amazon_df["helpfulness"].dtype == 'O'
        assert amazon_df["score"].dtype == 'float64'
        assert amazon_df["time"].dtype == 'O'
        assert amazon_df["summary"].dtype == 'O'
        assert amazon_df["text"].dtype == 'O'
        assert amazon_df["numVotesHelpful"].dtype == 'int64'
        assert amazon_df["numVotesTotal"].dtype == 'int64'
        assert amazon_df["reviewHelpfulnessScore"].dtype == 'float64'
        assert amazon_df["reviewLength"].dtype == 'int64'
        assert amazon_df["hasColonInText"].dtype == 'bool'


    def test_amazon_df_last_review_not_empty(self,amazon_df_full_file):
        """
        assures the last review isn't empty. this is a common symptom of splitting on a marker, when the marker occurs at the end of a string.
        """

        amazon_df = amazon_df_full_file

        import numpy as np
        assert  not( np.all(amazon_df.iloc[-1] == "") or np.all(amazon_df.iloc[-1].isna()) ) 


    def test_amazon_df_index_type(self, amazon_df_full_file):
        amazon_df = amazon_df_full_file

        assert amazon_df.index.dtype == 'int64'

    def test_amazon_df_row_0(self, amazon_df_full_file):
        """
        checks the values of entries for the 0th row of amazon_df
        """

        amazon_df = amazon_df_full_file

        assert amazon_df["productId"].iloc[0] == 'B001E4KFG0'
        assert amazon_df["userId"].iloc[0] == 'A3SGXH7AUHU8GW'
        assert amazon_df["profileName"].iloc[0] == 'delmartian'
        assert amazon_df["helpfulness"].iloc[0] == '1/1'
        assert amazon_df["score"].iloc[0] == 5.0
        assert amazon_df["time"].iloc[0] == '1303862400'
        assert amazon_df["summary"].iloc[0] == 'Good Quality Dog Food'
        assert amazon_df["text"].iloc[0] == 'I have bought several of the Vitality canned dog food products and have found them all to be of good quality. The product looks more like a stew than a processed meat and it smells better. My Labrador is finicky and she appreciates this product better than  most.'
        assert amazon_df["numVotesHelpful"].iloc[0] == 1
        assert amazon_df["numVotesTotal"].iloc[0] == 1
        assert amazon_df["reviewHelpfulnessScore"].iloc[0] == 1.0
        assert amazon_df["reviewLength"].iloc[0] == 263
        assert amazon_df["hasColonInText"].iloc[0] == False

    def test_amazon_df_row_5(self, amazon_df_full_file):
        """
        checks the values of entries for the 5th row of amazon_df
        """
        
        amazon_df = amazon_df_full_file

        assert amazon_df["productId"].iloc[5] == 'B006K2ZZ7K'
        assert amazon_df["userId"].iloc[5] == 'ADT0SRK1MGOEU'
        assert amazon_df["profileName"].iloc[5] == 'Twoapennything'
        assert amazon_df["helpfulness"].iloc[5] == '0/0'
        assert amazon_df["score"].iloc[5] == 4.0
        assert amazon_df["time"].iloc[5] == '1342051200'
        assert amazon_df["summary"].iloc[5] == 'Nice Taffy'
        assert amazon_df["text"].iloc[5] == 'I got a wild hair for taffy and ordered this five pound bag. The taffy was all very enjoyable with many flavors: watermelon, root beer, melon, peppermint, grape, etc. My only complaint is there was a bit too much red/black licorice-flavored pieces (just not my particular favorites). Between me, my kids, and my husband, this lasted only two weeks! I would recommend this brand of taffy -- it was a delightful treat.'
        assert amazon_df["numVotesHelpful"].iloc[5] == 0
        assert amazon_df["numVotesTotal"].iloc[5] == 0
        assert pd.isna(amazon_df["reviewHelpfulnessScore"].iloc[5])
        assert amazon_df["reviewLength"].iloc[5] == 416
        assert amazon_df["hasColonInText"].iloc[5] == True


    def test_amazon_df_row_10(self, amazon_df_full_file):
        """
        checks the values of entries for the 10th row of amazon_df
        """
        
        amazon_df = amazon_df_full_file

        assert amazon_df["productId"].iloc[10] == 'B0001PB9FE'
        assert amazon_df["userId"].iloc[10] == 'A3HDKO7OW0QNK4'
        assert amazon_df["profileName"].iloc[10] == 'Canadian Fan'
        assert amazon_df["helpfulness"].iloc[10] == '1/1'
        assert amazon_df["score"].iloc[10] == 5.0
        assert amazon_df["time"].iloc[10] == '1107820800'
        assert amazon_df["summary"].iloc[10] == 'The Best Hot Sauce in the World'
        assert amazon_df["text"].iloc[10] == "I don't know if it's the cactus or the tequila or just the unique combination of ingredients, but the flavour of this hot sauce makes it one of a kind!  We picked up a bottle once on a trip we were on and brought it back home with us and were totally blown away!  When we realized that we simply couldn't find it anywhere in our city we were bummed.<br /><br />Now, because of the magic of the internet, we have a case of the sauce and are ecstatic because of it.<br /><br />If you love hot sauce..I mean really love hot sauce, but don't want a sauce that tastelessly burns your throat, grab a bottle of Tequila Picante Gourmet de Inclan.  Just realize that once you taste it, you will never want to use any other sauce.<br /><br />Thank you for the personal, incredible service!"
        assert amazon_df["numVotesHelpful"].iloc[10] == 1
        assert amazon_df["numVotesTotal"].iloc[10] == 1
        assert amazon_df["reviewHelpfulnessScore"].iloc[10] == 1.0
        assert amazon_df["reviewLength"].iloc[10] == 779
        assert amazon_df["hasColonInText"].iloc[10] == False


    def test_amazon_df_row_20(self, amazon_df_full_file):
        """
        checks the values of entries for the 20th row of amazon_df
        """
        
        amazon_df = amazon_df_full_file

        assert amazon_df["productId"].iloc[20] == 'B001GVISJM'
        assert amazon_df["userId"].iloc[20] == 'A1WO0KGLPR5PV6'
        assert amazon_df["profileName"].iloc[20] == 'mom2emma'
        assert amazon_df["helpfulness"].iloc[20] == '0/0'
        assert amazon_df["score"].iloc[20] == 5.0
        assert amazon_df["time"].iloc[20] == '1313452800'
        assert amazon_df["summary"].iloc[20] == 'Always fresh'
        assert amazon_df["text"].iloc[20] == "My husband is a Twizzlers addict.  We've bought these many times from Amazon because we're government employees living overseas and can't get them in the country we are assigned to.  They've always been fresh and tasty, packed well and arrive in a timely manner."
        assert amazon_df["numVotesHelpful"].iloc[20] == 0
        assert amazon_df["numVotesTotal"].iloc[20] == 0
        assert pd.isna(amazon_df["reviewHelpfulnessScore"].iloc[20])
        assert amazon_df["reviewLength"].iloc[20] == 262
        assert amazon_df["hasColonInText"].iloc[20] == False


    def test_amazon_df_row_last(self, amazon_df_full_file):
        """
        checks the values of entries for the last row (-1) of amazon_df
        """
        
        amazon_df = amazon_df_full_file

        assert amazon_df["productId"].iloc[-1] == 'B001LR2CU2'
        assert amazon_df["userId"].iloc[-1] == 'A3LGQPJCZVL9UC'
        assert amazon_df["profileName"].iloc[-1] == 'srfell17'
        assert amazon_df["helpfulness"].iloc[-1] == '0/0'
        assert amazon_df["score"].iloc[-1] == 5.0
        assert amazon_df["time"].iloc[-1] == '1338422400'
        assert amazon_df["summary"].iloc[-1] == 'Great Honey'
        assert amazon_df["text"].iloc[-1] == 'I am very satisfied ,product is as advertised, I use it on cereal, with raw vinegar, and as a general sweetner.'
        assert amazon_df["numVotesHelpful"].iloc[-1] == 0
        assert amazon_df["numVotesTotal"].iloc[-1] == 0
        assert pd.isna(amazon_df["reviewHelpfulnessScore"].iloc[-1])
        assert amazon_df["reviewLength"].iloc[-1] == 111
        assert amazon_df["hasColonInText"].iloc[-1] == False





    def test_product_df_shape(self, product_df_full_file):
        product_df = product_df_full_file

        assert product_df.shape[0] == 74258
        assert product_df.shape[1] == 8

    def test_product_df_index_datatype(self, product_df_full_file):
        product_df = product_df_full_file
        assert product_df.index.dtype == 'O' and "the index for product_df should be O for object (string)"

    def test_product_df_column_names(self, product_df_full_file):
        product_df = product_df_full_file

        assert "numReviews" in product_df.columns
        assert "averageScore" in product_df.columns
        assert "num1" in product_df.columns
        assert "num2" in product_df.columns
        assert "num3" in product_df.columns
        assert "num4" in product_df.columns
        assert "num5" in product_df.columns
        assert "recommendationScore" in product_df.columns

    def test_product_df_data_types(self, product_df_full_file):
        product_df = product_df_full_file
        
        assert product_df["numReviews"].dtype == 'int64'
        assert product_df["averageScore"].dtype == 'float64'
        assert product_df["num1"].dtype == 'int64'
        assert product_df["num2"].dtype == 'int64'
        assert product_df["num3"].dtype == 'int64'
        assert product_df["num4"].dtype == 'int64'
        assert product_df["num5"].dtype == 'int64'
        assert product_df["recommendationScore"].dtype == 'float64'

    def test_product_df_row_B000LR4HYW(self, product_df_full_file):
        product_df = product_df_full_file

        assert product_df["numReviews"]["B000LR4HYW"] == 1
        assert product_df["averageScore"]["B000LR4HYW"] == 4.0
        assert product_df["num1"]["B000LR4HYW"] == 0
        assert product_df["num2"]["B000LR4HYW"] == 0
        assert product_df["num3"]["B000LR4HYW"] == 0
        assert product_df["num4"]["B000LR4HYW"] == 1
        assert product_df["num5"]["B000LR4HYW"] == 0

        # there is no check on the value of the `recommendationScore`, as it's made-up

    def test_product_df_row_B006K2ZZ7K(self, product_df_full_file):
        product_df = product_df_full_file

        assert product_df["numReviews"]["B006K2ZZ7K"] == 4
        assert product_df["averageScore"]["B006K2ZZ7K"] == 4.75
        assert product_df["num1"]["B006K2ZZ7K"] == 0
        assert product_df["num2"]["B006K2ZZ7K"] == 0
        assert product_df["num3"]["B006K2ZZ7K"] == 0
        assert product_df["num4"]["B006K2ZZ7K"] == 1
        assert product_df["num5"]["B006K2ZZ7K"] == 3

        # there is no check on the value of the `recommendationScore`, as it's made-up


    def test_summary_num_reviews(self,summary_stats_full_file):
        '''
        Verifies that the average review length is within a certain range. Note that this range changes while grading because a truncated review file is used.
        '''
        summary = summary_stats_full_file

        assert summary["num_reviews"] > 568453
        assert summary["num_reviews"] < 568455


    def test_summary_avg_length(self,summary_stats_full_file):
        '''
        Verifies that the average review length is within a certain range. Note that this range changes while grading because a truncated review file is used.
        '''
        summary = summary_stats_full_file
        
        assert summary["avg_length"] > 436.22
        assert summary["avg_length"] < 436.23


    def test_summary_num_reviews_with_colon(self,summary_stats_full_file):
        '''
        Verifies that the average review length is within a certain range. Note that this range changes while grading because a truncated review file is used.
        '''
        summary = summary_stats_full_file

        assert summary["num_reviews_with_colon"] > 54099
        assert summary["num_reviews_with_colon"] < 54101


    def test_summary_most_reviewed(self,summary_stats_full_file):
        '''
        Verifies that the average review length is within a certain range. Note that this range changes while grading because a truncated review file is used.
        '''
        summary = summary_stats_full_file

        
        assert (summary["most_reviewed_id"] == pd.Series(['B007JFMH8M'])).all()
        assert summary["times_most_reviewed"] > 912
        assert summary["times_most_reviewed"] < 914




    def test_wrote_all_foods_reviews_csv(self,process_foods_result_excerpts):
        '''
        Looks for a csv called `all_foods_reviews.csv` that has been submitted by the student.
        '''
        assert os.path.exists('all_foods_reviews.csv'), 'required output csv file `all_foods_reviews.csv` does not exist'



    def test_wrote_product_review_data_csv(self,process_foods_result_excerpts):
        '''
        Looks for a csv called `product_review_data.csv` that has been submitted by the student.
        '''
        assert os.path.exists('product_review_data.csv'), 'required output csv file `product_review_data.csv` does not exist'





