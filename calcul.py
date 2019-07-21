from scipy.stats import *
from enum import Enum
from util import *
import numpy as np


class Outlook(Enum):
    SUNNY = 1
    OVERCAST = 2
    RAINY = 3


class Temperature(Enum):
    HOT = 1
    MILD = 2
    COOL = 3


class Humidity(Enum):
    HIGH = 1
    NORMAL = 2


class Wind(Enum):
    WEAK = 1
    STRONG = 2


ex1 = [Outlook.SUNNY, Temperature.HOT, Humidity.HIGH, Wind.WEAK, False]
ex2 = [Outlook.SUNNY, Temperature.HOT, Humidity.HIGH, Wind.STRONG, False]
ex3 = [Outlook.OVERCAST, Temperature.HOT, Humidity.HIGH, Wind.WEAK, True]
ex4 = [Outlook.RAINY, Temperature.MILD, Humidity.HIGH, Wind.WEAK, True]
ex5 = [Outlook.RAINY, Temperature.COOL, Humidity.NORMAL, Wind.WEAK, True]
ex6 = [Outlook.RAINY, Temperature.COOL, Humidity.NORMAL, Wind.STRONG, False]
ex7 = [Outlook.OVERCAST, Temperature.COOL, Humidity.NORMAL, Wind.STRONG, True]
ex8 = [Outlook.SUNNY, Temperature.MILD, Humidity.HIGH, Wind.WEAK, False]
ex9 = [Outlook.SUNNY, Temperature.COOL, Humidity.NORMAL, Wind.WEAK, True]
ex10 = [Outlook.RAINY, Temperature.MILD, Humidity.NORMAL, Wind.WEAK, True]
ex11 = [Outlook.SUNNY, Temperature.MILD, Humidity.NORMAL, Wind.STRONG, True]
ex12 = [Outlook.OVERCAST, Temperature.MILD, Humidity.HIGH, Wind.STRONG, True]
ex13 = [Outlook.OVERCAST, Temperature.HOT, Humidity.NORMAL, Wind.WEAK, True]
ex14 = [Outlook.RAINY, Temperature.MILD, Humidity.HIGH, Wind.STRONG, False]

starting_examples = [ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8, ex9, ex10, ex11, ex12, ex13, ex14]
parameters_str = ['outlook', 'temperature', 'humidity', 'wind']
parameters = [Outlook, Temperature, Humidity, Wind]


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


def build_tree(available_indexes: set, examples):
    # print('\033[94m', available_indexes, '\033[0m')
    if len(examples) == 0:
        print("no examples")
        return
    if np.all(examples[:, -1]):
        print("all examples are true")
        return
    if np.all(examples[:, -1] == False):
        print("all examples are false")
        return
    H_ex = get_entropy(examples)
    igrs = {}
    for index in available_indexes:
        # print('\033[94m', index, '\033[0m')
        iv = get_iv(index, examples)
        print("iv_" + parameters_str[index] + " =", iv)
        ig = H_ex - get_ig(index, examples)
        print("ig_" + parameters_str[index] + " =", ig)
        igr = ig / iv
        print("igr_" + parameters_str[index] + " =", igr)
        igrs[index] = igr
    best_att_index = max(igrs, key=lambda x: igrs[x])
    print("\nbest attribute is " + parameters_str[best_att_index])
    remaining_indexes = available_indexes.copy()
    remaining_indexes.remove(best_att_index)
    for i in parameters[best_att_index]:
        print('\033[94m', "branch", i, ":\033[0m")
        build_tree(remaining_indexes, examples[examples[:, best_att_index] == i])


build_tree({0, 1, 2, 3}, np.array(starting_examples))
