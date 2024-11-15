from collections import defaultdict
from collections.abc import Generator, Iterable
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


class Rule:
    def __init__(
            self,
            features: list[str, str],
            conclusion: list[str, str],
        ) -> None:
        self.rule = defaultdict(lambda: ' ')
        for f, v in features:
            self.rule[f'{f}:{v}'] = '-'
        for f, v in conclusion:
            self.rule[f'{f}:{v}'] = '+'

# feature, value, type
Rule = list[tuple[str, str, str]]


def first(iterable: Iterable, predicate):
    for item in iterable:
        if predicate(item):
            return item
    return None


def get_target_features(rule: Rule) -> list[str]:
    return [
        feature
        for feature, _, type_ in rule
        if type_ == '+'
    ]


def nontarget_count(rule: Rule) -> int:
    return sum(type_ == '-' for *_, type_ in rule)


def get_feature(rule: Rule, feature: str) -> tuple[str, str] | None:
    for f, value, t in rule:
        if f == feature:
            return value, t
        
    return None

def has_feature(rule: Rule, feature: str) -> bool:
    return get_feature(rule, feature) is None


def first_unknown_feature(rule: Rule, context: dict[str, str]) -> str:
    return first(rule, lambda x: x[-1] == '-' and x not in context)


class Algorithm:
    def __init__(
            self,
            rules: list[Rule],
            log_file: str
        ) -> None:
        
        self.rules = rules
        self.targets_stack = []
        self.results = {}

        self.logger = Logger(log_file)

    def run(self, target_feature: str) -> Generator[None, dict[str, str | None], None]:
        goals_table = [
            rule 
            for rule in self.rules
            if target_feature in get_target_features(rule)
        ] # 1.1

        while True:
            goals_table.sort(key=nontarget_count)
            if len(goals_table) == 0:
                yield {'result': None}
                return
            
            if nontarget_count(goals_table[0]) == 0:
                yield {'result': get_feature(goals_table[0], target_feature)}
                return

            unk_feature = first_unknown_feature(goals_table[0], self.results)
            result = yield unk_feature[0]
            if result is None:
                generator = self.run(unk_feature[0])
                res = next(generator)
                while 'result' not in res:
                    ans = yield res
                    res = generator.send(ans)
                result = res['result']

            self.results[unk_feature[0]] = result

            excluded_rules = []
            for idx, rule in enumerate(goals_table):
                for fid, (feature, value, type_) in enumerate(rule):
                    if feature not in self.results:
                        if type_ == '+':
                            self.logger.log(f'Setting plus: {rule}')
                            self.results[feature] = value
                            continue
                        else:
                            break
                    
                    if type_ == '-' and value != self.results[feature]:
                        self.logger.log(f'EXCLUDED {rule}')
                        excluded_rules.append(idx)
                        break
                    elif type_ == '-':
                        rule[fid] = feature, value, ' '
                    elif type_ == '+' and value != self.results[feature]:
                        self.logger.log(f'EXCLUDED {rule}')
                        excluded_rules.append(idx)
                        break
            
            if target_feature in self.results:
                self.logger.log('Target found!')
                yield {'result': self.results[target_feature]}
            
            self.logger.log('Reloading goals table')
            goals_table = [
                goals_table[i] for i in range(len(goals_table))
                if i not in excluded_rules
            ]

                
                
