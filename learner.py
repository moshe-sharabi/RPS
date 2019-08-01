import os
import random

from decision_tree import *
from attribute_functions import *
from Constants import *
import glob

TREE_FILE_PREFIX = 'tree_'


class Reflex_agent:

    def predict(self, history):
        return Prediction(history)

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


def get_parameters(history):
    return [func(history) for func in attribute_functions_list]


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
        return Prediction(played), games

    long_enough_games = []
    parameters_and_predictions = []
    for game in games:
        if len(game) >= length+1:
            long_enough_games.append(game)
            history = game[:length]
            game_parameters = get_parameters(history)
            game_prediction = game[length][INDEX_OF_PLAY]
            parameters_and_predictions.append(game_parameters + [game_prediction])
    return parameters_and_predictions, long_enough_games


def build_trees(example_files):
    global all_examples, all_trees
    example_games = []
    for path in example_files:
        example_games += read_histories(path)

    all_examples = []
    all_trees = dict()
    length = 0
    while example_games:
        examples = []
        new_examples, example_games = get_parameters_and_predictions_for_history_length(example_games, length)
        next_length = length + 1
        while next_length not in AI_agent.jumping_iterations and example_games:
            examples, example_games = get_parameters_and_predictions_for_history_length(example_games, next_length)
            new_examples += examples
            next_length += 1

        all_examples.append(new_examples)
        new_tree = DecisionTree()
        if length == 0:  # examples is a Prediction for player's move. assuming (1 in jumping_iterations)
            new_tree.root = Node(leaf=True, label=new_examples)
        else:
            new_examples = np.array(new_examples)
            new_tree.CART(new_examples)
        all_trees[length] = new_tree
        new_tree.save_tree(os.path.join(AI_agent.tree_folder, TREE_FILE_PREFIX + str(length)))
        length = next_length
    return all_trees, all_examples


class AI_agent:
    # constants:
    jumping_iterations = [0,1,2,3,4,5]
    example_folder_name = 'examples'
    example_folder = os.path.join('.', example_folder_name)
    tree_folder_name = 'trees'
    tree_folder = os.path.join('.', tree_folder_name)
    example_files = glob.glob(os.path.join(example_folder, '*.txt'))
    tree_files = glob.glob(os.path.join(tree_folder, '*'))

    def __init__(self):
        self.all_trees = []
        self.all_examples = []
        for length in AI_agent.jumping_iterations:
            if os.path.join(AI_agent.tree_folder, TREE_FILE_PREFIX + str(length)) not in AI_agent.tree_files:
                self.build()
                return
            new_tree = DecisionTree()
            new_tree.parse_tree_dic(os.path.join(AI_agent.tree_folder, TREE_FILE_PREFIX + str(length)))
            self.all_trees.append(new_tree)


    def build(self):
        self.all_trees, self.all_examples = build_trees(AI_agent.example_files)

    def predict(self, history):
        for length in AI_agent[::-1]:
            if len(history) >= length:
                if length == 0:
                    return self.all_trees[length].predict(None)
                return self.all_trees[length].predict(get_parameters(history))

def main():
    ai = AI_agent()
    # ai.build()