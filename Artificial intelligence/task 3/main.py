import sys
from PyQt6 import QtWidgets as W
from collections import defaultdict
from algorithm import Algorithm, Statement

app = W.QApplication(sys.argv)

def read_statements(statements_file: str, statements_values: str) -> tuple[list[Statement], dict[str, list[str]]]:
    statements_ = []
    with open(statements_file, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            premise, conclusion = line.strip().split('=>')
            conclusion = tuple(conclusion.split('='))
            assert len(conclusion) == 2
            statement = Statement(
                premise={
                    k: v
                    for k, v in map(lambda x: x.split('='), premise.split(','))
                },
                conclusion=(conclusion[0], conclusion[1])  # for type checker
            )
            statements_.append(statement)

    ranges = defaultdict(list)
    with open(statements_values, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            header, values = line.strip().split(':')
            values = values.split(',')
            ranges[header] = list(values)

    return statements_, ranges


class MainWindow(W.QMainWindow):
    def __init__(
            self,
            statements_: list[Statement],
            available_values: dict[str, list[str]],
            target: str,
            target_value: str
    ) -> None:
        super().__init__()

        self.algo = Algorithm(statements_, 'algo_log.txt')



        self.setWindowTitle('Кто ты?')
        self.widget = W.QWidget()
        self.text = W.QLabel()
        self.choose = W.QComboBox()
        self.button = W.QPushButton("Go")
        self.layout = W.QVBoxLayout(self.widget)
        for w in [self.text, self.choose, self.button]:
            self.layout.addWidget(w)
        for i, v in enumerate(available_values['ты']):
            self.choose.insertItem(i, v)
        
        self.setCentralWidget(self.widget)

        self.button.clicked.connect(self._clicked)

        
    def _clicked(self):
        target = 'ты'
        target_value = self.choose.currentText()
        self.algo_exit = self.algo.run(target, target_value)
        if self.algo_exit is None:
            self.text.setText('Низя')
        else:
            self.text.setText(str(self.algo_exit))


statements, rules = read_statements('rules.txt', 'available_values.txt')
for s in statements:
    print(str(s))

window = MainWindow(
    statements, rules, 'ты', 'Булатов'
)
window.show()

app.exec()
