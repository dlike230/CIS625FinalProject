import math
import random


def random_labeled_sample(draw_random_example, sample_size):
    return [(draw_random_example(), random.randint(0, 1)) for _ in range(sample_size)]


def estimate_can_shatter(draw_random_example, can_induce, sample_size, num_trials):
    for _ in range(num_trials):
        labeled_sample = random_labeled_sample(draw_random_example, sample_size)
        if not can_induce(labeled_sample):
            return False
    return True


def log_phi(d, m):
    return d * math.log2(math.e * m / d)


def verify_saeur(draw_random_example, can_induce, vcd, num_trials):
    total_labelings_induced = 0
    sample_size = vcd * 2
    for _ in range(num_trials):
        labeled_sample = random_labeled_sample(draw_random_example, sample_size)
        if can_induce(labeled_sample):
            total_labelings_induced += 1

    # print(log_phi(vcd, sample_size) - sample_size, vcd, sample_size)
    # expected_labelings_induced = num_trials * (2 ** (log_phi(vcd, sample_size) - sample_size))

    if total_labelings_induced == 0:
        return True

    log_est_labels_induced = math.log2(total_labelings_induced / num_trials) + sample_size

    return log_est_labels_induced < log_phi(vcd, sample_size)


def estimate_vc_bin_search(draw_random_example, can_induce, consistent_vc):
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


def estimate_vc_shattering(draw_random_example, can_induce, num_trials=2000):
    consistent_vc = lambda draw, check, sample_size: estimate_can_shatter(draw, check, sample_size, num_trials)
    return estimate_vc_bin_search(draw_random_example, can_induce, consistent_vc)


def estimate_vc_sauer(draw_random_example, can_induce, num_trials=2000):
    consistent_vc = lambda draw, check, vc: verify_saeur(draw, check, vc, num_trials) and estimate_can_shatter(draw, check, vc, num_trials)
    return estimate_vc_bin_search(draw_random_example, can_induce, consistent_vc)
