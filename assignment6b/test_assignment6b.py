# Assignment 6b Unit Tests
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
# `pytest test_assignment6b.py`
#
# this set of unit tests requires packages:
# * `pytest`

#


###################
# begin checker
######################





###########
#
# first, a bunch of infrastructure to get everything lined up correctly
#
########

def default_code_filename():
    assignment_number = "6b" 
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




import pytest



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

# a function that finds files with the student's last name; robust to student testing and autograder
def find_files_student_name_and_ending(name, file_ending,allow_previous=False):
    return [file for file in find_files_with_ending(file_ending,allow_previous) if file.lower().startswith(name.lower())]


from pathlib import Path

def remove_file_if_exists(filename):
    Path(filename).unlink(missing_ok=True)


possible_generated_files = [
    'assign6b_task1-2.png',
    'assign6b_task1-3.png',
    'assign6b_task1-4-1.png',
    'assign6b_task1-4-2.png',
    'assign6b_task1-5.png',
    'assign6b_task1-6.png',
    'assign6b_task2-2-ec-li-bh-pmc.png',
    'assign6b_task2-2-WI.png',
    'assign6b_task2-3.png',
    'assign6b_task2-4.png',
    'assign6b_task3.html'
    ]


for p in possible_generated_files:
    found_files = find_files_with_ending(p)
    for f in found_files:
        remove_file_if_exists(f)












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






import numpy as np

@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask1SalaryPlots:

    def test_salary_df_shape(self, student_code):
        assert student_code.salary_df.shape == (1319, 10)

    def test_have_salary_vs_years_in_job(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name, 'assign6b_task1-2.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign6b_task1-2.png' and starts with your last name"

    def test_have_salary_vs_years_in_job_with_pay_basis(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name, 'assign6b_task1-3.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign6b_task1-3.png' and starts with your last name"

    def test_have_salary_pay_basis_violin(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name, 'assign6b_task1-4-1.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign6b_task1-4-1.png' and starts with your last name"

    def test_have_salary_sub_department(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name, 'assign6b_task1-4-2.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign6b_task1-4-2.png' and starts with your last name"

    def test_have_salary_pay_basis_hist_stacked(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name, 'assign6b_task1-5.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign6b_task1-5.png' and starts with your last name"

    def test_have_salary_new_plot(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name, 'assign6b_task1-6.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign6b_task1-6.png' and starts with your last name"










@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask2HousingPlots:
    def test_have_data(self, student_code):
        assert student_code.housing_df.shape == (62849, 10)

    def test_have_function_plot_price_for_places(self, student_code):
        assert callable(student_code.plot_price_for_places)

    def test_have_price_vs_time_ec_fc_sb_ra(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name, 'assign6b_task2-2-ec-li-bh-pmc.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign6b_task2-2-ec-li-bh-pmc.png' and starts with your last name"

    def test_have_price_vs_time_WI(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name, 'assign6b_task2-2-WI.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign6b_task2-2-WI.png' and starts with your last name"






    def test_have_function_plot_price_hist(self, student_code):
        assert callable(student_code.plot_price_hist)

    def test_have_price_histograms_2010q1_2020q1(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name, 'assign6b_task2-3.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign6b_task2-3.png' and starts with your last name"

    def test_have_housing_new_plot(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name, 'assign6b_task2-4.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign6b_task2-4.png' and starts with your last name"

