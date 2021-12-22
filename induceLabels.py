def union_of_intervals(s, k):
    sorted_list = sorted(s)
    num_intervals = 0
    last_labeling = 0
    for (_, label) in sorted_list:
        if label == 1 and last_labeling == 0:
            num_intervals += 1
        last_labeling = label
        if num_intervals > k:
            return False
    return True


if __name__ == "__main__":
    print(union_of_intervals(
        [(0.1574765189730678, 0), (0.18931598384519954, 0), (0.32239593085970264, 0), (0.351401408872969, 0),
         (0.4628265220930625, 0), (0.5322146538418349, 1), (0.5524520347591332, 0), (0.7856192346543641, 0)]
        , 5))
