"""
Dirty implementation of the apriori algorithm for the frequency pattern growth algorithm to be tested against
"""

from itertools import chain, combinations
from collections import Counter


def get_one_item_occurrences(data: dict):
    """
    Accumulates all items of all itemsets into a list and use the collections modules Counter method to return a dict
    with items as keys and their frequencies as values
    :param data: dict, transaction id as key, itemset as value
    :return: dict, dict with items as keys and their frequencies as values
    """
    all_items = [(item,) for item in chain.from_iterable([itemset for itemset in data.values()])]
    return dict(Counter(all_items))


def check_support(candidates, itemset, minsup):
    """
    Takes each newly generated candidate one-by-one and iterates through the whole dataset to count their supports
    :param candidates: set, set of all items of the n-1 candidates
    :param itemset: dict, the whole dataset with transaction ids as keys and itemsets as values
    :param minsup: int, the minimum support, i.e. the minimum pattern frequency of interest
    :return:
    """
    frequencies = {candidate: 0 for candidate in candidates}

    for candidate in candidates:
        for one_itemset in itemset.values():
            if set(candidate).issubset(set(one_itemset)):
                frequencies[candidate] += 1

    return {pattern: support for pattern, support in frequencies.items() if support >= minsup}


def prune_candidates(candidates: set, previous: set, n: int):
    """
    Prune the generated candidates by filtering out those the n-1 subsets of which are all frequent
    :param candidates: set, set of n element patterns as tuples
    :param previous: set, set of n-1 element, already verified patterns (tuples)
    :param n: int, number of items in the candidate patterns
    :return: set, pruned candidates
    """
    pruned = []
    for candidate in candidates:
        if all([(c in set(previous.keys())) for c in combinations(candidate, n-1)]):
            pruned.append(candidate)
    return pruned


def generate_candidates(candidates: set, n: int):
    """
    Generates n element pattern candidates from the items of the n-1 element candidates by creating all n element
    combinations
    :param candidates: set, set of all items of the n-1 candidates
    :param n: int, number of items in the candidates to be generated
    :return: set, set of patterns as tuples
    """
    return set([tuple(sorted(list(c))) for c in combinations(candidates, n)])


def do_apriori(itemset, minsup):
    """

    :param itemset: dict, the whole dataset with transaction ids as keys and itemsets as values
    :param minsup: int, the minimum support, i.e. the minimum pattern frequency of interest
    :return:
    """
    freq_items = {(k[0],): v for k, v in get_one_item_occurrences(itemset).items() if v >= minsup}
    freq_patterns = []
    n = 2
    while freq_items:
        items_ = set(chain.from_iterable(freq_items.keys()))
        candidates = generate_candidates(items_, n)
        pruned_candidates = prune_candidates(candidates, freq_items, n)
        freq_items = check_support(pruned_candidates, itemset, minsup)
        for freq_item in freq_items:
            freq_patterns.append((freq_item))
        n += 1
    return freq_patterns


if __name__ == "__main__":
    from samples import han_data_1

    for pattern in do_apriori(han_data_1,2):
        print(pattern)