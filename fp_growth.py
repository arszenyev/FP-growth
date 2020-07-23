"""
Frequency pattern growth algorithm as described in

Data mining : concepts and techniques / Jiawei Han, Micheline Kamber, Jian Pei. – 3rd ed.
p. cm.
ISBN 978-0-12-381479-1
"""


from itertools import chain, combinations
from collections import Counter


from mine_the_tree import process_branches


def sort_by_value(itemset):
    """
    Takes a dictionary with unique items az keys and frequencies as values, returns the same dictionary with the fields
    sorted in descending order of frequencies
    :param itemset: dict, dictionary with unique items az keys and frequencies as values
    :return: dict, dictionary with the fields sorted in descending order of frequencies
    """
    return {k: v for k, v in sorted(itemset.items(), reverse=True, key=lambda item: item[1])}


def check_min_sup(occurrences: dict, min_sup: int):
    """
    Takes a dictionary of items as keys and the minimum support as value, iterates through all the fields and keeps only
    those, which has frequencies above or equal to the minimum support. The fields are sorted in descending order by
    their frequencies
    :param occurrences: dict, dictionary of items as keys and the minimum support as value
    :param min_sup: integer, minimum support value for filtering the 1-itemsets
    :return: dict, 1-itemsets filtered by minimum support and sorted in descending order by their frequencies
    """
    return sort_by_value({(item,): occurrence for item, occurrence in occurrences.items() if occurrence >= min_sup})

def get_frequencies(data: dict):
    """
    Accumulates all items of all itemsets into a list and return a dictionary with frequencies of all unique items in
    the dataset
    :param data: dict, all itemsets
    :return: dict, items as keys and frequencies of items as values
    """
    all_items = list(chain.from_iterable([list(set(itemset)) for itemset in data.values()]))
    return dict(Counter(all_items))


def get_patterns(frequent_items: dict, itemset: dict):
    """
    Collecting the occurrences list of all frequent items for each itemsets
    :param frequent_items: dict, dictionary with tuples of single frequent items as keys and their frequencies as values
    :param itemset: dict, the itemset being investigated for frequent patterns
    :return: list, list of tuples of co-occurring items
    """
    frequent_items_tuple = tuple([item[0] for item in frequent_items.keys()])
    patterns = ()
    for one_itemset in itemset.values():
        frequent_items = ()
        for frequent_item in frequent_items_tuple:
            if frequent_item in one_itemset:
                frequent_items = frequent_items + (frequent_item,)
        patterns = patterns + (frequent_items,)

    return patterns


def convert_to_dict(pattern: tuple):
    """
    (As the name implies) converts the incoming pattern into a dictionary, e.g.

        ('l2', 'l1', 'l3') -> {'l2': {'support': 1, 'l1': {'support': 1, 'l3': {'support': 1}}}}

    :param pattern: tuple, the pattern being processed
    :return: dict, one new branch of the frequency pattern tree
    """
    previous_node = None
    work_list = list(pattern)
    for idx in range(len(pattern)):
        new_key = work_list.pop(-1)
        branch = {new_key: {"support": 1}}
        if previous_node:
            branch[new_key][list(previous_node.keys())[0]] = list(previous_node.values())[0]
        previous_node = branch
    return branch


def seek_superset(pattern: tuple, tree: dict):
    """
    Takes the pattern being processed and the tree already been processed as arguments, and checks if the FP-tree has
    already a branch which starts with the first item of the pattern, i.e. is there a branch exists, into which the
    pattern has to be merged
    :param pattern: tuple, the pattern being processed, e.g. ('l2', 'l1', 'l3', 'l5')
    :param tree: dict, the tree being processed
    :return: dict, one branch of tree already processed
    """
    pattern_start = pattern[0]
    for root_node, branch in tree.items():
        if root_node == pattern_start:
            return branch


def restore_branches(other_branches_, node_key, node):
    """
    Adds all subbranches to the node being restored from the other_branches dict
    :param other_branches_:
    :param node_key:
    :param node:
    :return:
    """
    if node_key in other_branches_:
        for k, v in other_branches_[node_key].items():
            node[node_key][k] = v


