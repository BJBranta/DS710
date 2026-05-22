first_name = "Ben"
last_name = "Branta"


# Task 1 - Divisibility and Integers
# Write code to compute the greatest power of a given number that divides another.
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
