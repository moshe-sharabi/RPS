from decision_tree import *
from attribute_functions import *
from Constants import *
import glob
import random

TREE_FILE_PREFIX = 'tree_'
LEN_EPOCH = 7
ROCK_IND = 0
PAPER_IND = 1
SCISSORS_IND = 2


class Dummy:
    def __init__(self, idk):
        self.idk = idk

    def best_counter(self):
        return self.idk


class RandomAgent:
    @staticmethod
    def predict(history):
        # return random.choice([Rock, Paper, Scissors])
        return Prediction(0, 0, 0)


class ReflexAgent:
    def predict(self, history):
        if not history:
            return Prediction(0, 0, 0)
        return Prediction(history)


def read_histories(path):
    """
    parses the file to get a list of attributes according to the histories in the file
    :param path: the path of file
    :return: a list of attributes per history
    """
    # get update from git:
    command = 'git checkout master -- ' + path
    # print(command)
    os.system(command)
    file_str = open(path).read()
    histories_str = file_str.split("\n")
    histories_str = [history.split(" ") for history in histories_str if history]  # if history is not empty
    for hist_str in histories_str:
        if hist_str[-1] not in neg:
            hist_str.pop()

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
        if len(game) >= length + 1:
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
            new_tree.train(new_examples)
        all_trees[length] = new_tree
        new_tree.save_tree(os.path.join(AI_agent.tree_folder, TREE_FILE_PREFIX + str(length)))
        length = next_length
    return all_trees, all_examples


class AI_agent:
    # constants:
    jumping_iterations = [0, 1, 2, 3, 4, 5, 10]
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
                self.all_trees, self.all_examples = self.build()
                return
            new_tree = DecisionTree()
            new_tree.parse_tree_dic(os.path.join(AI_agent.tree_folder, TREE_FILE_PREFIX + str(length)))
            self.all_trees.append(new_tree)

    def build(self):
        return build_trees(AI_agent.example_files)

    def predict(self, history):
        for length in self.jumping_iterations[::-1]:
            if len(history) >= length:
                if length == 0:
                    return self.all_trees[length].predict(None)
                example = np.array(get_parameters(history))
                return self.all_trees[AI_agent.jumping_iterations.index(length)].predict(example)

    def get_relevant_tree(self, history_length):
        for length in self.jumping_iterations[::-1]:
            if history_length >= length:
                return self.all_trees[AI_agent.jumping_iterations.index(length)]


class Ai2:

    def __init__(self, epoch, starting_at, gamma1):
        self.trees = []
        self.epoch = epoch
        self.starting_at = starting_at
        self.gamma = gamma1
        self.counter = 0
        self.epoch_examples = []
        self.entire_history = []
        # self.last_play = Paper
        self.basic_ai = AI_agent()
        self.trees.append(self.basic_ai.get_relevant_tree(0))

    def get_tree_score(self, tree):
        score = 0
        for i in range(self.epoch):
            hist = self.entire_history[:-i - 1]
            played = self.entire_history[-i - 1][INDEX_OF_PLAY]
            if tree.predict(get_parameters(hist)).best_counter() == played:
                score += self.epoch - i
        return score

    def tree_voting(self, example):
        trees_by_relevant = sorted(self.trees, key=lambda x: self.get_tree_score(x), reverse=True)
        votes = Counter()
        for i in range(len(trees_by_relevant)):
            cur_prediction = trees_by_relevant[i].predict(example)
            cur_power = np.power(self.gamma, len(trees_by_relevant) - 1 - i)
            votes[Rock] += cur_prediction.rock_percentage * cur_power
            votes[Paper] += cur_prediction.scissors_percentage * cur_power
            votes[Scissors] += cur_prediction.paper_percentage * cur_power
        return Prediction(votes[Rock], votes[Scissors], votes[Paper])

    def get_wins(self, entire_history):
        c = Counter()
        for game in entire_history:
            c[game[INDEX_OF_RESULT]] += 1
        print("L:" + str(c[LOSS] / len(entire_history)) + "\n" +
              "W:" + str(c[WIN] / len(entire_history)) + "\n" +
              "d:" + str(c[DRAW] / len(entire_history)))

    def predict(self, history):
        self.entire_history = history
        self.trees[0] = self.basic_ai.get_relevant_tree(len(history))
        if len(history) > self.starting_at:
            self.counter += 1
            example = get_parameters(history[:-1]) + [history[-1][INDEX_OF_PLAY]]
            self.epoch_examples.append(example)
            if self.counter == self.epoch:
                cur_tree = DecisionTree()
                cur_tree.train(np.array(self.epoch_examples))
                self.trees.append(cur_tree)
                self.epoch_examples = []
                self.counter = 0
        if len(self.trees) == 1:
            return self.basic_ai.predict(history)
        return self.tree_voting(get_parameters(history))