def merge_remnant(reprocessed_nodes, preprocessed_remnant):
    """
    Adds the unprocessed remnant of superbranch to the last node of the reprocessed nodes thus having it reconstructed
    :param reprocessed_nodes: tuple, nodes found during attempts to get subbranches with subsequent pattern items
    :param preprocessed_remnant: dict, the remnant of the superbranch after a new node was discovered
    :return: tuple, reprocessed nodes with unprocessed part of the superbanch added to the last node
    """
    reprocessed_nodes_list = list(reprocessed_nodes)
    last_node = reprocessed_nodes_list.pop(-1)
    last_node_key = list(last_node.keys())[0]
    last_node[last_node_key] = {**last_node[last_node_key], **preprocessed_remnant}
    reprocessed_nodes_list.append(last_node)
    return tuple(reprocessed_nodes_list)


def put_it_together(reprocessed_nodes, preprocessed_remnant, other_branches):
    """
    Checks if there is unprocessed remnant, and adds it to the prepocessed if there is
    Reverse the preprocessed nodes and reconstruct the superbranch from the inside by checking if some accompanying
    branches to be added at the appropriate depth
    :param reprocessed_nodes: tuple, nodes found during attempts to get subbranches with subsequent pattern items
    :param preprocessed_remnant: dict, the remnant of the superbranch after a new node was discovered
    :param other_branches: dict, dictionary with the accompanying branches for each depths of the superbranch
    :return: dict, the reconstructed superbranch with the newly added subbranch
    """
    if preprocessed_remnant:
        reprocessed_nodes = merge_remnant(reprocessed_nodes, preprocessed_remnant)

    reprocessed_nodes_list = list(reprocessed_nodes)
    reprocessed_nodes_list.reverse()
    previous_node = {}
    for node in reprocessed_nodes_list:

        if previous_node:
            node_key = list(node.keys())[0]
            previous_key = list(previous_node.keys())[0]
            previous_value = previous_node[previous_key]
            node[node_key][previous_key] = previous_value

            restore_branches(other_branches, node_key, node)

        previous_node = node

    return node


def gather_branches(pattern, depth, preprocessed_superbranch):
    """
    Gathers all subbranches other than the one emanating form the node being processed
    :param pattern: tuple, the pattern being processed
    :param depth: int, depth being processed
    :param preprocessed_superbranch: dict, the preprocessed superbranch
    :return: dict, items as keys, and branches at items at the depth being processed
    """
    branches_at_depth = {}
    for node, branch in preprocessed_superbranch.items():
        if node not in ["support", pattern[depth]]:
            branches_at_depth[node] = branch
    return branches_at_depth


def get_other_branches(other_branches, previous_item, pattern, depth, preprocessed_superbranch):
    """
    Passes preprocessed superbranch to the gather_branches function to collect subbranches from the parent node. If
    there are other subbranches, they are
    :param other_branches: dict, parent pattern item as key, subbranches as value
    :param previous_item: str, parent pattern item
    :param pattern: tuple, pattern being examined
    :param depth: int, depth being processed
    :param preprocessed_superbranch: dict, the preprocessed superbranch
    """
    other_branches_ = gather_branches(pattern, depth, preprocessed_superbranch)
    if other_branches_:
        other_branches[previous_item] = other_branches_


