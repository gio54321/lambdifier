import ast
from utils import pp

class NameScramblerTransformer(ast.NodeTransformer):
    def __init__(self):
        self.mapping = {}
        self.counter = 0
        super().__init__()

    def visit_Lambda(self, node):
        var_name = f'_{self.counter}'
        self.counter += 1

        # assume curried lambda
        original_name = node.args.args[0].arg
        self.mapping[original_name] = var_name
        self.visit(node.body)
        node.args.args[0].arg = var_name
        del self.mapping[original_name]

        return node
    
    def visit_Name(self, node):
        if node.id in self.mapping:
            node.id = self.mapping[node.id]
        return node
