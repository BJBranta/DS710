first_name = "Ben"
last_name = "Branta"


# Task 1 (Computing)
first_name_lowercase = "ben"
last_name_lowercase = "branta"
first_name_capitalized = first_name_lowercase.capitalize()
last_name_capitalized = last_name_lowercase.capitalize()
full_name = first_name_capitalized + " " + last_name_capitalized
name_pieces = full_name.split(" ")
print(type(name_pieces))

assert name_pieces[0] == first_name_capitalized.split()[0]
assert name_pieces[1] == last_name_capitalized.split()[0]
