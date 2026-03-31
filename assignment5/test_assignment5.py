# Assignment 5 Unit Tests
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
# `pytest test_assignment5.py`
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
    assignment_number = "5" 
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




@pytest.fixture(scope='class')
def submitted_source_code():
    with open(with_dotpy(student_code_filename), 'r', encoding='utf8') as f:
        return f.read()

@pytest.fixture(scope='class')
def submitted_source_code_as_lines():
    with open(with_dotpy(student_code_filename), 'r', encoding='utf8') as f:
        return f.readlines()











from pathlib import Path

def remove_file_if_exists(filename):
    Path(filename).unlink(missing_ok=True)


possible_generated_files = [
    'assign5_task4.png',
    'assign5_task5.png',
    'assign5_task6_hist.png',
    'assign5_task6_line.png'
    ]

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

def find_files_student_name_and_ending(name, file_ending,allow_previous=False):
    return [file for file in find_files_with_ending(file_ending,allow_previous) if file.lower().startswith(name.lower())]


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


# this suite is conditional on finding the code file specified.
#
# https://stackoverflow.com/questions/38966785/it-is-possible-to-skip-fail-test-in-setup-using-pytest

@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask1HasZerosExact:


    def test_have_function(self, student_code):
        assert callable(student_code.has_zeros)


    def test_can_call(self, student_code):
        has_zeros = student_code.has_zeros
        has_zeros(np.zeros((5))) # try calling with a 1d array
        has_zeros(np.zeros((5,6))) # try calling with a 2d array
        # i opted not to do 3d arrays.  i hope you are using `np.any`...



    def test_example_1(self, student_code):
        has_zeros = student_code.has_zeros
        assert has_zeros(np.array([0,0,0,1,1,1,13,3,3,3])) == True

    def test_example_2(self, student_code):
        has_zeros = student_code.has_zeros
        assert has_zeros(np.array([[0,0,0],[1,1,1],[13,3,3]])) == True

    def test_example_3(self, student_code):
        has_zeros = student_code.has_zeros
        assert has_zeros(np.array([1,1,1,13,3,3,3])) == False

    def test_example_4(self, student_code):
        has_zeros = student_code.has_zeros
        assert has_zeros(np.array([[1,1,1],[13,3,3]])) == False

    def test_example_5(self, student_code):
        has_zeros = student_code.has_zeros
        assert has_zeros(np.array([0.000001, -0.000001])) == False

    def test_example_6(self, student_code):
        has_zeros = student_code.has_zeros
        assert has_zeros(np.array([[1,2,3,4],[1e-1, 1e-2, 1e-3, 1e-4]])) == False



# this suite is conditional on finding the code file specified.
#
# https://stackoverflow.com/questions/38966785/it-is-possible-to-skip-fail-test-in-setup-using-pytest

@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask1HasZerosApproximate:


    def test_have_function(self, student_code):
        assert callable(student_code.has_approximate_zeros)


    def test_can_call(self, student_code):
        has_approximate_zeros = student_code.has_approximate_zeros
        has_approximate_zeros(np.zeros((5)),1e-10) # try calling with a 1d array
        has_approximate_zeros(np.zeros((5,6)),1e-5) # try calling with a 2d array
        # i opted not to do 3d arrays.  i hope you are using `np.any`...



    def test_example_1(self, student_code):
        has_approximate_zeros = student_code.has_approximate_zeros
        assert has_approximate_zeros(np.array([0,0,1e-10,1,1,1,13,3,3,3]), 1e-7) == True

    def test_example_2(self, student_code):
        has_approximate_zeros = student_code.has_approximate_zeros
        assert has_approximate_zeros(np.array([[0,1e-10,1e-5],[1,1,1],[13,3,3]]), 1e-7) == True

    def test_example_3(self, student_code):
        has_approximate_zeros = student_code.has_approximate_zeros
        assert has_approximate_zeros(np.array([-1e-8,1,1,13,3,3,3]), 1e-7) == True

    def test_example_4(self, student_code):
        has_approximate_zeros = student_code.has_approximate_zeros
        assert has_approximate_zeros(np.array([[-2e-9,1,1],[13,3,3]]), 1e-9) == False

    def test_example_5(self, student_code):
        has_approximate_zeros = student_code.has_approximate_zeros
        assert has_approximate_zeros(np.array([0.000001, -0.000001]), 1e-10) == False

    def test_example_6(self, student_code):
        has_approximate_zeros = student_code.has_approximate_zeros
        assert has_approximate_zeros(np.array([[1,2,3,4],[1e-1, 1e-2, 1e-3, 1e-4]]), 1e-10) == False