def merge_branches(pattern: tuple, preprocessed_superbranch: dict):
    """
    Deconstruct the preprocessed superbranch by iterating through the pattern being processed. It is taking the items in
    the pattern and trying to get them while going deeper in the subbranch.
        If the item is the node of a subbranch at the appropriate depth of the superbranch:
            - it increments the support of the node by one
            - adds the node to the reprocessed_nodes, e.g. ('l2': {'support': 1}, 'l1': {'support': 1})
            - stores all other subbranches at depth into the other_branches, with parent node item as key and
                subbranches as value
            - takes the subbranch at the node for further processing
         If the item is not a node of any subbranches:
            - it transform the rest of the pattern into a branch (unprocessed_branch)
        The branch is reconstructed form reprocessed_nodes, other_branches and the new branch
    :param pattern: e.g. ('l2', 'l1', 'l3', 'l5')
    :param preprocessed_superbranch: e.g. {'l2': {'support': 1, 'l1': {'support': 1, 'l3': {'support': 1}}}}
    :return: dict, superbranch with new subbranch added
    """
    reprocessed_nodes = ()
    previous_item = ""
    other_branches = {}
    for depth in range(len(pattern)):
        if depth > 0:
            previous_item = pattern[depth-1]
        try:
            reprocess = {pattern[depth]: {"support": preprocessed_superbranch[pattern[depth]]["support"] + 1}}
            get_other_branches(other_branches, previous_item, pattern, depth, preprocessed_superbranch)
            preprocessed_superbranch = preprocessed_superbranch[pattern[depth]]
            del preprocessed_superbranch["support"]
            reprocessed_nodes = reprocessed_nodes + (reprocess,)
        except KeyError:
            unprocessed_branch = convert_to_dict(pattern[depth:])
            unprocessed_key = list(unprocessed_branch.keys())[0]
            if preprocessed_superbranch:
                preprocessed_superbranch[unprocessed_key] = unprocessed_branch[unprocessed_key]
                return put_it_together(reprocessed_nodes, preprocessed_superbranch, other_branches)
            else:
                preprocessed_superbranch = unprocessed_branch
                return put_it_together(reprocessed_nodes, preprocessed_superbranch, other_branches)

    return put_it_together(reprocessed_nodes, preprocessed_superbranch, other_branches)


def build_tree(pattern_list: list):
    """
    Takes the list of unique frequent item patterns and creates the frequency growth pattern tree
    :param pattern_list: list
    :return:
    """
    tree = {}
    for pattern in pattern_list:
        preprocessed_superset = seek_superset(pattern, tree)

        if preprocessed_superset:
            branch = merge_branches(pattern, preprocessed_superset)
        else:
            branch = convert_to_dict(pattern)
        tree[pattern[0]] = branch
    return tree


def build_cond_fp_tree(prefixes):
    """
    Taking the prefixes of a given suffix from the conditional pattern base builds the conditional frequency tree for
    the given suffix by generating all combinations for all prefixes and accumulates them into a dictionary with their
    frequencies as values
    :param prefixes: dict, tuples of prefix items as keys and supports as valuey
    :return: dict, patterns generated form the combinations of the prefixes as keys, and supports as values
    """

    cond_fp_tree = {}
    for prefixes_, support in prefixes.items():
        for idx in range(1, len(prefixes_) + 1):
            for comb in combinations(prefixes_, idx):
                try:
                    cond_fp_tree[comb] = cond_fp_tree[comb] + support["support"]
                except KeyError:
                    cond_fp_tree[comb] = support["support"]
    return cond_fp_tree


def extract_patterns(conditional_pattern_base, minsup):
    """
    Extracts patterns from the conditional pattern base by generating all possible combinations of the prefixes and
    checks one by one if they are a subset of the prefix patterns. Their support is the number of their occurrences
    in the prefixes multiplied by the prefix support
    :param conditional_pattern_base: dict, suffixes as keys followed by subfields with prefix patterns as keys adn their
    support as values
    :param minsup: int, minimum support
    :return: list, patterns occurring in the whole itemset with counts above the minimum support
    """
    frequent_patterns = {}
    for suffix, prefixes in conditional_pattern_base.items():
        cond_fp_tree = build_cond_fp_tree(prefixes)
        for prefixes_, support in cond_fp_tree.items():
            if support < minsup:
                continue
            frequent_patterns[prefixes_ + (suffix,)] = support
    return frequent_patterns


def process_and_get_patterns(itemset, min_sup):
    """
    Function to forward the input data and the minimum support to the appropriate functions
    :param itemset: dict, identifier as key and list of items as value
    :param min_sup: int, the minimum support
    :return:
    """
    item_frequencies = get_frequencies(itemset)
    frequent_items = check_min_sup(item_frequencies, min_sup)
    patterns = get_patterns(frequent_items, itemset)
    fp_tree = build_tree(patterns)
    conditional_pattern_base = process_branches(fp_tree)
    return extract_patterns(conditional_pattern_base, min_sup)
