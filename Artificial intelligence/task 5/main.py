import sys
import pandas as pd
from numpy.typing import NDArray
from PyQt6 import QtWidgets as W
from scipy.spatial import distance_matrix

def algo_continuous(
        x_train: NDArray,
        y_train: NDArray,
        x_test: NDArray
) -> NDArray:
    return y_train[distance_matrix(x_train, x_test).argmin(axis=0)]


app = W.QApplication(sys.argv)

df = pd.read_csv('mnist_test.csv').to_numpy()
x0_train, y0_train = df[:1000, 1:], df[:1000, 0]
x1_train, y1_train = df[1000:2000, 1:], df[1000:2000, 0]
x0_test, y0_test = df[2000:2200, 1:], df[2000:2200, 0]
x1_test, y1_test = df[2200:2400, 1:], df[2200:2400, 0]

y0_preds = algo_continuous(x0_train, y0_train, x0_test)
y1_preds = algo_continuous(x1_train, y1_train, x1_test)

accuracies = [
    (y0_preds == y0_test).astype('float32').mean(),
    (y1_preds == y1_test).astype('float32').mean(),
]

class MainWindow(W.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.widget = W.QWidget()
        self.text = W.QLabel()
        self.layout = W.QVBoxLayout(self.widget)
        for w in [self.text]:
            self.layout.addWidget(w)

        lines = [
            f'T{i} accuracy: {acc}'
            for i, acc in enumerate(accuracies)
        ]

        lines.append(f'T0 labels (real, preds):')
        for j in range(10):
            lines.append(f'{y0_test[j], y0_preds[j]}')
        lines.append(f'T1 labels (real, preds):')
        for j in range(10):
            lines.append(f'{y1_test[j], y1_preds[j]}')

        self.text.setText('\n'.join(lines))
        self.setCentralWidget(self.widget)


mw = MainWindow()
mw.show()
app.exec()