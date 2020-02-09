import random

#   defaults
default_pin_amount = 4
default_color_amount = 8
default_color_dict = ['red', 'yellow', 'pink', 'white', 'purple', 'green', 'blue', 'orange']


def next_poss(previous_color, color_am):
    prev_color = list(previous_color)
    if not prev_color:
        return None
    prev_color[-1] += 1
    if prev_color[-1] >= color_am:
        prev_color[-1] = 0
        sub = next_poss(prev_color[:-1], color_am)
        if sub is None:
            return None
        prev_color[:-1] = sub
    return list(prev_color)


def generate_all_possibilities(pin_am, color_am):
    all_poss = []
    new_color = [0]*pin_am
    while True:
        all_poss.append(new_color)
        new_color = next_poss(new_color, color_am)
        if new_color is None:
            break
    return all_poss


def random_color(pin_am, color_am):
    color = []
    for i in range(pin_am):
        color.append(random.randint(0, color_am-1))
    return color


def get_pro_feedback(correct_comb, attempt, feedbacks=None, color_dict=None):
    correct_comb: list
    attempt: list
    feedback = []
    cor_used = []
    for color_i in range(len(attempt)):
        if attempt[color_i] == correct_comb[color_i]:
            feedback.append(1)
            cor_used.append(color_i)
    for color_i in range(len(correct_comb)):
        if color_i not in cor_used and correct_comb[color_i] in attempt:
            feedback.append(0)
    return feedback


def update_possibilities(possa, past_atmpt, feedbacks):
    poss = list(possa)
    #feedbacks[-1].sort(reverse=True)
    remove_indexes = []
    for tc_i in range(len(poss)):     # Test Case index
        if not(get_pro_feedback(poss[tc_i], past_atmpt[-1]) == feedbacks[-1]):
            remove_indexes.insert(0, tc_i)
    for rem in remove_indexes:
        poss.pop(rem)
    return poss


def get_pro_attempt(poss, att, feeds, color_dict):
    if [0, 0, 1, 1] in poss:
        return [0, 0, 1, 1]
    return poss[random.randint(0, len(poss)-1)]
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


def get_user_feedback(poss, att, feedbacks, color_dict):
    return list(map(int, input("feedback: ").split(' ')))


def get_user_attempt(poss, att, feeds, color_dict):
    attempt = input("attempt: ").lower().split(' ')
    for color_i in range(len(attempt)):
        attempt[color_i] = color_dict.index(attempt[color_i])
    return attempt


def play(get_feedback=get_pro_feedback, get_attempt=get_pro_attempt,
         pin_amount=default_pin_amount, color_amount=default_color_amount,  color_dict=default_color_dict):
    possi = generate_all_possibilities(pin_amount, color_amount)
    attempts, feedbacks = [], []
    gen = random_color(pin_amount, color_amount)
    print("color options:", color_dict, '\n')
    while True:
        attempts.append(get_attempt(possi, attempts, feedbacks, color_dict))
        attempt_string = ''
        for color_code in attempts[-1]:
            attempt_string = attempt_string + ' ' + color_dict[color_code]
        print("attempt:" + attempt_string)
        feedbacks.append(get_feedback(gen, attempts[-1], feedbacks, color_dict))
        print("feedback:", feedbacks[-1])
        if feedbacks[-1] == [1] * pin_amount:
            print("\ndone in {} steps".format(len(attempts)))
            break
        possi = update_possibilities(possi, attempts, feedbacks)
        if len(possi) <= 0:
            print("\nNo possibilities")
            break
        print("still {} possibilities".format(len(possi)))
    print()


if __name__ == "__main__":
    play(get_feedback=get_pro_feedback, get_attempt=get_pro_attempt)
