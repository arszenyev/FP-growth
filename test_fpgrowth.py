import unittest

from random import randint, sample
from timeit import default_timer as timer

from fp_growth import process_and_get_patterns
from apriori import do_apriori
from samples import han_et_al_2000, han_data_1, han_data_2, crazy_ronnys_college_stuff_emporium, D, some_data,\
    IdaSamson, SoftwaretestingHelp


samples = {
    "han_et_al_2000": han_et_al_2000,
    "han_data_1":han_data_1,
    "han_data_2": han_data_2,
    "crazy_ronnys_college_stuff_emporium": crazy_ronnys_college_stuff_emporium,
    "D": D,
    "IdaSamson": IdaSamson,
    "SoftwaretestingHelp": SoftwaretestingHelp
}


class TestFpGrowth(unittest.TestCase):

    def test__han_et_al_2000(self):
        fp_tree_patterns = [tuple(sorted(list(pattern))) for pattern in process_and_get_patterns(samples["han_et_al_2000"], 2)]
        apriori_patterns = [tuple(sorted(list(pattern))) for pattern in do_apriori(samples["han_et_al_2000"], 2)]
        self.assertTrue(all([item for item in fp_tree_patterns if item in apriori_patterns]))
        self.assertTrue(all([item for item in apriori_patterns if item in fp_tree_patterns]))



if __name__ == "__main__":
    unittest.main()