import random

from util import Counter
from scipy.stats import *
from Constants import *
import json
import numpy as np

##########################################################################################
# new!
class Prediction:

    def __init__(self, rock_percentage, paper_percentage = None, scissors_percentage = None):
        """
        usage options:
        * enter those 3 percentages
        * enter ROCK/PAPER/SCISSORS which means it is the prediction 100%
        * enter list of prediction to calculate percentages from
        """
        if scissors_percentage is not None:
            self.rock_percentage = rock_percentage
            self.paper_percentage = paper_percentage
            self.scissors_percentage = scissors_percentage
            return

        if isinstance(rock_percentage, str):
            self.rock_percentage = int(rock_percentage == Rock)
            self.paper_percentage = int(rock_percentage == Paper)
            self.scissors_percentage = int(rock_percentage == Scissors)
            return

        # in the usage case of sending all the history:
        c = Counter()
        for prediction in rock_percentage:
            c[prediction[INDEX_OF_PLAY]] += 1
        self.rock_percentage = c[Rock] / len(rock_percentage)
        self.paper_percentage = c[Paper] / len(rock_percentage)
        self.scissors_percentage = c[Scissors] / len(rock_percentage)

    def best_counter(self):
        scores = Counter()
        scores[Rock] = self.scissors_percentage - self.paper_percentage
        scores[Paper] = self.rock_percentage - self.scissors_percentage
        scores[Scissors] = self.paper_percentage - self.rock_percentage
        best_score = scores[scores.argMax()]
        choose_from = []
        for choice in Choices:
            if scores[choice] == best_score:
                choose_from.append(choice)
        if not choose_from:
            return scores.argMax()
        return random.choice(choose_from)

    def __str__(self):
        return str((self.rock_percentage, self.paper_percentage, self.scissors_percentage))

    def to_tuple(self):
        return self.rock_percentage, self.paper_percentage, self.scissors_percentage

##########################################################################################


#############################################
# ID3:
#############################################

def read_histories(path):
    """
    parses the file to get a list of attributes according to the histories in the file
    :param path: the path of file
    :return: a list of attributes per history
    """
    file_str = open(path).read()
    histories_str = file_str.split("\n")
    histories_str = [history.split(" ") for history in histories_str]
    ##histories_attributes = [[func(history)for func in attribute_functions] for history in histories_str[:-1]]
    histories_attributes = []
    for history in histories_str:
        if history[0] != "":
            histories_attributes.append([func(history) for func in attribute_functions_list])
    return histories_attributes


def get_iv(index_of_attribute, examples):
    c = Counter()
    for ex in examples:
        c[ex[index_of_attribute]] += 1
    percentages = np.array(list(c.values()))
    percentages = percentages / len(examples)
    return entropy(percentages, base=2)


def get_ig(index_of_attribute, examples):
    ig = 0
    attribute_parameters = parameters[attribute_names[index_of_attribute]]
    for param in attribute_parameters:
        indexes = examples[:, index_of_attribute] == param
        att_examples = examples[indexes]
        if len(att_examples) == 0:
            continue
        ig += (len(att_examples) / len(examples)) * get_entropy(att_examples)
    return ig

def get_entropy(examples):
    counts = []
    for choice in Choices:
        counts.append(len(examples[examples[:, -1] == choice]))
    counts = np.array(counts) / len(examples)
    return entropy(counts, base=2)

#############################################
# ID3 end
#############################################

def save_tree_helper(node):
    """
    a helper function for saving the tree as ajson file
    :param node: the node
    :return: dictionary that desribes the sub tree in the node
    """
    node_dic = {}
    node_dic["leaf"] = node.leaf
    # node_dic["samples"] = node.samples
    node_dic['attribute'] = node.attribute
    if node.leaf:
        node_dic['children'] = None
        node_dic["label"] = node.label.to_tuple()
        return node_dic
    else:
        node_dic['children'] = [save_tree_helper(child) for child in node.children]
        node_dic["label"] = node.label
        return node_dic


class Node(object):
    """ A node in a real-valued decision tree.
        Set all the attributes properly for viewing the tree after training.
    """
    def __init__(self,leaf = True,children=None,samples = 0,attribute = None,misclassification = 0,label = None):
        """
        Parameters
        ----------
        leaf : True if the node is a leaf, False otherwise
        left : left child
        right : right child
        samples : number of training samples that got to this node
        feature : a coordinate j in [d], where d is the dimension of x (only for internal nodes)
        theta : threshold over self.feature (only for internal nodes)
        label : the label of the node, if it is a leaf
        """
        self.leaf = leaf
        self.children = children
        self.samples = samples
        self.attribute = attribute
        self.label = label

