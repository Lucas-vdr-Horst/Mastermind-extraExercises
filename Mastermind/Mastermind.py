import random

#   defaults:
default_pin_amount = 4
default_color_text = ('red', 'yellow', 'black', 'white', 'green', 'blue')
default_color_amount = len(default_color_text)


#   Gives the next color combination, so [1, 5, 2, 4] becomes [1, 5, 2, 5], 
#   needs the amount of colors so [1, 7] becomes [2, 0]
def next_poss(previous_colors, color_am):
    prev_colors = list(previous_colors)
    if not prev_colors:
        return None
    prev_colors[-1] += 1
    if prev_colors[-1] >= color_am:
        prev_colors[-1] = 0
        sub = next_poss(prev_colors[:-1], color_am)
        if sub is None:
            return None
        prev_colors[:-1] = sub
    return list(prev_colors)


#   Give all the possibilities (all the color combinations) with these amount of pins and the amount of colors
def generate_all_possibilities(pin_am, color_am):
    all_poss = []
    new_color = [0]*pin_am
    while True:
        all_poss.append(new_color)
        new_color = next_poss(new_color, color_am)
        if new_color is None:
            break
    return all_poss


#   Gives a random color combination
def random_color_comb(pin_am, color_am):
    color_comb = []
    for i in range(pin_am):
        color_comb.append(random.randint(0, color_am-1))
    return color_comb


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
    # feedbacks[-1].sort(reverse=True)
    remove_indexes = []
    for tc_i in range(len(poss)):     # Test Case index
        if not(get_pro_feedback(poss[tc_i], past_atmpt[-1]) == feedbacks[-1]):
            remove_indexes.insert(0, tc_i)
    for rem in remove_indexes:
        poss.pop(rem)
    return poss


#   The program gives a new attempt based on the possibilities, the previous attempts and the feedback it got
def get_pro_attempt(poss, att, feeds):
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

    return poss[random.randint(0, len(poss)-1)]


#   Asks the user in the console for feedback
def get_user_feedback(poss, att):
    return list(map(int, input("feedback: ").split(' ')))


#   Asks the user in the console for a attempt
def get_user_attempt(poss, att, feeds, color_text):
    attempt = input("attempt: ").lower().split(' ')
    for color_i in range(len(attempt)):
        attempt[color_i] = color_text.index(attempt[color_i])
    return attempt


#   Play the game by the rules in a turn-based loop
def play(get_feedback=get_pro_feedback, get_attempt=get_pro_attempt, cor=None,
         pin_amount=default_pin_amount, color_amount=default_color_amount,  color_text=default_color_text):
    possi = generate_all_possibilities(pin_amount, color_amount)
    attempts, feedbacks = [], []
    if cor is None:
        cor = random_color_comb(pin_amount, color_amount)
    print("color options:", color_text, '\n')
    while True:
        attempts.append(get_attempt(possi, attempts, feedbacks))
        attempt_string = ''
        for color_code in attempts[-1]:
            attempt_string = attempt_string + ' ' + color_text[color_code]
        print("attempt:" + attempt_string)
        feedbacks.append(get_feedback(cor, attempts[-1]))
        print("feedback:", feedbacks[-1])
        if feedbacks[-1][0] == pin_amount:
            print("\ndone in {} steps".format(len(attempts)))
            break
        possi = update_possibilities(possi, attempts, feedbacks)
        if len(possi) <= 0:
            print("\nNo possibilities")
            break
        print("still {} possibilities".format(len(possi)))
    print()


if __name__ == "__main__":
    play(get_feedback=get_pro_feedback)
