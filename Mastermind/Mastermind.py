import random

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
def generate_all_possibilities(pin_am, color_am):
    all_poss = []
    new_color = [0] * pin_am
    while new_color is not None:
        all_poss.append(new_color)
        new_color = next_comb(new_color, color_am)
    return all_poss


#   Gives a random color combination
def random_color_comb(pin_am, color_am):
    color_comb = []
    for i in range(pin_am):
        color_comb.append(random.randint(0, color_am - 1))
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
def get_pro_feedback(correct_comb, attempt):
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


#   The program gives a new attempt based on the possibilities, the previous attempts and the feedback it got
def get_pro_attempt(poss, att, feeds, color_text):
    if [0, 0, 1, 2] in poss:
        return [0, 0, 1, 2]

    #   following lines are "under construction", these will at the moment never be run
    """
    unused_poss = [i for j, i in enumerate(poss) if j not in att]
    scores = []
    for left_poss_i in range(len(poss)):
        print(left_poss_i, scores)
        worst_score = None
        for un_poss_i in range(len(unused_poss)):
            feedback = get_pro_feedback(poss[left_poss_i], unused_poss[un_poss_i])
            score = len(update_possibilities(poss, att, [feedback]))
            #print(score)
            if worst_score is None:
                worst_score = score
            elif score > worst_score:
                worst_score = score
        scores.append(worst_score)
    return poss[scores.index(min(scores))]
    """

    return poss[random.randint(0, len(poss) - 1)]


#   Asks the user in the console for feedback
def get_user_feedback(poss, att):
    while True:
        try:
            feedback = [int(input("Number of pins of the right color in the right spot:\t")),
                        int(input("Number of pins of the right color not in the right spot:"))]
            if 0 <= feedback[0] <= 4 and 0 <= feedback[1] <= 4 and sum(feedback) <= 4:
                return feedback
            else:
                print("Number of pins not possible.")
        except:
            print("User input not in the right format.")


#   Asks the user in the console for a attempt
def get_user_attempt(poss, att, feeds, color_text):
    while True:
        try:
            return color_string_to_code_list(input("Attempt:\t"), color_text)
        except:
            print("User input should be colors from the color options and separated with spaces.")
            print("For example:\tred green blue yellow")


#   Play the game by the rules in a turn-based loop
def play(get_feedback=get_pro_feedback,
         get_attempt=get_pro_attempt,
         cor=None,
         pin_amount=default_pin_amount,
         color_amount=default_color_amount,
         color_text=default_color_text):
    try:
        possi = generate_all_possibilities(pin_amount, color_amount)
        attempts, feedbacks = [], []
        if cor is None:
            cor = random_color_comb(pin_amount, color_amount)

        print("\nColor options:", color_text, '\n')

        while True:
            attempts.append(get_attempt(possi, attempts, feedbacks, color_text))

            attempt_string = ''
            for color_code in attempts[-1]:
                attempt_string = attempt_string + ' ' + color_text[color_code]
            print("Attempt:" + attempt_string)

            feedbacks.append(get_feedback(cor, attempts[-1]))
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
    except:
        print("Something went wrong during the game.")


#   A example of getting user input for the settings of the game
if __name__ == "__main__":
    if input("Should the computer be the code breaker? Y/n\t").lower() in ('n', 'no'):
        breaker = get_user_attempt
    else:
        breaker = get_pro_attempt

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

    color_text = input("Which colors are you playing with (in text)? blank will be the default:\n{}\n"
                       .format(str(default_color_text[:color_amount])[1:-1].replace('\'', '').replace(',', '')))
    if color_text == '':
        color_text = default_color_text
    else:
        color_text = color_text.split(' ')

    secret = None
    if master == get_pro_feedback:
        secret = input("If you want to manually set the secret code, give it now, else leave blank.\t")
        if secret != '':
            secret = color_string_to_code_list(secret, default_color_text)
        else:
            secret = None

    play(get_feedback=master, get_attempt=breaker, cor=secret, pin_amount=pin_amount, color_amount=color_amount,
         color_text=color_text)