# this suite is conditional on finding the code file specified.
#
# https://stackoverflow.com/questions/38966785/it-is-possible-to-skip-fail-test-in-setup-using-pytest

@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask2Primes:

    def test_have_function(self, student_code):
        assert callable(student_code.primes)


    def test_example_1(self, student_code):
        primes = student_code.primes
        assert np.all(primes(2,7) == np.array([2,3,5]))

    def test_example_2(self, student_code):
        primes = student_code.primes
        assert np.all(primes(2,8) == np.array([2,3,5,7]))

    def test_example_3(self, student_code):
        primes = student_code.primes
        assert np.all(primes(2,9) == np.array([2,3,5,7]))

    def test_example_4(self, student_code):
        primes = student_code.primes

        with pytest.raises(ValueError) as e_info:
            primes(-2,7) # should raise, -2 not allowed

    def test_example_5(self, student_code):
        primes = student_code.primes

        with pytest.raises(Exception) as e_info: # a generic exception.  i don't care what kind.
            primes(-1.5,7) # should raise, -1.5 not allowed











# this suite is conditional on finding the code file specified.
#
# https://stackoverflow.com/questions/38966785/it-is-possible-to-skip-fail-test-in-setup-using-pytest

@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask3ColumnStats:
    def test_have_function(self, student_code):
        assert callable(student_code.column_statistics)

    def test_can_call(self, student_code):
        column_statistics = student_code.column_statistics

        column_statistics(np.zeros((10,30)))
        column_statistics(np.ones((5,8)))
        column_statistics(np.random.uniform(size=(9,13)))

    def test_given_example(self, student_code):
        column_statistics = student_code.column_statistics

        arr = np.array([[1,0,3],[4,5,-1]])

        assert np.all(column_statistics(arr) == np.array([
                  [2.5,2.5,1],   # means of each column
                  [1,0,-1],      # min of each column
                  [4,5,3],       # max of each column
                  [0,1,0]        # number of zero entries
                ]))

    def test_random_4_5(self, student_code):
        column_statistics = student_code.column_statistics

        random_data_4_5 = np.array([
         [0.67422951, 0.38365935, 0.62041326, 0.00297396, 0.36025429],
         [0.8987696 , 0.71183167, 0.10001006, 0.23090831, 0.9758121 ],
         [0.98318505, 0.27235507, 0.21307811, 0.10396805, 0.41828476],
         [0.43248385, 0.46482787, 0.52397411, 0.59496885, 0.9486531 ]])

        expected_answer = np.array([[0.747167  , 0.45816849, 0.36436888, 0.23320479, 0.67575106],
            [0.43248385, 0.27235507, 0.10001006, 0.00297396, 0.36025429],
            [0.98318505, 0.71183167, 0.62041326, 0.59496885, 0.9758121 ],
            [0.        , 0.        , 0.        , 0.        , 0.        ]])


        assert np.all(np.isclose(column_statistics(random_data_4_5), expected_answer))

    def test_random_7_9(self, student_code):
        column_statistics = student_code.column_statistics

        random_data_7_9 = np.array([
             [0.0, 0.29411764705882354, 0.1764705882352941, 0.23529411764705882, 0.11764705882352941, 0.29411764705882354, 0.23529411764705882, 0.0, 0.058823529411764705],
             [0.0, 0.1764705882352941, 0.29411764705882354, 0.23529411764705882, 0.058823529411764705, 0.11764705882352941, 0.058823529411764705, 0.058823529411764705, 0.058823529411764705],
             [0.0, 0.29411764705882354, 0.23529411764705882, 0.11764705882352941, 0.11764705882352941, 0.1764705882352941, 0.0, 0.23529411764705882, 0.23529411764705882],
             [0.058823529411764705, 0.1764705882352941, 0.11764705882352941, 0.058823529411764705, 0.29411764705882354, 0.0, 0.058823529411764705, 0.23529411764705882, 0.1764705882352941],
             [0.11764705882352941, 0.23529411764705882, 0.1764705882352941, 0.058823529411764705, 0.23529411764705882, 0.0, 0.058823529411764705, 0.11764705882352941, 0.058823529411764705],
             [0.23529411764705882, 0.058823529411764705, 0.11764705882352941, 0.0, 0.29411764705882354, 0.058823529411764705, 0.058823529411764705, 0.0, 0.0],
             [0.29411764705882354, 0.1764705882352941, 0.23529411764705882, 0.23529411764705882, 0.29411764705882354, 0.1764705882352941, 0.0, 0.29411764705882354, 0.11764705882352941]
            ])

        expected_answer = np.array([
         [0.10084033613445377, 0.20168067226890757, 0.19327731092436976, 0.13445378151260504, 0.20168067226890757, 0.11764705882352941, 0.06722689075630253, 0.13445378151260504, 0.10084033613445377],
         [0.0, 0.058823529411764705, 0.11764705882352941, 0.0, 0.058823529411764705, 0.0, 0.0, 0.0, 0.0],
         [0.29411764705882354, 0.29411764705882354, 0.29411764705882354, 0.23529411764705882, 0.29411764705882354, 0.29411764705882354, 0.23529411764705882, 0.29411764705882354, 0.23529411764705882],
         [3.0, 0.0, 0.0, 1.0, 0.0, 2.0, 2.0, 2.0, 1.0]
        ])

        assert np.all(np.isclose(column_statistics(random_data_7_9), expected_answer))





