import random
import json

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


def get_feedback(correct_comb, attempt):
    correct_comb: list
    attempt: list
    feedback = []
    cor_used = []
    for color_i in range(len(attempt)):
        if attempt[color_i] == correct_comb[color_i]:
            feedback.append(2)
            cor_used.append(color_i)
    for color_i in range(len(correct_comb)):
        if color_i not in cor_used and correct_comb[color_i] in attempt:
            feedback.append(1)
    return feedback


def update_possibilities(poss, past_atmpt, feedbacks):
    remove_indexes = []
    for tc_i in range(len(poss)):     # Test Case index
        if not(get_feedback(poss[tc_i], past_atmpt[-1]) == feedbacks[-1]):
            remove_indexes.insert(0, tc_i)
    for rem in remove_indexes:
        poss.pop(rem)
    return poss


def get_attempt(poss, att, feeds):
    return poss[random.randint(0, len(poss)-1)]
    unused_poss = [i for j, i in enumerate(poss) if j not in att]
    scores = []
    for left_poss_i in range(len(poss)):
        worst_score = None
        for un_poss_i in range(len(unused_poss)):
            feedback = get_feedback(poss[left_poss_i], unused_poss[un_poss_i])
            score = len(update_possibilities(poss, att, [feedback]))
            if worst_score is None:
                worst_score_score = score
            elif score > worst_score:
                worst_score = worst_score
        scores.append(worst_score)
    return poss[scores.index(min(scores))]


def play_as_breaker(pin_amount=default_pin_amount, color_amount=default_color_amount,  color_dict=default_color_dict):
    possi = generate_all_possibilities(pin_amount, color_amount)
    attempts, feedbacks = [[0, 0, 1, 1]], []
    while True:
        attempt_string = ''
        for color_code in attempts[-1]:
            attempt_string = attempt_string + ' ' + color_dict[color_code]
        feedbacks.append(json.loads(input("attempt:{}, feedback: ".format(attempt_string))))
        #print("attempt: {}, feedback: {}".format(attempts[-1], feedbacks[-1]),
        #      end=' ' * ((3 + pin_amount * 3) - len(str(feedbacks[-1]))))
        if feedbacks[-1] == [2] * pin_amount:
            break
        possi = update_possibilities(possi, attempts, feedbacks)
        print("still {} possibilities".format(len(possi)))
        attempts.append(get_attempt(possi, attempts, feedbacks))
    print("\nDone in {} steps".format(len(attempts)))


def play_as_maker(pin_amount=default_pin_amount, color_amount=default_color_amount, color_dict=default_color_dict):
    print("Color options: {}".format(color_dict))
    cor = random_color(pin_amount, color_amount)
    attempts = []
    while True:
        attempt = input("attempt: ").split(' ')
        for color_i in range(len(attempt)):
            attempt[color_i] = color_dict.index(attempt[color_i])
        attempts.append(attempt)



if __name__ == "__main__":
    play_as_breaker()
    pin_amount = 4
    color_amount = 8
    possi = generate_all_possibilities(pin_amount, color_amount)
    cor = random_color(pin_amount, color_amount)
    # cor = [4, 1, 5, 3]
    attempts, feedbacks = [[0, 0, 1, 1]], []
    while True:
        feedbacks.append(get_feedback(cor, attempts[-1]))
        print("attempt: {}, feedback: {}".format(attempts[-1], feedbacks[-1]), end=' '*((3 + pin_amount*3) - len(str(feedbacks[-1]))))
        if feedbacks[-1] == [2]*pin_amount:
            break
        poss = update_possibilities(possi, attempts, feedbacks)
        print("still {} possibilities".format(len(poss)))
        attempts.append(get_attempt(possi, attempts, feedbacks))
    print("\nDone in {} steps".format(len(attempts)))
