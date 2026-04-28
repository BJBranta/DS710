# Assignment 6a Unit Tests
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
# `pytest test_assignment6a.py`
#
# this set of unit tests requires packages:
# * `pytest`

#


###################
# begin checker
######################




import pandas as pd
import pytest



###########
#
# first, a bunch of infrastructure to get everything lined up correctly
#
########
assignment_number = "6a" 

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











from pathlib import Path

def remove_file_if_exists(filename):
    Path(filename).unlink(missing_ok=True)


possible_generated_files = []

for f in possible_generated_files:
    remove_file_if_exists(f)





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








# this suite is conditional on finding the code file specified.
#
# https://stackoverflow.com/questions/38966785/it-is-possible-to-skip-fail-test-in-setup-using-pytest

@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask1SalaryBasics:

    
    def test_salary_df_shape(self, student_code):
        assert student_code.salary_df.shape == (1319, 10)



    def test_longest_years_name_type(self, student_code):
        assert isinstance(student_code.longest_years_name,str)

    def test_longest_years_department_type(self, student_code):
        assert isinstance(student_code.longest_years_department,str)


    def test_longest_years_department_highest_salary_type(self, student_code):
        assert isinstance(student_code.longest_years_department_highest_salary,float)


    def test_longest_years_name_value(self, student_code):
        assert student_code.longest_years_name == "PLOMEDAHL, YVONNE M"

    def test_longest_years_department_value(self, student_code):
        assert student_code.longest_years_department == "GEOGRAPHY & ANTHROPOLOGY"


    def test_longest_years_department_highest_salary_value(self, student_code):
        assert student_code.longest_years_department_highest_salary == 82468.0






# this suite is conditional on finding the code file specified.
#
# https://stackoverflow.com/questions/38966785/it-is-possible-to-skip-fail-test-in-setup-using-pytest

@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask1SalaryFunctions:

    def test_have_required_function_title_highest_paid(self, student_code):
        assert callable(student_code.title_highest_paid)

    def test_title_highest_paid_values(self, student_code):
        title_highest_paid = student_code.title_highest_paid
        salary_df = student_code.salary_df

        assert title_highest_paid(salary_df, 'MATHEMATICS') == 'PROFESSOR'
        assert title_highest_paid(salary_df.iloc[0:3], 'ACADEMIC AFFAIRS') == 'DIR MGMT, ANALYTICS, REPORTING'
        assert title_highest_paid(salary_df.iloc[100:105], 'ALUMNI RELATIONS') == 'ATHLETICS/CORP DEVELOP SPEC'






    def test_have_required_function_num_ppl_within_pay(self, student_code):
        assert callable(student_code.num_ppl_within_pay)

    def test_num_ppl_within_pay_values(self, student_code):
        num_ppl_within_pay = student_code.num_ppl_within_pay
        salary_df = student_code.salary_df

        assert num_ppl_within_pay(salary_df, 42000, 1000) == 43
        assert num_ppl_within_pay(salary_df, 100000, 10000) == 74
        assert num_ppl_within_pay(salary_df, 300000, 50000) == 1
        assert num_ppl_within_pay(salary_df[salary_df['Sub Department']=='MUSIC AND THEATRE ARTS'], 100000, 10000) == 1


    def test_have_required_function_largest_department(self, student_code):
        assert callable(student_code.largest_department)


    def test_largest_department_values(self, student_code):
        largest_department = student_code.largest_department
        salary_df = student_code.salary_df

        assert largest_department(salary_df) == 'INTERCOLLEGIATE ATHLETICS'
        assert largest_department(salary_df.iloc[0:300]) == 'ADVISING, RETEN & CAREER CNTR'



    def test_have_required_function_smallest_department(self, student_code):
        assert callable(student_code.smallest_department)

    def test_smallest_department_values(self, student_code):
        smallest_department = student_code.smallest_department
        salary_df = student_code.salary_df


        assert (set(smallest_department(salary_df)) == set(['CAMPS & CONFERENCES', 'BARRON\\PSYCHOLOGY', 'UNIVERSITY SENATE', 'GOVERNMENTAL & COMMUN RELATION', 'STRATEGIC PLANNING', 'GRAD STUDIES/ACADEMIC AFFAIRS', 'BLUGOLD CARD OFFICE', 'BARRON\\HISTORY', 'BARRON COUNTY-ACADEMIC', 'SERVICE CENTER AND TICKETING', 'BARRON\\POLITICAL SCIENCE', 'BARRON\\KINESIOLOGY', 'BARRON\\PHYSICS', 'BARRON\\ACADEMIC SUPPORT', 'BARRON\\ART & DESIGN', 'BARRON\\BUILDING MAINTENANCE', 'BARRON\\CHEMISTRY & BIOCHEMSTRY', 'PARKING & TRANSPORTATION', 'LATIN AMER & LATINX STUDIES', 'BARRON\\COMM & JOURN', 'BARRON\\CONTINUING ED', 'LIBERAL STUDIES', 'BARRON\\FOUNDATION']))
        assert (set(smallest_department(salary_df.iloc[1000:])) == set(['SERVICE CENTER AND TICKETING', 'STRATEGIC PLANNING', 'PARKING & TRANSPORTATION', 'UNIVERSITY SENATE']))

        # assert smallest_department(salary_df) in ['BARRON COUNTY-ACADEMIC', 'BARRON\\ACADEMIC SUPPORT', 'BARRON\\ART & DESIGN', 'BARRON\\BUILDING MAINTENANCE', 'BARRON\\CHEMISTRY & BIOCHEMSTRY', 'BARRON\\COMM & JOURN', 'BARRON\\CONTINUING ED', 'BARRON\\FOUNDATION', 'BARRON\\HISTORY', 'BARRON\\KINESIOLOGY', 'BARRON\\PHYSICS', 'BARRON\\POLITICAL SCIENCE', 'BARRON\\PSYCHOLOGY', 'BLUGOLD CARD OFFICE', 'CAMPS & CONFERENCES', 'GOVERNMENTAL & COMMUN RELATION', 'GRAD STUDIES/ACADEMIC AFFAIRS', 'LATIN AMER & LATINX STUDIES', 'LIBERAL STUDIES', 'PARKING & TRANSPORTATION', 'SERVICE CENTER AND TICKETING', 'STRATEGIC PLANNING', 'UNIVERSITY SENATE']
        # assert smallest_department(salary_df.iloc[1000:]) in ['PARKING & TRANSPORTATION', 'SERVICE CENTER AND TICKETING', 'STRATEGIC PLANNING', 'UNIVERSITY SENATE']



    def test_have_required_function_max_pay_ratio(self, student_code):
        assert callable(student_code.max_pay_ratio)


    def test_max_pay_ratio_values(self, student_code):
        max_pay_ratio = student_code.max_pay_ratio
        salary_df = student_code.salary_df

        assert max_pay_ratio(salary_df) == 9.746381540781993
        assert max_pay_ratio(salary_df.iloc[1000:]) == 5.145001117603857









