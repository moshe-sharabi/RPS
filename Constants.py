from attribute_functions import *

Rock = 'R'
Paper = 'P'
Scissors = 'S'
Choices = [Rock, Paper, Scissors]

WIN = 'W'
DRAW = 'D'
LOSS = 'L'

points = {
    WIN: 1,
    DRAW: 0,
    LOSS: -1
}

INDEX_OF_PLAY = 0
INDEX_OF_RESULT = 1

PATTERN_S_NEXT_CHOICE = "patterns next choice"
LAST_SEQUENCE_S_LENGTH = "last sequence length"
MOST_PLAYED_AFTER_COMP_MOVE = "most played after <comp move>"
MOST_SUCCESSFUL = "most successful"
MOST_PLAYED_IN_LAST_10 = "most played in last 10"
MOST_PLAYED = "most played"
LAST_PLAYED = "last played"
attribute_names = [LAST_PLAYED, MOST_PLAYED, MOST_PLAYED_IN_LAST_10, MOST_SUCCESSFUL, MOST_PLAYED_AFTER_COMP_MOVE, LAST_SEQUENCE_S_LENGTH, PATTERN_S_NEXT_CHOICE]
attribute_functions = [get_last_played, get_most_played, get_most_playedd_in_last_10, get_most_successful, get_most_played_after_comp_move, get_last_sequence_length, get_pattern_next_choice]

parameters = {
    LAST_PLAYED: Choices,
    MOST_PLAYED: Choices,
    MOST_PLAYED_IN_LAST_10: Choices,
    MOST_SUCCESSFUL: Choices,
    MOST_PLAYED_AFTER_COMP_MOVE: Choices,
    LAST_SEQUENCE_S_LENGTH: [1, 2, 3, 4, '5+'],
    PATTERN_S_NEXT_CHOICE: Choices + ['N']

}