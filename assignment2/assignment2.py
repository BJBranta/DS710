first_name = "Ben"
last_name = "Branta"


# Task 1 - Divisibility and Integers
# Write code to compute the greatest power of a given number that divides another.
# I used a function so I didn't have to copy and paste code. I think the upcoming lessons are on functions as well so I hope this is ok.
def greatest_power_of_k_dividing_n(n, k):
    # Find the greatest integer i such that k^i divides n
    i = 1  # Initialize i to 1, since k^0 = 1 divides n for any n
    while n % (k**i) == 0:  # Check if k^i divides n
        i += 1  # increment i to check the next power of k
    return i - 1  # Subtract 1 to get the greatest power that divides n


val_2_24 = greatest_power_of_k_dividing_n(24, 2)
print(val_2_24)  # Verify result
val_5_24 = greatest_power_of_k_dividing_n(24, 5)
print(val_5_24)  # Verify result
val_3_30 = greatest_power_of_k_dividing_n(30, 3)
print(val_3_30)  # Verify result
val_2_10540974080 = greatest_power_of_k_dividing_n(10540974080, 2)
print(val_2_10540974080)  # Verify result

# Task 2 - Prime Numbers
# A prime number is a positive integer greater than 1 whose only divisors are 1 and itself.
# That is n is a prime number only if n%q is nonzero for all q greqter than 1 and less than n.
# 1 is not prime. Neither is 0.
# Subtask 2.1: Prime Counting
# Use a combination of control flow, the modulus operator, and looping over a range to count
# how many of the numbers from 1 thru 999 (inclusive) are prime numbers.
# Save this number to the variable num_primes.

num_primes = 0  # Initialize count of prime numbers
for n in range(1, 1000):  # Loop through numbers from 1 to 999
    if n > 1:  # check if n is greater than 1
        n_is_prime = True  # Assume n is prime until we find a divisor
        for q in range(2, n):  # loop through numbers from 2 to n-1
            if n % q == 0:  # check if n is divisible by q
                n_is_prime = False  # if n is divisible by q, it is not prime
                break  # break out of the loop
            else:
                pass  # if n is not divisible by q, continue checking
        if n_is_prime:  # if n is still marked as prime
            # print(f"{n} is prime")  # Print that n is prime
            num_primes += 1  # Increment count of prime numbers
    else:
        pass  # If n is 1 or less, do nothing (not prime)
print(num_primes)  # Verify result


# Task 3 - Mortgage Calculator
# Every month,
#    1. The amount you owe (the balance) first increases due to interest: 1/12 of the annual interest rate time the current balance.
#    2. Then, the balance decreases due to your monthly payment.
#  This happens until the loan is paid off. The last month is different, though.
#    DO NOT overpay in the last month. Interest acrues, but after that, if the balance is less than your payment, just pay the remaining balance (including the month's interest).

# Use control flow to create a mortgage calculator. Your calculator should be able to accept any 'principal loan amount', 'interest rate', and 'monthly payment'.
# As output your calculator should compute
#  1. The total months it took to pay off the mortgage,
#  2. The total amount paid over that time.
# If the monthly payment is too low to actually ever pay off the loan (infinite loop), your control flow must gracefully end with an appropriate error message.

# Considerations
#  Do not round.
#  The final payment will be smaller than the others, check for it, don't end up with negative balance. The final balance must be 0. (Each iteration check for balance less due less than monthly payment)
#  If the monthly payment is too small, the balance will go up every month!  (Each iteration check if balance is increasing, if so, exit gracefully with an appropriate error message)
#  Use float for all numbers.


def mortgage_calculator(
    principal_loan_amount: float, interest_rate: float, monthly_payment: float
):

    # Value and type validation
    if principal_loan_amount <= 0:
        raise ValueError("Principal loan amount must be greater than zero.")
    if not isinstance(principal_loan_amount, float):
        raise TypeError("Principal loan amount must be numeric type float.")
    if interest_rate < 0:
        raise ValueError("Interest rate cannot be negative.")
    if not isinstance(interest_rate, float):
        raise TypeError("Interest rate must be numeric type float.")
    if monthly_payment <= 0:
        raise ValueError("Monthly payment must be greater than zero.")
    if not isinstance(monthly_payment, float):
        raise TypeError("Monthly payment must be numeric type float.")

    balance = principal_loan_amount
    total_paid = 0.0
    months = 0

    while balance > 0:
        interest = (interest_rate / 12) * balance  # Calculate monthly interest
        balance += interest  # Add interest to balance
        if balance < monthly_payment:  # Check the remaining balance
            total_paid += balance  # Pay off the remaining balance
            balance = 0.0  # Set balance to zero
        else:
            total_paid += monthly_payment  # Add monthly payment to total paid
            balance -= monthly_payment  # Subtract monthly payment from balance
        months += 1  # Increment month count
        # Check if balance is increasing
        if months > 1 and balance > principal_loan_amount:
            raise ValueError(
                "Error: Monthly payment is too low to ever pay off the loan."
            )
    return months, total_paid  # Return total months and total amount paid


try:
    test_p500_r5_mp100_number_of_months, test_p500_r5_mp100_total_paid = (
        mortgage_calculator(500.0, 0.05, 100.0)
    )
    print(test_p500_r5_mp100_number_of_months, test_p500_r5_mp100_total_paid)
except (TypeError, ValueError) as e:
    print(f"Error: {e}")

try:
    test_p500_r5_mp500_number_of_months, test_p500_r5_mp500_total_paid = (
        mortgage_calculator(500.0, 0.05, 500.0)
    )
    print(test_p500_r5_mp500_number_of_months, test_p500_r5_mp500_total_paid)
except (TypeError, ValueError) as e:
    print(f"Error: {e}")  # Verify number of months

try:
    test_p500_r5_mp1_number_of_months, test_p500_r5_mp1_total_paid = (
        mortgage_calculator(500.0, 0.05, 1.0)
    )
    print(test_p500_r5_mp1_number_of_months, test_p500_r5_mp1_total_paid)
except (TypeError, ValueError) as e:
    print(f"Error: {e}")


assert test_p500_r5_mp100_number_of_months == 6  # noqa
assert round(test_p500_r5_mp100_total_paid, 2) == 506.35  # noqa
assert test_p500_r5_mp500_number_of_months == 2  # noqa
assert round(test_p500_r5_mp500_total_paid, 2) == 502.09  # noqa


# Subtask 3.3: Calculator Analysis
# Supposed you had a morgage with a principal of 250,000, an interest rate of 4%, and a monthly payment of $1000
# Use  your calculator to determine how many months it would take to pay the loan off. Store this value in the variable length_of_loan.
# Do not separate the total number of months into years and months. Leve as a total number.
# How much would you have paid in total? Store this value in the variable total_paid.

try:
    length_of_loan, total_paid = mortgage_calculator(250000.0, 0.04, 1000.0)
    print(length_of_loan, total_paid)
except (TypeError, ValueError) as e:
    print(f"Error: {e}")