# this suite is conditional on finding the code file specified.
#
# https://stackoverflow.com/questions/38966785/it-is-possible-to-skip-fail-test-in-setup-using-pytest

@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask4AlicePlot:



    def test_have_word_freqency(self, student_code):
        word_frequency = student_code.word_frequency

        assert isinstance(word_frequency, dict)

        assert word_frequency['a'] == 626
        assert word_frequency['abide'] == 1
        assert word_frequency['able'] == 1
        assert word_frequency['about'] == 94
        assert word_frequency['above'] == 3
        assert word_frequency['absence'] == 1

    def test_have_frequencies_unsorted(self, student_code):
        frequencies_unsorted = student_code.frequencies_unsorted

        assert isinstance(frequencies_unsorted,np.ndarray)

        assert frequencies_unsorted[0] == 626
        assert frequencies_unsorted[1] == 1
        assert frequencies_unsorted[2] == 1
        assert frequencies_unsorted[3] == 94
        



    def test_have_frequencies_sorted(self, student_code):
        frequencies_sorted = student_code.frequencies_sorted

        assert isinstance(frequencies_sorted,np.ndarray)

    def test_have_frequencies_sorted_is_actually_sorted(self, student_code):
        frequencies_sorted = student_code.frequencies_sorted
        assert np.all(np.sort(frequencies_sorted)[::-1]==frequencies_sorted) and "your frequencies_sorted should be sorted in *decreasing* order"

    def test_have_frequencies_unsorted_first_10_values(self, student_code):
        frequencies_unsorted = student_code.frequencies_unsorted
        assert np.all(frequencies_unsorted[0:10] == np.array([626,   1,   1,  94,   3,   1,   2,   1,   2,   1]))


    def test_have_frequencies_sorted_first_10_values(self, student_code):
        frequencies_sorted = student_code.frequencies_sorted
        assert np.all(frequencies_sorted[0:10] == np.array([1631,  864,  725,  626,  541,  530,  510,  462,  409,  386]))


    def test_have_plot(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name,'assign5_task4.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign5_task4.png' and starts with your last name."




# this suite is conditional on finding the code file specified.
#
# https://stackoverflow.com/questions/38966785/it-is-possible-to-skip-fail-test-in-setup-using-pytest

@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask5FunctionPlot:



    def test_have_x_and_is_array(self, student_code):
        assert isinstance(student_code.x, np.ndarray)

    def test_x_values(self, student_code):
        x = student_code.x

        # first value
        assert x[0] == 0.0
        
        # middle values
        assert x[49] == (1/99)*49
        assert x[50] == (1/99)*50

        # last values should be 1.0
        assert x[-1] == 1.0
        assert x[99] == 1.0


    def test_have_f(self, student_code):
        function_values = student_code.function_values
        assert isinstance(function_values, np.ndarray)

        assert function_values.shape == (5,100)


    def test_function_values_first_row(self, student_code):
        x = student_code.x
        function_values = student_code.function_values

        assert np.all(function_values[0,:] == 2*(x-1/2))

    def test_have_plot(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name,'assign5_task5.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign5_task5.png' and starts with your last name."





# this suite is conditional on finding the code file specified.
#
# https://stackoverflow.com/questions/38966785/it-is-possible-to-skip-fail-test-in-setup-using-pytest

@pytest.mark.skipif(not student_code_exists(), reason=f"specified code file {with_dotpy(student_code_filename)} doesn't exist")
class TestTask6BusSimulation:

    def test_have_simulate_simulate_busses_function(self, student_code):
        assert callable(student_code.simulate_busses)

    def test_can_call_simulate_busses(self, student_code):
        simulate_busses = student_code.simulate_busses

        simulate_busses(mean=15, num_busses=50)
        simulate_busses(mean=10, num_busses=30)

    def test_have_mean_wait_function(self, student_code):
        assert callable(student_code.mean_wait)

    def test_have_shortest_wait_function(self, student_code):
        assert callable(student_code.shortest_wait)

    def test_have_longest_wait_function(self, student_code):
        assert callable(student_code.longest_wait)

    def test_have_cumulative_wait_function(self, student_code):
        assert callable(student_code.cumulative_wait)




    def test_have_data(self, student_code):
        assert isinstance(student_code.bus_times, np.ndarray)

    def test_length_bus_times(self, student_code):
        assert student_code.bus_times.shape == (50,)


    def test_cumulative_wait_given_data(self, student_code):
        cumulative_wait = student_code.cumulative_wait
        assert np.all(np.abs(cumulative_wait(np.array([11.21, 34.15, 18.89, 23.51])) - np.array([11.21, 45.36, 64.25, 87.76]) ) < 0.001)

    def test_cumulative_wait_correct_values_first_four(self, student_code):
        cumulative_wait = student_code.cumulative_wait
        bus_times = student_code.bus_times
        assert cumulative_wait(bus_times)[0] == bus_times[0]
        assert cumulative_wait(bus_times)[1] == np.sum(bus_times[0:2])
        assert cumulative_wait(bus_times)[2] == np.sum(bus_times[0:3])
        assert cumulative_wait(bus_times)[3] == np.sum(bus_times[0:4])

    def test_cumulative_wait_correct_values_all(self, student_code):
        cumulative_wait = student_code.cumulative_wait
        bus_times = student_code.bus_times

        for ii in range(len(bus_times)):
            assert np.abs(cumulative_wait(bus_times)[ii] - np.sum(bus_times[0:ii+1])) < 1e-5


    def test_have_plot_line(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name,'assign5_task6_line.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign5_task6_line.png' and starts with your last name."

    def test_have_plot_hist(self, student_code):
        assert len(find_files_student_name_and_ending(student_code.last_name,'assign5_task6_hist.png',allow_previous=False))>0 and "i didn't find a file that ends with 'assign5_task6_hist.png' and starts with your last name."