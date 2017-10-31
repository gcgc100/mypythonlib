#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv


def tree_to_CSV(root, csvfile, header=None, get_data=None, get_children=None,
                get_parent=None, csvConf={}):
    """save a tree to csvfile, the leaf of the tree must be all the same depth

    :root: TODO
    :csvfile: TODO
    :get_data: TODO
    :get_leaf_nodes: TODO
    :get_parent: TODO
    :csvConf: TODO
    :returns: TODO

    """
    get_data, get_children, get_parent = \
        __setDefaultTreeFunc(get_data,
                             get_children,
                             get_parent)

    def get_leaf_nodes(root):
        if root is not None:
            leafs = []
            children = get_children(root)
            if len(children) == 0:
                leafs.append(root)
            for n in children:
                leafs += get_leaf_nodes(n)
            return leafs

    leafs = get_leaf_nodes(root)
    writer = csv.writer(csvfile, **csvConf)
    depth = None
    if header is not None:
        depth = len(header)
        writer.writerow(header)
    for l in leafs:
        row = []
        node = l
        while node is not None:
            row.insert(0, get_data(node))
            node = get_parent(node)
        if depth is None:
            depth = len(row)
        else:
            assert depth == len(row)
        writer.writerow(row)


def __setDefaultTreeFunc(get_data, get_children, get_parent):
    """set the default tree function for treeToCSV

    :get_data: TODO
    :get_children: TODO
    :get_parent: TODO
    :returns: TODO

    """
    if get_data is None:
        def get_data(node):
            return node.__str__()
    if get_children is None:
        def get_children(node):
            return node.children
    if get_parent is None:
        def get_parent(node):
            return node.parent
    return get_data, get_children, get_parent