def parse_dic_helper(dic):
    """
    a helper function to parse the dictionary to create a sub tree
    :param dic: dictionary describing the sub tree
    :return: the root of the sub tree
    """
    cur_node = Node(leaf=dic['leaf'], attribute=dic['attribute'], label=dic['label'])
    if dic['leaf']:
        cur_node.label = Prediction(cur_node.label)
        return cur_node
    else:
        cur_children = [parse_dic_helper(child) for child in dic["children"]]
        cur_node.children = cur_children
        return cur_node


def all_same(lst):
    cmp = lst[0]
    for obj in lst:
        if obj != cmp:
            return False
    return True


class DecisionTree(object):
    """ A decision tree for binary classification.
        max_depth - the maximum depth allowed for a node in this tree.
        Training method: CART
    """

    def __init__(self,epsilon=0.01, tree_path=None):
        self.root = None
        self.epsilon = epsilon  # todo use epsilon to prun
        if tree_path is not None:
            self.parse_tree_dic(tree_path)

    def train(self, examples):
        """
        Train this classifier over the sample (X,y)
        """
        self.root = self.CART(examples)

    def parse_tree_dic(self,  tree_path):
        """
        parsing the tree from the json file
        :param tree_path: the path of the json file
        :return: none
        """
        dic = {}
        with open(tree_path, 'r') as fp:
            dic = json.load(fp)
        fp.close()
        self.root = parse_dic_helper(dic)

    def CART(self, examples):
        """
        Gorw a decision tree with the CART method ()

        Parameters
        ----------
        X, y : sample
        A : array of d*m real features, A[j,:] row corresponds to thresholds over x_j
        depth : current depth of the tree

        Returns
        -------
        node : an instance of the class Node (can be either a root of a subtree or a leaf)
        """
        self.root = self.CART_helper(examples, set(range(len(examples[0]) - 1)))

    def CART_helper(self, examples, available_indexes):
        # print(examples)
        if len(examples) == 0:
            return Node(leaf=True, label=Prediction(Paper))
        if all_same(examples[:,
                    -1]):  # if all the samples classifications are the same
            return Node(leaf=True, label=Prediction(examples[0, -1]))
        best_attribute_index = self.find_classification(examples, available_indexes)
        if best_attribute_index is None: # all examples are the same, with different predictions
            played = examples[:,-1]
            return Node(leaf=True, label=Prediction(played))
        remaining_indexes = available_indexes.copy()
        remaining_indexes.remove(best_attribute_index)
        children = []
        for param in parameters[attribute_names[best_attribute_index]]:
            indexes = examples[:, best_attribute_index] == param
            # print("child " + param + ":")
            children.append(self.CART_helper(examples[indexes], remaining_indexes))
        return Node(leaf=False, samples=examples,
                    attribute=attribute_names[best_attribute_index],
                    children=children)

    def find_classification(self, examples, available_indexes):
        """
        finds the best values for f, theta. also returns X1,y1,X2,y2 - the groups those values divide to.

        X, y : sample
        A : array of d*m real features, A[j,:] row corresponds to thresholds over x_j
        """
        H_ex = get_entropy(examples)
        igrs = {}
        for index in available_indexes:
            iv = get_iv(index, examples)
            if iv == 0:
                continue
            ig = H_ex - get_ig(index, examples)
            igr = ig / iv
            igrs[index] = igr
        # print(igrs)

        if not igrs: # all examples are the same, with different predictions
            return None
        best_att_index = max(igrs, key=lambda x: igrs[x])

        return best_att_index


    def predict(self, X):
        """
        Returns
        -------
        y_hat : a prediction vector for X
        """
        try:
            res = []
            for x in X:
                res.append(self.label_value(x, self.root))
            return np.array(res)
        except TypeError: # X is not iterable
            return self.label_value(X, self.root)


    def label_value(self, x, node):
        """
        returns the prediction for x on the decision tree starting at node.
        :type node Node
        """
        if node.leaf:
            return node.label.best_counter()
        # todo check - I think it's fine (peleg)
        nodes_attribute_index = attribute_names.index(node.attribute)
        xs_parameter = x[nodes_attribute_index]
        children_num = parameters[node.attribute].index(xs_parameter)
        return self.label_value(x, node.children[children_num])


    def error(self, X, y):
        """
        Returns
        -------
        the error of this classifier over the sample (X,y)
        """
        return sum(np.not_equal(self.predict(X), y)) / len(y)

    def save_tree(self, path):
        """
        saves the current tree as a json file
        :param path: the path the tree wil be stored
        :return: none
        """
        dic = save_tree_helper(self.root)
        with open(path, 'w') as fp:
            json.dump(dic, fp, indent=1)
        fp.close()


