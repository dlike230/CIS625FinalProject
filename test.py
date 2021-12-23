import random

from estimateVC import estimate_vc_sauer, estimate_vc_shattering
from induceLabels import union_of_intervals

if __name__ == "__main__":
    for i in range(100):
        make_example = lambda: random.random()
        induce_labels = lambda s: union_of_intervals(s, i)
        print(i, ":", estimate_vc_sauer(make_example, induce_labels))
