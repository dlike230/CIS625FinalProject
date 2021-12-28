import random

from estimateVC import estimate_vc_sauer, estimate_vc_shattering
from induceLabels import union_of_intervals, separating_hyperplanes, rectangles

if __name__ == "__main__":
    make_example = lambda: (random.random(), random.random())
    print("Rect:", estimate_vc_sauer(make_example, rectangles))
    # for i in range(100):
    #     make_example = lambda: [random.random() for _ in range(i + 1)]
    #     print(i, ":", estimate_vc_shattering(make_example, separating_hyperplanes))
    # for i in range(100):
    #     make_example = lambda: random.random()
    #     induce_labels = lambda s: union_of_intervals(s, i)
    #     print(i, ":", estimate_vc_sauer(make_example, induce_labels))
