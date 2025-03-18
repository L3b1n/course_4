from numpy.typing import NDArray
from scipy.spatial import distance_matrix


def algo_continuous(
        x_train: NDArray,
        y_train: NDArray,
        x_test: NDArray
) -> NDArray:
    return y_train[distance_matrix(x_train, x_test).argmin(axis=0)]
