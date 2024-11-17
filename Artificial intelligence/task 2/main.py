import sys
from algorithm import Algorithm
from PyQt6 import QtWidgets as W
from collections import defaultdict

app = W.QApplication(sys.argv)

def read_statements(statements_file: str, statements_values: str):
    rules = []
    with open(statements_file, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            premise, conclusion = line.strip().split('=>')
            rule = []
            for p in premise.split(','):
                s = p.split('=')
                rule.append((s[0], s[1], '-'))
            for c in conclusion.split(','):
                s = c.split('=')
                rule.append((s[0], s[1], '+'))
            rules.append(rule)
    
    ranges = defaultdict(list)
    with open(statements_values, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            header, values = line.strip().split(':')
            values = values.split(',')
            ranges[header] = list(values)

    return rules, ranges


class MainWindow(W.QMainWindow):
    def __init__(
            self,
            rules: list,
            available_values: dict[str, list[str]],
            target: str
    ) -> None:
        super().__init__()

        self.algo = Algorithm(rules, 'algo_log.txt')
        self.algo_exit = self.algo.run(target)

        self.target = target
        self.available_values = available_values

        self.setWindowTitle('Кто ты?')
        self.widget = W.QWidget()
        self.text = W.QLabel()
        self.button = W.QPushButton('Submit')
        self.dropdown = W.QComboBox()
        self.layout = W.QVBoxLayout(self.widget)
        for w in [self.text, self.dropdown, self.button]:
            self.layout.addWidget(w)

        self.setCentralWidget(self.widget)

        self.button.clicked.connect(self._button_clicked)
        self._process_output(next(self.algo_exit))

    def _button_clicked(self) -> None:
        selected_item = self.dropdown.currentText()
        if selected_item == 'Не знаю':
            selected_item = None
        self._process_output(self.algo_exit.send(selected_item))

    def _process_output(self, output: str | dict[str, str | None]) -> None:
        if isinstance(output, dict):  # got result
            result = output['result']
            message_box = W.QMessageBox()
            if result is None:
                message_box.setText('Я не знаю кто ты')
            else:
                message_box.setText(f'ты - {result}')
            message_box.exec()
            app.exit(0)
            exit(0)

        self.dropdown.clear()
        self.text.setText(output)
        for i, item in enumerate(self.available_values[output] + ['Не знаю']):
            self.dropdown.insertItem(i, item)


statements, rules = read_statements('rules.txt', 'available_values.txt')

window = MainWindow(
    statements, rules, 'ты'
)
window.show()

app.exec()
