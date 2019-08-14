from attribute_functions import *


Rock = 'R'
Paper = 'P'
Scissors = 'S'
Choices = [Rock, Paper, Scissors]

neg = {
    'PW': 'RL',
    'PL': 'SW',
    'PD': 'PD',
    'RW': 'SL',
    'RL': 'PW',
    'RD': 'RD',
    'SW': 'PL',
    'SL': 'RW',
    'SD': 'SD'
}



WIN = 'W'
DRAW = 'D'
LOSS = 'L'
NOT_AVAILABLE = 'N'

points = {
    WIN: 1,
    DRAW: 0,
    LOSS: -1
}

PAIR_TRANSLATOR ={
    "RR": "RD",
    "RP": "RL",
    "RS": "RW",
    "PR": "PW",
    "PP": "PD",
    "PS": "PL",
    "SR": "SL",
    "SP": "SW",
    "SS": "SD",



}

INDEX_OF_PLAY = 0
INDEX_OF_RESULT = 1

PATTERN_S_NEXT_CHOICE = "patterns next choice"
LAST_SEQUENCE_S_LENGTH = "last sequence length"
MOST_PLAYED_AFTER_COMP_MOVE = "most played after <comp move>"
MOST_SUCCESSFUL = "most successful"
MOST_SUCCESSFUL_IN_LAST_5 = "most successful in last 5"
MOST_PLAYED_IN_LAST_10 = "most played in last 10"
MOST_PLAYED = "most played"
LAST_PLAYED = "last played"
NUM_ROCK = "num rock"
NUM_SCISSORS = "num scissors"
NUM_PAPER = "num paper"
LONGER_SEQUENCE = "longer sequence"
LAST_SEQ_ROCK = "last sequence rock"
LAST_SEQ_SCISSORS = "last sequence scissors"
LAST_SEQ_PAPER = "last sequence paper"
NUM_ROCK_IN_LAST_5 = "num rock in last 5"
NUM_SCISSORS_IN_LAST_5 = "num scissors in last 5"
NUM_PAPER_IN_LAST_5 = "num paper in last 5"
LAST_SEQ_ROCK_IN_LAST_5 = "last sequence rock in last 5"
LAST_SEQ_SCISSORS_IN_LAST_5 = "last sequence scissors in last 5"
LAST_SEQ_PAPER_IN_LAST_5 = "last sequence paper in last 5"
NUM_ROCK_IN_LAST_10 = "num rock in last 10"
NUM_SCISSORS_IN_LAST_10 = "num scissors in last 10"
NUM_PAPER_IN_LAST_10 = "num paper in last 10"
LAST_SEQ_ROCK_IN_LAST_10 = "last sequence rock in last 10"
LAST_SEQ_SCISSORS_IN_LAST_10 = "last sequence scissors in last 10"
LAST_SEQ_PAPER_IN_LAST_10 = "last sequence paper in last 10"
attribute_names = [LAST_PLAYED, MOST_PLAYED, MOST_PLAYED_IN_LAST_10, MOST_SUCCESSFUL, MOST_SUCCESSFUL_IN_LAST_5,
                   MOST_PLAYED_AFTER_COMP_MOVE, LAST_SEQUENCE_S_LENGTH, PATTERN_S_NEXT_CHOICE, NUM_ROCK, NUM_SCISSORS,
                   NUM_PAPER, LONGER_SEQUENCE, LAST_SEQ_ROCK, LAST_SEQ_SCISSORS, LAST_SEQ_PAPER,
                   NUM_ROCK_IN_LAST_5,NUM_PAPER_IN_LAST_5,NUM_SCISSORS_IN_LAST_5,
                   NUM_ROCK_IN_LAST_10,NUM_PAPER_IN_LAST_10,NUM_SCISSORS_IN_LAST_10,
                   LAST_SEQ_ROCK_IN_LAST_5,LAST_SEQ_PAPER_IN_LAST_5,LAST_SEQ_SCISSORS_IN_LAST_5,
                   LAST_SEQ_ROCK_IN_LAST_10,LAST_SEQ_PAPER_IN_LAST_10,LAST_SEQ_SCISSORS_IN_LAST_10]
