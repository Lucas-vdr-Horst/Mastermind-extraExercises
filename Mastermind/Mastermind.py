import random
import multiprocessing

"""
Lucas van der Horst
HBO-ICT Utrecht AI Structured Programming
Mastermind

It's really easy to crash the program, there is very little user input check,
because that wasn't my point of the project, that's more front-end, this was about the logic

For the multiprocessing used:
https://stackoverflow.com/questions/23816546/how-many-processes-should-i-run-in-parallel
https://stackoverflow.com/questions/10415028/how-can-i-recover-the-return-value-of-a-function-passed-to-multiprocessing-proce
"""

#   defaults:
default_pin_amount = 4
default_color_text = ('red', 'yellow', 'black', 'white', 'green', 'blue', 'brown', 'orange', 'purple', 'pink', 'gray')
default_color_amount = 6


#   Gives the next color combination, so [1, 5, 2, 4] becomes [1, 5, 2, 5], 
#   needs the amount of colors so [1, 7] becomes [2, 0]
def next_comb(previous_colors, color_am):
    prev_colors = list(previous_colors)
    if not prev_colors:
        return None
    prev_colors[-1] += 1
    if prev_colors[-1] >= color_am:
        prev_colors[-1] = 0
        sub = next_comb(prev_colors[:-1], color_am)
        if sub is None:
            return None
        prev_colors[:-1] = sub
    return list(prev_colors)


#   Give all the possibilities (all the color combinations) with these amount of pins and the amount of colors
def generate_all_possibilities(pin_am, color_am, duplicates):
    all_poss = []
    new_comb = [0] * pin_am
    while new_comb is not None:
        if duplicates or len(set(new_comb)) == len(new_comb):
            all_poss.append(new_comb)
        new_comb = next_comb(new_comb, color_am)
    return all_poss


#   Gives a random color combination
def random_color_comb(pin_am, color_am, duplicates):
    color_comb = []
    for i in range(pin_am):
        new_color = random.randint(0, color_am - 1)
        while not (duplicates) and new_color in color_comb:
            new_color = random.randint(0, color_am - 1)
        color_comb.append(new_color)
    return color_comb


#   Forms a code list like [2, 1, 0, 4] from a color string like 'black yellow red green'
def color_string_to_code_list(color_string, color_text):
    code_list = color_string.lower().split(' ')

    for color_i in range(len(code_list)):
        code_list[color_i] = color_text.index(code_list[color_i])

    return code_list


#   The program takes the correct code and a attempt and gives feedback,
#   like [1, 2] the zeroth index means that one pin is correct
#   and first index means two are the right color but not in the right place
def get_pro_feedback(correct_comb, attempt, pin_amount=default_pin_amount):
    correct_comb: list
    attempt: list
    feedback = [0, 0]
    cor_used = []

    for color_i in range(len(attempt)):
        if attempt[color_i] == correct_comb[color_i]:
            feedback[0] += 1
            cor_used.append(color_i)
    for color_i in range(len(correct_comb)):
        if color_i not in cor_used and correct_comb[color_i] in attempt:
            feedback[1] += 1

    return feedback


#  Takes a list of color combinations and removes all the color combinations that aren't possible with the last feedback
def update_possibilities(possibilities, past_atmpt, feedbacks):
    poss = list(possibilities)
    remove_indexes = []

    for tc_i in range(len(poss)):  # Test Case index
        if not (get_pro_feedback(poss[tc_i], past_atmpt[-1]) == feedbacks[-1]):
            remove_indexes.insert(0, tc_i)

    for rem in remove_indexes:
        poss.pop(rem)

    return poss


#   Gives the amount of combinations would be removed if this would be run through update_possibilities()
def amount_updated(possibilities, past_atmpt, feedbacks):
    amount_remove = 0
    for tc_i in range(len(possibilities)):  # Test Case index
        if not (get_pro_feedback(possibilities[tc_i], past_atmpt[-1]) == feedbacks[-1]):
            amount_remove += 1
    return amount_remove


#   Gives a new attempt based on feedback
#   However this function was written before I read the "YET ANOTHER MASTERMIND STRATEGY paper by Barteld Kooi",
#   it's basically the same as his 2.1 strategy
def a_simple_strategy(poss, att, feeds, color_text, all_combs):
    return poss[random.randint(0, len(poss) - 1)]


#   Part of the multiprocessing, tests one attempt against all the possibilities,
#   counts the amount of possibilities can be removed and returns the average
def gem_rem_worker(poss, unused_poss, unused_i, return_list):
    amount_rem = []
    for poss_i in range(len(poss)):
        attempt = unused_poss[unused_i]
        amount_rem.append(amount_updated(poss, [attempt], [get_pro_feedback(poss[poss_i], attempt)]))
    return_list[unused_i] = sum(amount_rem) / len(amount_rem)


