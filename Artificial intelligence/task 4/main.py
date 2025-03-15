import sys
import pandas as pd
from algorithm import algo
from PyQt6 import QtWidgets as W


app = W.QApplication(sys.argv)


df = pd.read_csv('mnist_test.csv').to_numpy()
x, y = df[10:40, 1:], df[10:40, 0]
inconsistency, pairs = algo(x, y, 10)


class MainWindow(W.QMainWindow):
    def __init__(
            self,
    ) -> None:
        super().__init__()

        self.setWindowTitle('Кто ты?')
        self.widget = W.QWidget()
        self.text = W.QLabel()
        self.layout = W.QVBoxLayout(self.widget)
        for w in [self.text]:
            self.layout.addWidget(w)

        lines = [f'Measure of inconsistency: {inconsistency}']

        for i, (real_class, predicted) in enumerate(pairs):
            lines.append(f'{i}: Predicted: {predicted}, real: {real_class}')

        self.text.setText('\n'.join(lines))
        self.setCentralWidget(self.widget)


mw = MainWindow()
mw.show()
app.exec()