import re
from typing import List, Tuple, Set, Dict

class ExprNode:
    def evaluate(self, variables: Dict[str, bool]) -> bool:
        raise NotImplementedError()

    def collect_variables(self, variables: Set[str]) -> None:
        raise NotImplementedError()


class VarNode(ExprNode):
    def __init__(self, name: str):
        self.name = name

    def evaluate(self, variables: Dict[str, bool]) -> bool:
        return variables[self.name]

    def collect_variables(self, variables: Set[str]) -> None:
        variables.add(self.name)


class NotNode(ExprNode):
    def __init__(self, child: ExprNode):
        self.child = child

    def evaluate(self, variables: Dict[str, bool]) -> bool:
        return not self.child.evaluate(variables)

    def collect_variables(self, variables: Set[str]) -> None:
        self.child.collect_variables(variables)


class AndNode(ExprNode):
    def __init__(self, left: ExprNode, right: ExprNode):
        self.left = left
        self.right = right

    def evaluate(self, variables: Dict[str, bool]) -> bool:
        return self.left.evaluate(variables) and self.right.evaluate(variables)

    def collect_variables(self, variables: Set[str]) -> None:
        self.left.collect_variables(variables)
        self.right.collect_variables(variables)


class OrNode(ExprNode):
    def __init__(self, left: ExprNode, right: ExprNode):
        self.left = left
        self.right = right

    def evaluate(self, variables: Dict[str, bool]) -> bool:
        return self.left.evaluate(variables) or self.right.evaluate(variables)

    def collect_variables(self, variables: Set[str]) -> None:
        self.left.collect_variables(variables)
        self.right.collect_variables(variables)


class ImplNode(ExprNode):
    def __init__(self, left: ExprNode, right: ExprNode):
        self.left = left
        self.right = right

    def evaluate(self, variables: Dict[str, bool]) -> bool:
        return (not self.left.evaluate(variables)) or self.right.evaluate(variables)

    def collect_variables(self, variables: Set[str]) -> None:
        self.left.collect_variables(variables)
        self.right.collect_variables(variables)


class EquivNode(ExprNode):
    def __init__(self, left: ExprNode, right: ExprNode):
        self.left = left
        self.right = right

    def evaluate(self, variables: Dict[str, bool]) -> bool:
        return self.left.evaluate(variables) == self.right.evaluate(variables)

    def collect_variables(self, variables: Set[str]) -> None:
        self.left.collect_variables(variables)
        self.right.collect_variables(variables)

# === Парсинг выражения ===

token_spec = [
    (r'\s+',              None),
    (r'\(',               'LPAREN'),
    (r'\)',               'RPAREN'),
    (r'!',                'NOT'),
    (r'&',                'AND'),
    (r'\|',               'OR'),
    (r'->',               'IMPL'),
    (r'~',                'EQUIV'),
    (r'[a-zA-Z_]\w*',     'VAR'),
]

Token = Tuple[str, str]

def tokenize(expression: str) -> List[Token]:
    tokens = []
    pos = 0
    while pos < len(expression):
        match = None
        for pattern, tag in token_spec:
            regex = re.compile(pattern)
            match = regex.match(expression, pos)
            if match:
                text = match.group(0)
                if tag:
                    tokens.append((tag, text))
                pos = match.end()
                break
        if not match:
            raise SyntaxError(f"Недопустимый символ: {expression[pos]}")
    return tokens


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> ExprNode:
        return self.parse_equiv()

    def parse_equiv(self):
        node = self.parse_impl()
        while self._accept('EQUIV'):
            right = self.parse_impl()
            node = EquivNode(node, right)
        return node

    def parse_impl(self):
        node = self.parse_or()
        while self._accept('IMPL'):
            right = self.parse_or()
            node = ImplNode(node, right)
        return node

    def parse_or(self):
        node = self.parse_and()
        while self._accept('OR'):
            right = self.parse_and()
            node = OrNode(node, right)
        return node

    def parse_and(self):
        node = self.parse_not()
        while self._accept('AND'):
            right = self.parse_not()
            node = AndNode(node, right)
        return node

    def parse_not(self):
        if self._accept('NOT'):
            return NotNode(self.parse_not())
        return self.parse_atom()

    def parse_atom(self):
        if self._accept('LPAREN'):
            node = self.parse_equiv()
            self._expect('RPAREN')
            return node
        elif self._accept('VAR'):
            return VarNode(self._prev_value)
        else:
            raise SyntaxError("Ожидалась переменная или скобка")

    def _accept(self, tag):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == tag:
            self._prev_value = self.tokens[self.pos][1]
            self.pos += 1
            return True
        return False

    def _expect(self, tag):
        if not self._accept(tag):
            raise SyntaxError(f"Ожидался {tag}")


def parse_expression(expression: str) -> Tuple[ExprNode, List[str]]:
    tokens = tokenize(expression)
    parser = Parser(tokens)
    root = parser.parse()

    variables = set()
    root.collect_variables(variables)
    return root, sorted(variables)
