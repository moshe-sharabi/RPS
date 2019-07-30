from attribute_functions import *
from Constants import *

def read_histories(path):
    """
    parses the file to get a list of attributes according to the histories in the file
    :param path: the path of file
    :return: a list of attributes per history
    """
    file_str = open(path).read()
    histories_str = file_str.split("\n")
    histories_str = [history.split(" ") for history in histories_str if history] #if history is not empty

    return histories_str

def get_parameters_and_predictions_for_history_length(games, length):
    """
    for every game that is long enough returns a list of parameters (one for every attribute) and the player's next move.
    also returns the games that were long enough.
    :param games: the games we learn from
    :param length: the length of the history we want to learn
    """

    if length == 0:
        # returns only a prediction (most played on first match)
        played = [game[0][INDEX_OF_PLAY] for game in games]
        return get_most_played(played)

    long_enough_games = []
    parameters_and_predictions = []
    for game in games:
        if len(game) >= length+1:
            long_enough_games.append(game)
            game_parameters = [func(game[:length])for func in attribute_functions]
            game_prediction = game[length][INDEX_OF_PLAY]
            parameters_and_predictions.append(game_parameters + [game_prediction])
    return parameters_and_predictions, long_enough_games