#   Gives a new attempt based on feedback
#   A custom strategy which compares every option vs every possibility
#   and looks how many combinations it would remove from the possibilities,
#   then chooses the one that removes the most on average
#   The problem is that the amount of sets to compare increases VERY fast when adding more pins or colors
def custom_strategy(poss, att, feeds, color_text, all_combs):
    if len(poss) == 1:
        return poss[0]

    manager = multiprocessing.Manager()
    unused_poss = [i for j, i in enumerate(all_combs) if j not in att]
    gem_rem = manager.list()
    num_workers = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(num_workers)

    for i in range(len(unused_poss)):
        gem_rem.append(0)

    for unused_i in range(len(unused_poss)):
        pool.apply_async(gem_rem_worker, args=(poss, unused_poss, unused_i, gem_rem))
    pool.close()
    pool.join()

    return unused_poss[gem_rem.index(max(gem_rem))]


#   Asks the user in the console for feedback
def get_user_feedback(poss, att, pin_amount):
    while True:
        try:
            feedback = [int(input("Number of pins of the right color in the right spot:\t")),
                        int(input("Number of pins of the right color not in the right spot:"))]
            if 0 <= feedback[0] <= pin_amount and 0 <= feedback[1] <= pin_amount and sum(feedback) <= pin_amount:
                return feedback
            else:
                print("Number of pins not possible.")
        except:
            print("User input not in the right format.")


#   Asks the user in the console for a attempt
def get_user_attempt(poss, att, feeds, color_text, all_combs):
    while True:
        try:
            return color_string_to_code_list(input("Attempt:\t"), color_text)
        except:
            print("User input should be colors from the color options and separated with spaces.")
            print("For example:\tred green blue yellow")


#   Play the game by the rules in a turn-based loop
def play(get_feedback=get_pro_feedback,
         get_attempt=a_simple_strategy,
         cor=None,
         pin_amount=default_pin_amount,
         color_amount=default_color_amount,
         color_text=default_color_text,
         duplicates=True):
    all_combinations = generate_all_possibilities(pin_amount, color_amount, duplicates)
    possi = list(all_combinations)
    attempts, feedbacks = [], []
    if cor is None:
        cor = random_color_comb(pin_amount, color_amount, duplicates)

    print("\nColor options:", color_text, '\n')

    while True:
        attempts.append(get_attempt(possi, attempts, feedbacks, color_text, all_combinations))

        attempt_string = ''
        for color_code in attempts[-1]:
            attempt_string = attempt_string + ' ' + color_text[color_code]
        print("Attempt:" + attempt_string)

        feedbacks.append(get_feedback(cor, attempts[-1], pin_amount))
        print("Feedback:", feedbacks[-1])
        if feedbacks[-1][0] == pin_amount:
            print("\nDone in {} steps".format(len(attempts)))
            break

        possi = update_possibilities(possi, attempts, feedbacks)
        if len(possi) <= 0:
            print("\nNo possibilities")
            break
        print("Still {} possibilities".format(len(possi)))
    print()


#   A example of getting user input for the settings of the game
if __name__ == "__main__":
    breaker = (get_user_attempt, a_simple_strategy, custom_strategy) \
        [int(input("Who should be the code breaker? user, simple_strategy, custom_strategy. choose 1, 2 or 3\t")) - 1]
    if breaker == custom_strategy:
        print("WARNING: decrease the amount of pins / amount of colors / disable duplicates,\n"
              "processing times can be very long with the default settings")

    if input("Should the computer be the code master? Y/n\t").lower() in ('n', 'no'):
        master = get_user_feedback
    else:
        master = get_pro_feedback

    pin_amount = input("How many pins are there? blank will be the default of {}\t".format(default_pin_amount))
    if pin_amount.isnumeric():
        pin_amount = int(pin_amount)
    else:
        pin_amount = default_pin_amount

    color_amount = input("How many different colors are there? blank will be the default of {}\t"
                         .format(default_color_amount))
    if color_amount.isnumeric():
        color_amount = int(color_amount)
    else:
        color_amount = default_color_amount

    color_text = input("Which colors are you playing with (in text)? blank will be the default:\n{}\t"
                       .format(str(default_color_text[:color_amount])[1:-1].replace('\'', '').replace(',', '')))
    if color_text == '':
        color_text = default_color_text[:color_amount]
    else:
        color_text = color_text.split(' ')

    duplicates = input("Allow duplicate colors in the secret code: Y/n\t").lower() not in ('n', 'no')

    secret = None
    if master == get_pro_feedback:
        secret = input("If you want to manually set the secret code, give it now, else leave blank.\t")
        if secret != '':
            secret = color_string_to_code_list(secret, default_color_text)
        else:
            secret = None

    play(get_feedback=master, get_attempt=breaker, cor=secret, pin_amount=pin_amount, color_amount=color_amount,
         color_text=color_text, duplicates=duplicates)
