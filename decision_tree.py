import numpy as np
from util import Counter
from scipy.stats import *
from Constants import *
import json

#############################################
# constants:
#############################################

Rock = 'R'
Paper = 'P'
Scissors = 'S'
Choices = [Rock, Paper, Scissors]

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
            histories_attributes.append([func(history)for func in attribute_functions])
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
        att_examples = examples[examples[:, index_of_attribute] == param]
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
    node_dic["samples"] = node.samples
    node_dic['attribute'] = node.feature
    node_dic["theta"] = node.theta
    node_dic["label"] = node.label
    if node.leaf:
        node_dic['children'] = None
        return node_dic
    else:
        node_dic['children'] = [save_tree_helper(child) for child in node.children]
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
    cur_node = Node(leaf=dic['leaf'], samples=dic['samples'], attribute=dic['attribute'], label=dic['label'])
    if dic['leaf']:
        return cur_node
    else:
        cur_children = [parse_dic_helper(child) for child in dic["children"]]
        cur_node.children = cur_children
        return cur_children


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

    def CART(self, examples, available_indexes):
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
        if len(examples) == 0:
            return Node(leaf=True, label=1)

        if all_same(examples[:,-1]):  # if all the samples classifications are the same
            return Node(leaf=True, label=examples[0,-1])

        best_attribute_index = self.find_classification(examples, available_indexes)
        remaining_indexes = available_indexes.copy()
        remaining_indexes.remove(best_attribute_index)

        children = []
        for param in parameters[attribute_names[best_attribute_index]]:
            children.append(self.CART(examples[examples[:,best_attribute_index == param]], remaining_indexes))

        return Node(leaf=False, samples=examples, attribute=best_attribute_index,
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
            ig = H_ex - get_ig(index, examples)
            igr = ig / iv
            igrs[index] = igr
        best_att_index = max(igrs, key=lambda x: igrs[x])

        return best_att_index



    def predict(self, X):
        """
        Returns
        -------
        y_hat : a prediction vector for X
        """
        res = []
        for x in X:
            res.append(self.label_value(x, self.root))
        return np.array(res)


    def label_value(self, x, node):
        """
        returns the prediction for x on the decision tree starting at node.
        """
        if node.leaf:
            return node.label
        return self.label_value(x, node.left) if x[node.feature] <= node.theta else \
            self.label_value(x, node.right)


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


