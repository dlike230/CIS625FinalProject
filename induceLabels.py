import numpy as np
from sklearn import metrics
from sklearn import svm


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


def separating_hyperplanes(labeled_samples):
    X = [x for x, _ in labeled_samples]
    y = [y for _, y in labeled_samples]
    if sum(y) == 0 or sum(y) == len(labeled_samples):
        return True
    clf = svm.SVC(kernel='linear')
    clf.fit(X, y)
    y_pred = clf.predict(X)
    return (metrics.accuracy_score(y_pred, y) == 1)


def rectangles(labeled_samples):
    X = [x for x, _ in labeled_samples]
    y = [y for _, y in labeled_samples]
    if len(X) == 0 or sum(y) == 0 or sum(y) == len(labeled_samples):
        return True
    positives = []
    negatives = []
    for (xi, yi) in zip(X, y):
        if yi == 1:
            positives.append(xi)
        else:
            negatives.append(xi)
    positives = np.array(positives)
    negatives = np.array(negatives)

    left = min(positives, key=lambda x: x[0])[0]
    right = max(positives, key=lambda x: x[0])[0]
    top = max(positives, key=lambda x: x[1])[1]
    bottom = min(positives, key=lambda x: x[1])[1]

    # lower_boundary = np.amin(positives)
    # upper_boundary = np.amax(positives)
    for ni in negatives:
        x, y = ni[0], ni[1]
        if left <= x <= right and bottom <= y <= top:
            return False
        # if np.all(ni > lower_boundary) and np.all(ni < upper_boundary):
        #     return False
    return True


def polynomial_classifier(labeled_samples, degree):
    X = [x for x, _ in labeled_samples]
    y = [y for _, y in labeled_samples]
    if sum(y) == 0 or sum(y) == len(labeled_samples):
        return True
    clf = svm.SVC(kernel='poly', degree=degree)
    clf.fit(X, y)
    y_pred = clf.predict(X)
    return (metrics.accuracy_score(y_pred, y) == 1)


if __name__ == "__main__":
    print(union_of_intervals(
        [(0.1574765189730678, 0), (0.18931598384519954, 0), (0.32239593085970264, 0), (0.351401408872969, 0),
         (0.4628265220930625, 0), (0.5322146538418349, 1), (0.5524520347591332, 0), (0.7856192346543641, 0)]
        , 5))
