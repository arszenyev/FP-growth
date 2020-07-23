"""
Testing the frequency pattern growth and apriori against each other, measure runtime metrics
"""

from random import randint, sample
from timeit import default_timer as timer

from fp_growth import process_and_get_patterns
from apriori import do_apriori
from samples import han_et_al_2000, han_data_1, han_data_2, crazy_ronnys_college_stuff_emporium, D, some_data,\
    IdaSamson, SoftwaretestingHelp

samples = [han_et_al_2000, han_data_1, han_data_2, crazy_ronnys_college_stuff_emporium, D, some_data, IdaSamson,
           SoftwaretestingHelp]

samples = {
    "han_et_al_2000": han_et_al_2000,
    "han_data_1":han_data_1,
    "han_data_2": han_data_2,
    "crazy_ronnys_college_stuff_emporium": crazy_ronnys_college_stuff_emporium,
    "D": D,
    "IdaSamson": IdaSamson,
    "SoftwaretestingHelp": SoftwaretestingHelp
}


letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
           "x", "y", "z"]


def generate_itemset(itemset_size: int, min_of_items: int, max_of_items: int, alphabet_slice: int):
    return [sample(letters[:alphabet_slice], randint(min_of_items, max_of_items)) for i in range(itemset_size)]


if __name__ == "__main__":

    for sample_name, sample_  in samples.items():
        print(f"fp_growth_tree against apriori for sample >> {sample_name} <<")
        fp_tree_patterns = [tuple(sorted(list(pattern))) for pattern in process_and_get_patterns(sample_, 2)]
        apriori_patterns = [tuple(sorted(list(pattern))) for pattern in do_apriori(sample_, 2)]

        print(f"    All fp tree in apriori: {all([item in apriori_patterns for item in fp_tree_patterns])}")
        print(f"    All apriori in fp tree: {all([item in fp_tree_patterns for item in apriori_patterns])}")

        for pattern in fp_tree_patterns:
            if pattern not in apriori_patterns:
                print(f"missing from apriori_patterns: {pattern}")

    id_ = "10"
    itemset = {}
    params = {
        "itemset_size": 500,
        "min_of_items": 3,
        "max_of_items": 8,
        "alphabet_slice": 24
    }
    for items_ in generate_itemset(**params):
        id_ = str(int(id_) + 10)
        itemset[id_] = items_

    start = timer()
    fp_tree_patterns = [tuple(sorted(list(pattern))) for pattern in process_and_get_patterns(itemset, 4)]
    end = timer()
    print()
    print("Random generated itemset is being processed with params:")
    print(f"        number of itemsets: {params['itemset_size']}")
    print(f"        minimum itemset size: {params['min_of_items']}")
    print(f"        maximum itemset size: {params['max_of_items']}")
    print(f"        alphabet slice: {params['alphabet_slice']}")
    print("                           ...")
    print()
    print(f">> frequency pattern growth << patterns generated in {end - start} seconds...")

    start = timer()
    apriori_patterns = [tuple(sorted(list(pattern))) for pattern in do_apriori(itemset, 4)]
    end = timer()
    print(f">> apriori  << patterns generated in {end - start} seconds...")

    print(f"    All fp tree in apriori: {all([item in apriori_patterns for item in fp_tree_patterns])}")
    print(f"    All apriori in fp tree: {all([item in fp_tree_patterns for item in apriori_patterns])}")
    print(f"    Number of patterns found {len(fp_tree_patterns)}")

    for pattern in fp_tree_patterns:
        if pattern not in apriori_patterns:
            print(f"missing from apriori_patterns: {pattern}")
