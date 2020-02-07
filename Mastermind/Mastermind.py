import random


def get_index_positions(list_of_elements, element):
    #   from: https://thispointer.com/python-how-to-find-all-indexes-of-an-item-in-a-list/
    """ Returns the indexes of all occurrences of give element in
    the list- list_of_elements """
    index_pos_list = []
    index_pos = 0
    while True:
        try:
            # Search for item in list from index_pos to the end of list
            index_pos = list_of_elements.index(element, index_pos)
            # Add the index position in list
            index_pos_list.append(index_pos)
            index_pos += 1
        except ValueError as e:
            break
    return index_pos_list


def next_poss(previous_color, color_am):
    prev_color = list(previous_color)
    if not prev_color:
        return None
    prev_color[-1] += 1
    if prev_color[-1] >= color_amount:
        prev_color[-1] = 0
        sub = next_poss(prev_color[:-1], color_amount)
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


def get_feedback(correct_color, attempt):
    correct_color: list
    attempt: list
    feedback = []
    used = set()
    for i in range(len(attempt)):
        if attempt[i] == correct_color[i]:
            feedback.append(2)
            used.add(i)
    for i in range(len(attempt)):
        if correct_color[i] in attempt:
            available = set(get_index_positions(attempt, correct_color[i])).difference(set(used))
            if len(available) > 0:
                feedback.append(1)
                used.add(random.sample(available, 1)[0])
    return feedback


def update_possibilities(poss, past_atmpt, feedbacks):
    for tc in poss:     # Test Case
        pass
    return poss


def get_attempt(poss):
    return poss[random.randint(0, len(poss)-1)]


if __name__ == "__main__":
    pin_amount = 4
    color_amount = 6
    poss = generate_all_possibilities(pin_amount, color_amount)
    cor = random_color(pin_amount, color_amount)
    attempts, feedbacks = [], []
    while True:
        attempts.append(get_attempt(poss))
        feedbacks.append(get_feedback(cor, attempts[-1]))
        print(attempts[-1], feedbacks[-1])
        if feedbacks[-1] == [2]*pin_amount:
            break
        poss = update_possibilities(poss, attempts, feedbacks[-1])
    print("Done")
