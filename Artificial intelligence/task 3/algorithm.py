from collections.abc import Generator
from datetime import datetime
from enum import Enum


class Logger:
    def __init__(self, filename: str) -> None:
        self.filename = filename
    
    def log(self, message: object) -> None:
        logged_string = f'[{datetime.now():%H:%M:%S}] {message}\n'
        with open(self.filename, 'a', encoding='utf-8') as file:
            file.write(logged_string)


class StatementResult(Enum):
    TRUE = 'True'
    FALSE = 'False'
    UNKNOWN = 'Unknown'


class Statement:
    def __init__(
        self,
        premise: dict[str, str],
        conclusion: tuple[str, str]
    ) -> None:
        self.premise = premise
        self.conclusion = conclusion

    @property
    def target(self) -> str:
        return self.conclusion[0]
    
    @property
    def value(self) -> str:
        return self.conclusion[1]
    
    def check(self, context: dict[str, str]) -> StatementResult:
        met_unk = False
        for k, v in self.premise.items():
            if k not in context:
                met_unk = True
                continue
            
            if context[k] != v:
                return StatementResult.FALSE
        
        if met_unk:
            return StatementResult.UNKNOWN
        
        return StatementResult.TRUE

    def first_unknown(self, context: dict[str, str]) -> str:
        for k in self.premise:
            if k not in context:
                return k
        
        assert False, 'context doesnt contain unknown feature'

    def __str__(self) -> str:
        return f'premise: {self.premise}, conclusion: {self.conclusion}'
    

class Algorithm:
    def __init__(
        self,
        statements: list[Statement],
        log_file: str
    ) -> None:
        self.statements = statements

        self.targets = []
        self.available_rules = set(range(len(self.statements)))
        self.logger = Logger(log_file)

    def run(self, target: str, value: str):
        self.targets = [(target, value)]
        context = {}
        a = True
        while True:
            if a:
                current_target, current_value = self.targets[-1]
                if current_target in context:
                    while len(self.targets) > 0:
                        self.targets.pop()
                        current_target, current_value = self.targets[-1]
                        if current_target not in context:
                            break

                if len(self.targets) == 1 and \
                    all(self.statements[i].target != current_target for i in self.available_rules):
                    return None 

            print('XXX', current_target, current_value)
            to_remove = []

            repeat = True
            while repeat:
                rule_found = False
                repeat = False
                for i in self.available_rules:
                    br = False

                    rule = self.statements[i]
                    if rule.target != current_target or rule.value != current_value:
                        continue
                    
                    rule_found = True
                    for feat, value in rule.premise.items():
                        if feat in context and value == context[feat]:
                            continue
                        if any(r.target == feat for r in self.statements):
                            self.targets.append((feat, value))
                            br = True
                            a = True
                            break
                        else:
                            context[feat] = value

                    to_remove.append(i)
                    if br:
                        break
                    if len(self.targets) == 1:
                        return context

                    current_target, current_value = self.targets[-1]
                    self.targets.pop()
                    repeat = True
                if not rule_found:
                    context[current_target] = current_value
                    self.targets.pop()

            a = True
            print(self.targets, context)
        return context