num_rock = num_smth(Rock)
num_scissors = num_smth(Scissors)
num_paper = num_smth(Paper)
last_seq_rock = sequence_smth(Rock)
last_seq_paper = sequence_smth(Paper)
last_seq_scissors = sequence_smth(Scissors)
num_rock_in_last_5 = num_smth_in_last_x(Rock, 5)
num_scissors_in_last_5 = num_smth_in_last_x(Scissors, 5)
num_paper_in_last_5 = num_smth_in_last_x(Paper, 5)
last_seq_rock_in_last_5 = sequence_smth_in_last_x(Rock, 5)
last_seq_paper_in_last_5 = sequence_smth_in_last_x(Paper, 5)
last_seq_scissors_in_last_5 = sequence_smth_in_last_x(Scissors, 5)
num_rock_in_last_10 = num_smth_in_last_x(Rock, 10)
num_scissors_in_last_10 = num_smth_in_last_x(Scissors, 10)
num_paper_in_last_10 = num_smth_in_last_x(Paper, 10)
last_seq_rock_in_last_10 = sequence_smth_in_last_x(Rock, 10)
last_seq_paper_in_last_10 = sequence_smth_in_last_x(Paper, 10)
last_seq_scissors_in_last_10 = sequence_smth_in_last_x(Scissors, 10)

attribute_functions_list = [get_last_played, get_most_played, get_most_playedd_in_last_10, get_most_successful,
                            get_most_successful_in_last_5, get_most_played_after_comp_move, get_last_sequence_length,
                            get_pattern_next_choice, num_rock, num_paper, num_scissors, longer_sequence, last_seq_rock,
                            last_seq_paper, last_seq_scissors,
                            num_rock_in_last_5, num_paper_in_last_5, num_scissors_in_last_5,
                            last_seq_rock_in_last_5, last_seq_paper_in_last_5, last_seq_scissors_in_last_5,
                            num_rock_in_last_10, num_paper_in_last_10, num_scissors_in_last_10,
                            last_seq_rock_in_last_10, last_seq_paper_in_last_10, last_seq_scissors_in_last_10]

# MAX_LAST_SEQUENCE_S_LENGTH = 5
MAX_LENGTH_FOR_EVERYTHING = 5
PARAM_MAX_LENGTH = str(MAX_LENGTH_FOR_EVERYTHING) + '+'
LENGTH_PARAMETERS = [str(num) for num in range(MAX_LENGTH_FOR_EVERYTHING)] + [PARAM_MAX_LENGTH]

parameters = {
    LAST_PLAYED: Choices,
    MOST_PLAYED: Choices,
    MOST_PLAYED_IN_LAST_10: Choices,
    MOST_SUCCESSFUL: Choices,
    MOST_SUCCESSFUL_IN_LAST_5: Choices,
    MOST_PLAYED_AFTER_COMP_MOVE: Choices + [NOT_AVAILABLE],
    LAST_SEQUENCE_S_LENGTH: LENGTH_PARAMETERS,
    PATTERN_S_NEXT_CHOICE: Choices + [NOT_AVAILABLE],
    NUM_ROCK: LENGTH_PARAMETERS,
    NUM_SCISSORS: LENGTH_PARAMETERS,
    NUM_PAPER: LENGTH_PARAMETERS,
    LONGER_SEQUENCE: Choices,
    LAST_SEQ_ROCK: LENGTH_PARAMETERS,
    LAST_SEQ_PAPER: LENGTH_PARAMETERS,
    LAST_SEQ_SCISSORS: LENGTH_PARAMETERS,
    NUM_ROCK_IN_LAST_5: LENGTH_PARAMETERS,
    NUM_PAPER_IN_LAST_5: LENGTH_PARAMETERS,
    NUM_SCISSORS_IN_LAST_5: LENGTH_PARAMETERS,
    NUM_ROCK_IN_LAST_10: LENGTH_PARAMETERS,
    NUM_PAPER_IN_LAST_10: LENGTH_PARAMETERS,
    NUM_SCISSORS_IN_LAST_10: LENGTH_PARAMETERS,
    LAST_SEQ_ROCK_IN_LAST_5: LENGTH_PARAMETERS,
    LAST_SEQ_PAPER_IN_LAST_5: LENGTH_PARAMETERS,
    LAST_SEQ_SCISSORS_IN_LAST_5: LENGTH_PARAMETERS,
    LAST_SEQ_ROCK_IN_LAST_10: LENGTH_PARAMETERS,
    LAST_SEQ_PAPER_IN_LAST_10: LENGTH_PARAMETERS,
    LAST_SEQ_SCISSORS_IN_LAST_10: LENGTH_PARAMETERS
}

print(len(attribute_names) , len(attribute_functions_list) , len(parameters))

assert len(attribute_names) == len(attribute_functions_list) == len(parameters)