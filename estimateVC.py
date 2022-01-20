import math
import random
from math import comb


def random_labeled_sample(draw_random_example, sample_size):
    return [(draw_random_example(), random.randint(0, 1)) for _ in range(sample_size)]

def estimate_can_shatter_v2(draw_random_example, can_induce, sample_size, num_trials, num_labelings=250):
    for _ in range(num_trials):
        unlabeled_sample = random_unlabeled_sample(draw_random_example, sample_size)
        success = False
        for _ in range(num_labelings):
            labeled_sample = [(x, random.randint(0, 1)) for x in unlabeled_sample]
            if not can_induce(labeled_sample):
                success = False
                break
            success = True
        if success:
            return True
    return False


def estimate_can_shatter(draw_random_example, can_induce, sample_size, num_trials):
    """
    Estimates whether a concept class can shatter some sample of a certain size
    :param draw_random_example: A function that returns a random example from any arbitrary distribution
    :param can_induce: A function that takes in a labeled sample and returns whether the concept class of interest
                       can produce that labeling on that sample.
    :param sample_size: The sample size to test
    :param num_trials: How many randomized trials to run
    :return:
    """
    for _ in range(num_trials):
        labeled_sample = random_labeled_sample(draw_random_example, sample_size)
        if not can_induce(labeled_sample):
            return False
    return True


def phi(d, m):
    return sum(comb(m, i) for i in range(d + 1))


def verify_saeur(draw_random_example, can_induce, vcd, num_trials):
    """
    Checks whether phi(d, m) is too small for the given vc dimension. If it is, return that the proposed
    vcd is inconsistent with Sauer's lemma.
    :param draw_random_example: Function for returning a random example
    :param can_induce: Function that takes in a labeled sample and returns whether that labeling can be induced
    :param vcd: The proposed vc-dimension
    :param num_trials: The number of trials to use for estimation
    :return:
    """
    total_labelings_induced = 0
    sample_size = vcd * 2
    for _ in range(num_trials):
        labeled_sample = random_labeled_sample(draw_random_example, sample_size)
        if can_induce(labeled_sample):
            total_labelings_induced += 1

    if total_labelings_induced == 0:
        return False

    est_labels_induced = (total_labelings_induced / num_trials) * (2 ** sample_size)

    return est_labels_induced >= phi(vcd, sample_size)


def estimate_vc_bin_search(draw_random_example, can_induce, consistent_vc):
    """
    A meta-algorithm for estimating the VC dimension
    :param draw_random_example: Draw a random example from the distribution
    :param can_induce: Function that takes in a labeled sample and returns whether that labeling can be induced
    :param consistent_vc: A function that uses some metric to determine whether a given vc dimension is consistent
                          with empirical data.
    :return: An estimate of the VC dimension
    """
    # estimate a lower and upper bound on the VC dimension before performing a binary search for the VC dimension
    lower_bound = 1
    upper_bound = 1
    while consistent_vc(draw_random_example, can_induce, upper_bound):
        lower_bound = upper_bound
        upper_bound *= 2

    # perform a binary search for the estimated VC dimension
    while abs(lower_bound - upper_bound) > 1:
        middle = (lower_bound + upper_bound) // 2
        if consistent_vc(draw_random_example, can_induce, middle):
            lower_bound = middle
        else:
            upper_bound = middle

    if not consistent_vc(draw_random_example, can_induce, upper_bound):
        return lower_bound

    return upper_bound


def estimate_vc_shattering(draw_random_example, can_induce, num_trials=500):
    """
    Estimates the VC dimension based on an estimate of how many examples can be shattered
    :param draw_random_example:
    :param can_induce:
    :param num_trials:
    :return:
    """
    consistent_vc = lambda draw, check, sample_size: estimate_can_shatter_v2(draw, check, sample_size, num_trials)
    return estimate_vc_bin_search(draw_random_example, can_induce, consistent_vc)


def estimate_vc_sauer(draw_random_example, can_induce, num_trials=2000):
    """
    Estimates the VC dimension based on how closely the estimated number of labellings that can be induced matches
    Sauer's lemma
    :param draw_random_example:
    :param can_induce:
    :param num_trials:
    :return:
    """
    consistent_vc = lambda draw, check, vc: verify_saeur(draw, check, vc, num_trials)
    return estimate_vc_bin_search(draw_random_example, can_induce, consistent_vc)
