import os
import random

from decision_tree import *
from attribute_functions import *
from Constants import *
import glob

class Reflex_agent:

    def predict(self, history):
        return Prediction(history).best_counter()

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
        played = [game[0] for game in games]
        return get_most_played(played)

    long_enough_games = []
    parameters_and_predictions = []
    for game in games:
        if len(game) >= length+1:
            long_enough_games.append(game)
            game_parameters = [func(game[:length]) for func in attribute_functions_list]
            game_prediction = game[length][INDEX_OF_PLAY]
            parameters_and_predictions.append(game_parameters + [game_prediction])
    return parameters_and_predictions, long_enough_games


# main:
example_folder_name = 'examples'
example_folder = os.path.join('.', example_folder_name)
example_files = glob.glob(os.path.join(example_folder, '*.txt'))
tree_folder_name = 'trees'
tree_folder = os.path.join('.', tree_folder_name)
example_games = []
for path in example_files:
    example_games += read_histories(path)

examples = []
example, example_games = get_parameters_and_predictions_for_history_length(example_games, 1)
example = np.array(example)
# print(example)
examples.append(example)
trees = []
new_tree = DecisionTree()
# new_tree.parse_tree_dic(os.path.join(tree_folder, 'tree1'))
new_tree.CART(examples[-1])
trees.append(new_tree)
trees[-1].save_tree(os.path.join(tree_folder, 'tree' + str(len(trees))))

for _ in range(10000):
    x = example[int(random.random() * 10000)]
    y = new_tree.predict([x])
    print(x[-1], y)