# this suite is conditional on finding the code file specified.
#
# https://stackoverflow.com/questions/38966785/it-is-possible-to-skip-fail-test-in-setup-using-pytest

@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask2HousingLoadAndSelect:
    def test_have_master_data(self, student_code):
        assert isinstance(student_code.housing_master_df, pd.DataFrame)

    def test_master_data_correct_shape(self, student_code):
        assert student_code.housing_master_df.shape == (118984, 10)


    def test_have_filtered_data(self, student_code):
        assert isinstance(student_code.housing_df, pd.DataFrame)

    def test_filtered_data_correct_shape(self, student_code):
        assert student_code.housing_df.shape == (62849, 10)






# this suite is conditional on finding the code file specified.
#
# https://stackoverflow.com/questions/38966785/it-is-possible-to-skip-fail-test-in-setup-using-pytest

@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask2HousingFunctions:


    def test_have_required_function_place_with_highest_price(self, student_code):
        assert callable(student_code.place_with_highest_price)


    def test_place_with_highest_price(self, student_code):
        housing_df = student_code.housing_df
        place_with_highest_price = student_code.place_with_highest_price

        assert place_with_highest_price(housing_df, (2022, 1)) == 'Austin-Round Rock-Georgetown, TX'
        assert place_with_highest_price(housing_df, (2015, 1)) == 'San Francisco-San Mateo-Redwood City, CA (MSAD)'
        assert place_with_highest_price(housing_df, (2000, 1)) == 'San Jose-Sunnyvale-Santa Clara, CA'
        assert place_with_highest_price(housing_df, (1990, 1)) == 'Los Angeles-Long Beach-Glendale, CA (MSAD)'




    def test_have_required_function_time_price_first_above(self, student_code):
        assert callable(student_code.time_price_first_above)

    def test_time_price_first_above(self, student_code):
        housing_df = student_code.housing_df
        time_price_first_above = student_code.time_price_first_above

        assert time_price_first_above(housing_df,'Orlando-Kissimmee-Sanford, FL', 200) == (2005, 2)
        assert time_price_first_above(housing_df,'Eau Claire, WI', 200) == (2016, 2)




    def test_have_required_function_price_ratio(self, student_code):
        assert callable(student_code.price_ratio)


    def test_price_ratio(self, student_code):
        housing_df = student_code.housing_df
        price_ratio = student_code.price_ratio

        assert price_ratio(housing_df,'Kokomo, IN',(1999, 1),(2000, 3)) == 1.045124439004488
        assert price_ratio(housing_df,'Eau Claire, WI',(2000, 1),(2020, 1)) == 1.8048886948930596




