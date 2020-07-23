
from copy import deepcopy


def deconstruct_and_remove_leaf(cond_patt_base, workbranch):
    """
    Iterating through n-1 items of an n-member conditional pattern base, while taking the subfield from the input
    dictionary with the key as the item being processed. Then it removes the subfield from the result dictionary
    with the forthcoming item. These will be put reconstructed, except the innermost subfield (i.e. the leaf node)
    :param cond_patt_base: tuple, the conditional pattern base being processed
    :param workbranch: dict, the copy of the branch being processed
    :return: archived, tuple of archived nodes for branch reconstruction
    """
    archived = ()
    for idx in range(len(cond_patt_base) - 1):
        workbranch = workbranch[cond_patt_base[idx]]
        archive = deepcopy(workbranch)
        del archive[cond_patt_base[idx + 1]]
        archived = archived + (cond_patt_base[idx], archive)
    return archived


def reconstruct_branch(archived):
    """
    Taking the tuple of archived nodes, reverse its order and rebuild the branch starting from its innermost node
    :param archived: tuple, archived nodes
    :return: dict, the branch reconstructed from the input tuple
    """
    previous_node = {}
    pruned_branch = {}
    archived_list = list(archived)
    while archived_list:
        val = archived_list.pop()
        key = archived_list.pop()
        pruned_branch = {key: val}
        if previous_node:
            pruned_branch[key][list(previous_node.keys())[0]] = list(previous_node.values())[0]
        previous_node = pruned_branch
    return pruned_branch


def remove_leaf(cond_patt_base, branch):
    """
    Removing the leaf node from the branch by passing the branch and the path through the branch to that leaf node to
    deconstructin and reconstruction functions
    :param cond_patt_base: dict, the conditional pattern base dict created in the previous walkthrough
    :param branch: dict, the barnch as rebuild by the previous rebuild
    :return: pruned_branch, dict, the branch after removal of the path already walked through (i.e. the previously found
            conditional pattern base)
    """
    archived = deconstruct_and_remove_leaf(cond_patt_base, branch)
    return reconstruct_branch(archived)


def get_subbranch(parent_node, branch):
    """
    Takes a parent node and its subbranch as input, checks if the subbranch is a leaf (by checking if "support" is the
    only field). Returns the subbranch and the support if so, or the subbranch and None.
    :param parent_node: str, the key item of the branch being investigated
    :param branch: dict, the subbranch of the branch being investigated
    :return: the subbranch being investigated and None or the support if the subbranch is a leaf
    """
    try:
        subbranch = branch[parent_node[-1]]
        if list(subbranch.keys()) == ["support"]:
            return subbranch, list(subbranch.values())[0]
        return subbranch, None
    except IndexError as e:
        print(e)


def put_into_conditionals(one_conditional, conditionals, support):
    """
    Enriching conditional pattern bases by adding  # TODO continue...
    :param one_conditional:
    :param conditionals:
    :param support:
    :return:
    """
    try:
        conditionals[one_conditional[-1]][one_conditional[:-1]] = support
    except KeyError:
        conditionals[one_conditional[-1]] = {one_conditional[:-1]: support}


def get_cond_patt_bases(branch: dict, conditionals: dict):
    """
    Mines the tree by going through a path to a leaf by choosing the first found items for each depth of a branch during
    a walkthrough. Items found during the walkthrough are saved into one a path. Once a leaf is found
    it is added to conditional pattern bases dictionary with the node item as key. The branch is then rebuild without
    the path previously been walked through and restart processing
    :param branch: dict, one branch of the tree
    :param conditionals: tree, all conditional pattern bases with the leaf branches as keys and the corresponding
                        conditional pattern bases as values (i.e. paths to the key leafs)
    """
    workbranch = branch
    path = (list(branch.keys())[0],)
    flag = {list(branch.keys())[0]: {"support": branch[list(branch.keys())[0]]["support"]}}
    while workbranch != flag:
        workbranch, support = get_subbranch(path, workbranch)
        if support:
            put_into_conditionals(path, conditionals, workbranch)
            workbranch = remove_leaf(path, branch)
            branch = workbranch
            path = ()

        nodes = [item for item in workbranch.keys() if item != "support"]
        path = path + (nodes[0],)


def process_branches(fp_tree):
    """
    Iterating through the branches of the FP-tree being processed and pass them to get_cond_patt_bases for processing
    :param fp_tree: dict, the FP-tree
    :return: dict, suffixes as keys and corresponding conditional pattern bases and their supports as values
    """
    cond_patt_bases = {}
    for branch in fp_tree.values():
        get_cond_patt_bases(branch, cond_patt_bases)
    return cond_patt_bases
