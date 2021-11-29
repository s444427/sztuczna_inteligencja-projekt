import copy
import operator
from collections import Counter

import numpy as np

from src.cases import *


class Node:
    def __init__(self, Class, tag=None):
        self.Class = Class
        self.childs = []


def classes_of_cases(cases):
    classes = []
    for case in cases:
        if case.Class not in classes:
            classes.append(case.Class)
    return classes


def count_classes(cases):
    classes = []
    for case in cases:
        classes.append(case.Class)
    c = Counter(classes)
    return max(c.items(), key=operator.itemgetter(1))[0]


def chose_attribute(cases, attributes):
    a = ""
    max = float("-inf")
    for attribute in attributes:
        if I(cases) - E(cases, attribute) >= max:
            max = I(cases) - E(cases, attribute)
            a = attribute
    return a


def I(cases):
    i = 0
    all = len(cases)
    classes = classes_of_cases(cases)
    for Class in classes:
        noc = 0
        for case in cases:
            if case.Class == Class:
                noc += 1
        i -= (noc / all) * np.log2(noc / all)
    return i


def E(cases, attribute):
    e = 0
    values = []
    index = cases[0].attributes.index(attribute)
    for case in cases:
        if case.values[index] not in values:
            values.append(case.values[index])
    for value in values:
        ei = []
        for case in cases:
            if case.values[index] == value:
                ei.append(case)
        e += (len(ei) / len(cases)) * I(ei)
    return e


def treelearn(cases, attributes, default_class):
    if cases == []:
        t = Node(default_class)
        return t
    if len(classes_of_cases(cases)) == 1:
        t = Node(cases[0].Class)
        return t
    if attributes == []:
        t = Node(count_classes(cases))
        return t
    A = chose_attribute(cases, attributes)
    t = Node(A)
    new_default_class = count_classes(cases)

    values = []
    index = attributes.index(A)
    for case in cases:
        if case.values[index] not in values:
            values.append(case.values[index])

    for value in values:
        new_cases = []
        for case in cases:
            if case.values[index] == value:
                new_case = copy.deepcopy(case)
                new_case.values = case.values[:index] + case.values[index + 1:]
                new_case.attributes = case.attributes[:index] + case.attributes[index + 1:]
                new_cases.append(new_case)
        new_attributes = attributes[:index] + attributes[index + 1:]
        child = treelearn(new_cases, new_attributes, new_default_class)
        t.childs.append([child, value])

    return t


def pretty_print(root, n):
    if len(root.childs) == 0:
        for _ in range(n):
            print("    ", end="")
        print("return " + str(root.Class))
    for child in root.childs:
        for _ in range(n):
            print("    ", end="")
        if child != root.childs[0]:
            print("el", end="")
        if len(str(child[1])) > 1:
            print("if self." + str(root.Class) + " == \"" + str(child[1]) + "\":")
        else:
            print("if self." + str(root.Class) + " == " + str(child[1]) + ":")
        pretty_print(child[0], n + 1)


# Get view of decision_tree.py
if __name__ == "__main__":
    tree = treelearn(cases, attributes, 0)
    pretty_print(tree, 0)
