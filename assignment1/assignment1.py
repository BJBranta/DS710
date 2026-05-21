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


# Task 2 (Computing)
lime_density_grams_per_cup = 248
grapefruit_density_grams_per_cup = 226.8
grams_per_pound = 453.592
oz_per_cup = 8
ml_per_oz = 29.574

ml_per_cup = oz_per_cup * ml_per_oz
lime_density_grams_per_ml = lime_density_grams_per_cup / ml_per_cup
lime_density_pounds_per_oz = lime_density_grams_per_cup / grams_per_pound / oz_per_cup
mixed_density_grams_per_cup = (
    lime_density_grams_per_cup + grapefruit_density_grams_per_cup
) / 2
mixed_mass_grams = 0.75 * mixed_density_grams_per_cup
mixed_weight_pounds = mixed_mass_grams / grams_per_pound
mixed_density_pounds_per_oz = mixed_density_grams_per_cup / oz_per_cup / grams_per_pound


# Task 3 (Computing)
# fmt: off
# copy this verbatim into your .py file

def generate_robot_message(first_name, last_name, possible_messages_init, possible_messages_term): #  <---- do not modify this line
    import random  # gain access to the `random` library

    # select a random integer
    selection_init = random.randrange(len(possible_messages_init))
    selection_term = random.randrange(len(possible_messages_term))

    # extract the randomly selected init or term message part using []
    message_init = possible_messages_init[selection_init]
    message_term = possible_messages_term[selection_term]

    # construct a message using f-string formatting
    message = f"{message_init}, {first_name} {last_name}.  {message_term}" # 1️⃣ <---- Modify this line in Task 3 to also use `last_name`

    return message  #to get data out of a function, we must use the `return` keyword

# a hardcoded list of initial messages
possible_messages_init = [
    "greetings",
    "cheerio",
    "good day",
    "uh oh",
    "hello there",
]  # 2️⃣ <---- add a thing to the end of this list

# another hardcoded list of terminal messages
possible_messages_term = [
    "actually, i need to go over there now",
    "wait, don't i know you",
    "this conversation is so boring",
    "i'm a robot, i don't have feelings",
]  # 2️⃣ <---- add a thing to this list


# 3️⃣ inputs are the lowercase names.
message_result = generate_robot_message(first_name_capitalized, last_name_capitalized, possible_messages_init,
    possible_messages_term,
)
