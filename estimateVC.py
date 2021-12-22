import random


def draw_random_labeled_sample(draw_random_example, sample_size):
    return [(draw_random_example(), random.randint(0, 1)) for _ in range(sample_size)]


def estimate_can_shatter(draw_random_example, can_induce, sample_size, num_trials):
    for _ in range(num_trials):
        sample = draw_random_labeled_sample(draw_random_example, sample_size)
        if not can_induce(sample):
            return False
    return True


def estimate_vc_shattering(draw_random_example, can_induce, num_trials=2000):
    # estimate a lower and upper bound on the VC dimension before performing a binary search for the VC dimension
    lower_bound = 1
    upper_bound = 1
    while estimate_can_shatter(draw_random_example, can_induce, upper_bound, num_trials):
        lower_bound = upper_bound
        upper_bound *= 2

    # perform a binary search for the estimated VC dimension
    while abs(lower_bound - upper_bound) > 1:
        middle = (lower_bound + upper_bound) // 2
        if estimate_can_shatter(draw_random_example, can_induce, middle, num_trials):
            lower_bound = middle
        else:
            upper_bound = middle

    if not estimate_can_shatter(draw_random_example, can_induce, upper_bound, num_trials):
        return lower_bound

    return upper_bound


def estimate_vc_shattering_improved(draw_random_example, can_induce, vc_prior=2):
    vc1 = estimate_vc_shattering(draw_random_example, can_induce, vc_prior * 1000)
    return estimate_vc_shattering(draw_random_example, can_induce, vc1 * 1000)
