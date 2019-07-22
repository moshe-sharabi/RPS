from util import Counter
from Constants import *


class HistoryException(ValueError):
    def __init__(self):
        super(HistoryException, self).__init__()

def get_last_played(history):
    if not history:
        raise HistoryException
    return history[-1][0]

def get_most_played(history):
    c = Counter()
    for game in history:
        c[game[INDEX_OF_PLAY]] += 1
    return c.argMax()

def get_most_playedd_in_last_10(history):
    if len(history) <= 10:
        return get_most_played(history)
    return get_most_played(history[-10:])

def get_most_successful(history):
    c = Counter()
    for game in history:
        c[game[INDEX_OF_PLAY]] += points[game[INDEX_OF_RESULT]]
    return c.argMax()

def get_most_played_after_comp_move(history):
    last_comp_play = neg[history[-1]][INDEX_OF_PLAY]
    c = Counter()
    for i in range(len(history)-1):
        if neg[history[i]][INDEX_OF_PLAY] == last_comp_play:
            c[history[i+1][INDEX_OF_PLAY]] += 1
    return c.argMax()

def get_last_sequence_length(history):
    sequence_play = history[-1][INDEX_OF_PLAY]
    reversed_history = reversed(history)[1:]
    i = 1
    for game in reversed_history:
        if game[INDEX_OF_PLAY] != sequence_play:
            return i
        i += 1
    return i

def get_pattern_next_choice(history):
    history_no_results = [game[INDEX_OF_PLAY] for game in history]
    longest_possible_sequence = history/2 if history%2==0 else int(history/2)+1
    shortest_checked_sequence = 2
    for i in range(longest_possible_sequence,shortest_checked_sequence,-1): # i is sequence length
        set1 = history_no_results[1-i*2:1-i]
        set2 = history_no_results[1-i:]
        if set1[:-1] == set2:
            return set1[-1]
    return