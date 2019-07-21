"""
===================================================
     Introduction to Machine Learning (67577)
===================================================

Skeleton for the decision tree classifier with real-values features.
Training algorithm: CART

Author: Noga Zaslavsky
Edited: Yoav Wald, May 2018

"""
import numpy as np
from util import Counter
from scipy.stats import *

#############################################
# ID3:
#############################################

def get_iv(index_of_attribute, examples):
    c = Counter()
    for ex in examples:
        c[ex[index_of_attribute]] += 1
    percentages = np.array(list(c.values()))
    percentages = percentages / len(examples)
    return entropy(percentages, base=2)


def get_ig(index_of_attribute, examples):
    ig = 0
    param = parameters[index_of_attribute]
    for i in param:
        att_examples = examples[examples[:, index_of_attribute] == i]
        if len(att_examples) == 0:
            continue
        ig += (len(att_examples) / len(examples)) * get_entropy(att_examples)
    return ig

def get_entropy(examples):
    count_goal = len(examples[examples[:, -1] == True])
    p = count_goal / len(examples)
    return entropy((p, 1 - p), base=2)

#############################################
# ID3 end
#############################################



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


class DecisionTree(object):
    """ A decision tree for binary classification.
        max_depth - the maximum depth allowed for a node in this tree.
        Training method: CART
    """

    def __init__(self,epsilon=0.01):
        self.root = None
        self.epsilon = epsilon

    def train(self, X, y):
        """
        Train this classifier over the sample (X,y)
        """
        self.root = self.CART(X,y,np.transpose(X), 0)

    def CART(self,X, y, A, depth):
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
        if len(X) == 0:
            return Node(leaf=True, label=1)

        if np.allclose(y, y[0]):  # if all the samples classifications are the same
            return Node(leaf=True, label=y[0])

        if depth == self.max_depth:
            return Node(samples=X, label=(1 if sum(y) >=0 else -1), leaf=True)

        feature, threshhold, X1, y1, X2, y2 = self.find_classification(X, y, A)
        return Node(leaf=False, samples=X, feature=feature, theta=threshhold,
                    left=self.CART(X1, y1, np.transpose(X1), depth + 1),
                    right=self.CART(X2, y2, np.transpose(X2), depth + 1))

    def find_classification(self, X, y, A):
        """
        finds the best values for f, theta. also returns X1,y1,X2,y2 - the groups those values divide to.

        X, y : sample
        A : array of d*m real features, A[j,:] row corresponds to thresholds over x_j
        """
        best_misclass = np.inf

        for feature in range(len(A)):
            for threshhold in A[feature]:

                group_1 = X[:, feature] <= threshhold
                group_2 = np.logical_not(group_1)

                X1, y1 = X[group_1], y[group_1]
                X2, y2 = X[group_2], y[group_2]

                y1_label = 1 if sum(y1) > 0 else -1
                y2_label = 1 if sum(y2) > 0 else -1

                cur_misclass = sum(y1 != y1_label) + sum(y2 != y2_label)
                if cur_misclass < best_misclass:
                    best_misclass = cur_misclass
                    best_feature = feature
                    best_threshold = threshhold
                    best_X1 = X1
                    best_X2 = X2
                    best_y1 = y1
                    best_y2 = y2

        return best_feature, best_threshold, best_X1, best_y1, best_X2, best_y2



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