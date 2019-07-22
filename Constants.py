Rock = 'R'
Paper = 'P'
Scissors = 'S'
Choices = [Rock, Paper, Scissors]

PATTERN_S_NEXT_CHOICE = "pattern's next choice"
LAST_SEQUENCE_S_LENGTH = "last sequence's length"
PLAYED_AFTER_COMP_MOVE = "most played after <comp move>"
MOST_SUCCESSFUL = "most successful"
MOST_PLAYED_IN_LAST_10 = "most played in last 10"
MOST_PLAYED = "most played"
LAST_PLAYED = "last played"
attribute_names = [LAST_PLAYED, MOST_PLAYED, MOST_PLAYED_IN_LAST_10, MOST_SUCCESSFUL, PLAYED_AFTER_COMP_MOVE, LAST_SEQUENCE_S_LENGTH, PATTERN_S_NEXT_CHOICE]

parameters = {
    LAST_PLAYED: Choices,
    MOST_PLAYED: Choices,
    MOST_PLAYED_IN_LAST_10: Choices,
    MOST_SUCCESSFUL: Choices,
    PLAYED_AFTER_COMP_MOVE: Choices,
    LAST_SEQUENCE_S_LENGTH: [1, 2, 3, 4, '5+'],
    PATTERN_S_NEXT_CHOICE: Choices + ['N']

}