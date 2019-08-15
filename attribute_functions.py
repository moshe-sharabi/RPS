from util import Counter
import Constants as cons


class HistoryException(ValueError):
    def __init__(self):
        super(HistoryException, self).__init__()

def quantize(count):
    if count < cons.MAX_LENGTH_FOR_EVERYTHING:
        return str(count)
    else:
        return cons.PARAM_MAX_LENGTH
def get_last_played(history):
    if not history:
        raise HistoryException
    return history[-1][cons.INDEX_OF_PLAY]


def get_most_played(history):
    c = Counter()
    for game in history:
        c[game[cons.INDEX_OF_PLAY]] += 1
    return c.argMax()


def get_most_playedd_in_last_10(history):
    if len(history) <= 10:
        return get_most_played(history)
    return get_most_played(history[-10:])


def get_most_successful(history):
    c = Counter()
    for member in cons.Choices:
        c[member] = 0
    for game in history:
        c[game[cons.INDEX_OF_PLAY]] += cons.points[game[cons.INDEX_OF_RESULT]]
    return c.argMax()


def get_most_successful_in_last_5(history):
    return get_most_successful(history[-5:])


def get_most_played_after_comp_move(history):
    last_comp_play = cons.neg[history[-1]][cons.INDEX_OF_PLAY]
    c = Counter()
    for i in range(len(history) - 1):
        if cons.neg[history[i]][cons.INDEX_OF_PLAY] == last_comp_play:
            c[history[i + 1][cons.INDEX_OF_PLAY]] += 1
    return c.argMax() if c.argMax() else cons.NOT_AVAILABLE


def get_last_sequence_length(history):
    sequence_play = history[-1][cons.INDEX_OF_PLAY]
    reversed_history = history[::-1][1:]
    i = 1
    for game in reversed_history:
        if game[cons.INDEX_OF_PLAY] != sequence_play:
            if i >= cons.MAX_LENGTH_FOR_EVERYTHING:
                return cons.PARAM_MAX_LENGTH
        i += 1
    if i >= cons.MAX_LENGTH_FOR_EVERYTHING:
        return cons.PARAM_MAX_LENGTH
    return quantize(i)


def get_pattern_next_choice(history):
    history_no_results = [game[cons.INDEX_OF_PLAY] for game in history]
    longest_possible_sequence = len(history) / 2 if len(history) % 2 == 0 else int(len(history) / 2) + 1
    shortest_checked_sequence = 2
    for i in range(int(longest_possible_sequence), int(shortest_checked_sequence), -1):  # i is sequence length
        set1 = history_no_results[1 - i * 2:1 - i]
        set2 = history_no_results[1 - i:]
        if set1[:-1] == set2:
            return set1[-1]
    # for i=2 we check for at least 2 full patterns before this one
    # i.e. R,S,R,S,R - next this function predicts R
    if len(history) >= 5:
        set1 = history_no_results[-5:-3]
        set2 = history_no_results[-3:-1]
        if set1 == set2 and set1[0] == history_no_results[-1]:
            return set1[1]
    # checking for staying with the same choice
    if len(history) >= 3:
        if history_no_results[-3] == history_no_results[-2] == history_no_results[-1]:
            return history_no_results[-1]
    # no pattern was found
    return cons.NOT_AVAILABLE


def num_smth(member):
    """
    return a functionn that counts how many times the member appeared in history
    :param member: member
    :return: the function
    """

    def count(history):
        counter = 0
        for move in history:
            if move[cons.INDEX_OF_PLAY] == member:
                counter += 1
        if counter >= cons.MAX_LENGTH_FOR_EVERYTHING:
            return cons.PARAM_MAX_LENGTH
        return quantize(counter)  # /float(len(history))

    return count

def num_smth_in_last_x(member,x):
    """
    return a functionn that counts how many times the member appeared in history
    :param member: member
    :return: the function
    """

    def count(history):
        history = history[-x:]
        counter = 0
        for move in history:
            if move[cons.INDEX_OF_PLAY] == member:
                counter += 1
        if counter >= cons.MAX_LENGTH_FOR_EVERYTHING:
            return cons.PARAM_MAX_LENGTH
        return quantize(counter)  # /float(len(history))

    return count


def longer_sequence(history):
    """
    returns the member with the longest last seqeunce
    :param history:
    :return:
    """
    c = Counter()
    for member in cons.Choices:
        flag = False
        counter = 0
        for i in range(len(history) - 1, -1, -1):
            if history[i][cons.INDEX_OF_PLAY] == member:
                flag = True
                c[member] += 1
                continue
            if flag:
                break
    return c.argMax()


def sequence_smth(member):
    """
    creates a function that countss the lenght of the last sequence of the member in history
    :param member:the member
    :return:the function
    """

    def count(history):
        flag = False
        counter = 0
        for i in range(len(history) - 1, 0, -1):
            if history[i][cons.INDEX_OF_PLAY] == member:
                flag = True
                counter += 1
                continue
            if flag:
                break
        if counter >= cons.MAX_LENGTH_FOR_EVERYTHING:
            return cons.PARAM_MAX_LENGTH
        return quantize(counter)  # /float(len(history))

    return count

def sequence_smth_in_last_x(member, x):
    """
    creates a function that countss the lenght of the last sequence of the member in history
    :param member:the member
    :return:the function
    """

    def count(history):
        history = history[-x:]
        flag = False
        counter = 0
        for i in range(len(history) - 1, 0, -1):
            if history[i][cons.INDEX_OF_PLAY] == member:
                flag = True
                counter += 1
                continue
            if flag:
                break
        if counter >= cons.MAX_LENGTH_FOR_EVERYTHING:
            return cons.PARAM_MAX_LENGTH
        return quantize(counter)  # /float(len(history))

    return count

def last_winning_streak(history):
    count = 0
    for game in history[::-1]:
        if game[cons.INDEX_OF_RESULT] == cons.WIN:
            count += 1
        else:
            break
    return quantize(count)