import numpy as np
from collections import Counter
from numpy.typing import NDArray
from scipy.spatial import distance_matrix


def algo(data: NDArray, labels: NDArray, l: int):
    classes = {i: [(data[i], labels[i])] for i in range(len(data))}
    while len(classes) != l:
        object = {i: np.array([z[0] for z in v]).mean(axis=0) for i, v in classes.items()}
        objects = np.stack([
            object[i].reshape(-1) for i in range(len(classes))
        ], axis=0)
        distances = distance_matrix(objects, objects)
        distances = distances + np.eye(distances.shape[0]) * distances.max()
        i, j = np.unravel_index(distances.argmin(), distances.shape)
        classes[i] = classes[i] + classes[j]
        classes.pop(j)
        classes = {i: d for i, d in enumerate(classes.values())}
    
    classes = {i: d for i, d in enumerate(classes.values())}
    pairs = []
    for k, v in classes.items():
        pairs.extend([
            (label, k) for (_, label) in v 
        ])

    class_counts = Counter([p[1] for p in pairs])
    counts = list(class_counts.items())
    counts.sort(key=lambda x: -x[1])

    a = [set() for _ in range(l)]
    for label, k in pairs:
        a[label].add(k)
    
    b = [x[1] for x in counts]
    c = [x[0] for x in counts]
    a0, b0, c0 = [], [], []

    while True:
        u = b.index(max(b))
        if c[u] not in c0:
            b0.append(b[u])
            c0.append(c[u])
            a0.append(a[u])
            if len(a0) == l:
                break
        
        else:
            b0 = [0] * l
            mx = -1
            idx = 0
            for j in range(0, l):
                if j not in c0 and b0[j] > mx:
                    mx = b0[j]
                    idx = j

            if mx == -1:
                b[u] = 0
                c[u] = -1
            else:
                b[u] = mx
                c[u] = idx

    inconsistency = (len(data) - sum(b)) / len(data)
    return inconsistency, pairs


