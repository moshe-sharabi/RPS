"""
===================================================
     Introduction to Machine Learning (67577)
===================================================

This module provides some useful tools for Ex4.

NOTE: To use the function view_dtree you need to install graphviz.
See https://pypi.python.org/pypi/graphviz for more details.

Author: Noga Zaslavsky

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
# from graphviz import Digraph # TODO - comment out if you didn't install graphviz


class DecisionStump(object):
    """
    Decision stump classifier
    """
    def __init__(self, D, X, y):
        self.theta = 0
        self.j = 0
        self.s = 0
        self.train(D, X, y)

    def train(self,D, X, y):
        """
        Train the classifier over the sample (X,y) w.r.t. the weights D over X

        Parameters
        ----------
        D : weights over the sample
        X, y: sample
        """
        m, d = X.shape
        F, J, theta = [0]*2, [0]*2, [0]*2
        for b in [0,1]:
            s = 2*b - 1
            F[b], theta[b], J[b] = D[y==s].sum(), X[:,0].min()-1, 0
            for j in range(d):  # go over all features
                ind = np.argsort(X[:, j])
                Xj = np.sort(X[:, j])  # sort by coordinate j
                Xj = np.hstack([Xj,Xj.max()+1])
                f = D[y==s].sum()
                for i in range(m): # check thresholds over Xj for improvement
                    f -= s*y[ind[i]]*D[ind[i]]
                    if f < F[b] and Xj[i] != Xj[i+1]:
                        F[b], J[b], theta[b] = f, j, (Xj[i]+Xj[i+1])/2
        b = np.argmin(F)
        self.theta, self.j, self.s = theta[b], J[b], 2*b-1

    def predict(self, X):
        """
        Returns
        -------
        y_hat : a prediction vector for X
        """
        y_hat = self.s*np.sign(self.theta - X[:,self.j])
        y_hat[y_hat==0] = 1
        return y_hat


class h_opt(object):
    """
    The optimal classifier for the synthetic data provided in ex4
    """
    @staticmethod
    def predict(X):

        def b(X,c,r2):
            z = X-c
            return np.sign(r2-(z*z).sum(axis=1))

        return np.sign(b(X,np.array([-.5,0]),.2)+b(X,np.array([0.45,0.5]),.4)+1)


def decision_boundaries(classifier, X, y, title_str='', weights=None):
    """
    Plot the decision boundaries of a binary classfiers over X \subseteq R^2

    Parameters
    ----------
    classifier : a binary classifier, implements classifier.predict(X)
    X : m*2 matrix whose rows correspond to the data points
    y : m dimensional vector of binary labels
    title_str : optional title
    weights : weights for plotting X
    """
    cm = ListedColormap(['#AAAAFF','#FFAAAA'])
    cm_bright = ListedColormap(['#0000FF','#FF0000'])
    h = .01  # step size in the mesh
    # Plot the decision boundary.
    x_min, x_max = X[:, 0].min() - .2, X[:, 0].max() + .2
    y_min, y_max = X[:, 1].min() - .2, X[:, 1].max() + .2
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = classifier.predict(np.c_[xx.ravel(), yy.ravel()])
    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.pcolormesh(xx, yy, Z, cmap=cm)
    # Plot also the training points
    if weights is not None: plt.scatter(X[:, 0], X[:, 1], c=y, s=weights, cmap=cm_bright)
    else: plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cm_bright)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks([])
    plt.yticks([])
    plt.title(title_str)
    plt.show()


def view_dtree(dtree, feature_names = None, class_names=None, filename='dtree'):
    """
    Cerate a graphical view of a decision tree.
    For this function to work well, you need to set correctly the attributes of each node in the tree.

    Parameters
    ----------
    dtree : DecisionTree object that follows the guidlines in the skeleton 'decision_tree.py'
    feature_names : By default the feature names are 'X[j]'. You may give a list of strings, with the same size
            as the dimension of X.
    class_names : By default the class names are the labels (e.g. 0/1). You may give a list of strings with
            custom class names.
    filename : name of the PDF file
    """
    if dtree.root is not None:

        def shape(node):
            if node.leaf:
                return 'oval'
            else:
                return 'box'

        def node_to_str(node):
            if node.leaf:
                if class_names is not None:
                    return 'label = '+class_names[node.label] +'\nsamples = %d'%node.samples
                return 'label = %d'%node.label +'\nsamples %d'%node.samples
            else:
                if feature_names is not None:
                   feature_str = feature_names[node.feature]
                else:
                    feature_str = 'X[%d'%node.feature + ']'
                return feature_str +' < %0.2f'%node.theta + '?\ninfo-gain = %0.2f'\
                      %node.gain +'\nsamples = %d'%+node.samples

        def build_dot(dot,node,path):
            if node.leaf:
                return
            else:
                left_path = path+'0'
                right_path = path+'1'
                dot.node(left_path,node_to_str(node.left),shape=shape(node.left))
                dot.node(right_path,node_to_str(node.right),shape=shape(node.right))
                dot.edge(path, left_path)
                dot.edge(path, right_path)
                build_dot(dot,node.left,left_path)
                build_dot(dot,node.right,right_path)

        dot = Digraph(filename)
        if dtree.root is not None:
            dot.node('0', node_to_str(dtree.root),shape=shape(dtree.root))
            build_dot(dot,dtree.root,'0')
            dot.view()