class OnlineEpochAgent:

    def __init__(self, epoch, round1, gamma1):
        self.trees = []
        self.epoch = epoch
        self.round = round1
        self.gamma = gamma1
        self.counter = 0
        self.epoch_examples = []
        self.cur_round = []
        self.entire_history = []
        self.last_play = Paper
        new_tree = DecisionTree()
        if self.round > 5:
            new_tree.parse_tree_dic(os.path.join(AI_agent.tree_folder, TREE_FILE_PREFIX + str(5)))
        else:
            new_tree.parse_tree_dic(os.path.join(AI_agent.tree_folder, TREE_FILE_PREFIX + str(self.round)))
        self.trees.append(new_tree)

    def tree_voting(self):
        if len(self.entire_history) < self.round:
            return random.choice(Choices)
        cur_history = self.entire_history[-self.round:]
        example = get_parameters(cur_history)
        votes = {Rock: 0, Paper: 0, Scissors: 0}
        for i in range(len(self.trees)):
            cur_prediction = self.trees[i].predict(example)
            rock_percentage, paper_percentage, scissors_percentage = cur_prediction.best_counter_precentage()
            cur_power = np.power(self.gamma, len(self.trees) - 1 - i)
            votes[Rock] += rock_percentage * cur_power
            votes[Paper] += paper_percentage * cur_power
            votes[Scissors] += scissors_percentage * cur_power
        return max(votes.keys(), key=(lambda x: votes[x]))

    def get_wins(self):
        c = Counter()
        for game in self.entire_history:
            c[game[INDEX_OF_RESULT]] += 1
        print("L:" + str(c[LOSS] / len(self.entire_history)) + "\n" +
              "W:" + str(c[WIN] / len(self.entire_history)) + "\n" +
              "d:" + str(c[DRAW] / len(self.entire_history)))

    def predict(self, history):
        if len(history) == 0:
            return Dummy(self.last_play)
        previous_play = history[-1]
        self.counter += 1
        if self.counter == self.round:
            example = get_parameters(self.cur_round) + [previous_play[INDEX_OF_PLAY]]
            self.epoch_examples.append(example)
            if len(self.epoch_examples) == self.epoch:
                cur_tree = DecisionTree()
                cur_tree.train(np.array(self.epoch_examples))
                self.trees.append(cur_tree)
                self.epoch_examples = []
            self.counter = 0
            self.cur_round = []
        else:
            self.cur_round.append(previous_play)
        self.entire_history.append(previous_play)
        self.last_play = self.tree_voting()
        return Dummy(self.last_play)


class OnlineSingleTreeAgent:

    def __init__(self, epoch, round1):
        self.tree = None
        self.epoch = epoch
        self.round = round1
        self.counter = 0
        self.round_counter = 0
        self.all_examples = []
        self.cur_round = []
        self.entire_history = []
        self.last_play = Paper
        new_tree = DecisionTree()
        if self.round > 5:
            new_tree.parse_tree_dic(os.path.join(AI_agent.tree_folder, TREE_FILE_PREFIX + str(5)))
        else:
            new_tree.parse_tree_dic(os.path.join(AI_agent.tree_folder, TREE_FILE_PREFIX + str(self.round)))
        self.tree = new_tree

    def get_wins(self):
        c = Counter()
        for game in self.entire_history:
            c[game[INDEX_OF_RESULT]] += 1
        print("L:" + str(c[LOSS] / len(self.entire_history)) + "\n" +
              "W:" + str(c[WIN] / len(self.entire_history)) + "\n" +
              "d:" + str(c[DRAW] / len(self.entire_history)))

    def predict(self, history):
        if len(history) == 0:
            return Dummy(self.last_play)
        previous_play = history[-1]
        self.counter += 1
        if self.counter == self.round:
            example = get_parameters(self.cur_round) + [previous_play[INDEX_OF_PLAY]]
            self.all_examples.append(example)
            if self.round_counter == self.epoch:
                cur_tree = DecisionTree()
                cur_tree.train(np.array(self.all_examples))
                self.tree = cur_tree
                self.round_counter = 0
            else:
                self.round_counter += 1
            self.counter = 0

            self.cur_round = []
        else:
            self.cur_round.append(previous_play)
        self.entire_history.append(previous_play)
        if len(self.entire_history) < self.round:
            self.last_play = random.choice(Choices)
            return Dummy(self.last_play)
        cur_history = self.entire_history[-self.round:]
        example = get_parameters(cur_history)
        rock_percentage, paper_percentage, scissors_percentage = self.tree.predict(example).best_counter_precentage()
        precentage = {Rock: rock_percentage, Scissors: scissors_percentage, Paper: paper_percentage}
        self.last_play = max(precentage.keys(), key=(lambda x: precentage[x]))

        return Dummy(self.last_play)


if __name__ == "__main__":
    flag = True
    idk = OnlineEpochAgent(5, 3, 0.9)
    last_choice = None
    our_choice = None
    for i in range(2):
        for j in range(15):
            our_choice = idk.predict(last_choice)
            last_choice = input("your_choice")
            print("our choice:" + our_choice + "\n")
    idk.get_wins()
