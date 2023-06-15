import ast

"""
Transform this:

(lambda f1: f1(expr1))(lambda x1:
    (lambda f2: f2(expr2))(lambda x2:
        [...]
    )
)

Into this:

x1 = expr1
x2 = expr2
[...]

"""


class UnbindTransformer(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.statements = []
    
    def visit_Module(self, node):
        self.generic_visit(node)
        # return the statements
        node.body = self.statements
        return node
    
    def visit_Call(self, node):
        """
        We are interested in this pattern
        (lambda f1: f1(expr1))(lambda x1: something)

        We want to transform it into
        x1 = expr1
        and recurse on something
        """
        f = node.func

        if isinstance(f, ast.Lambda):
            # pp(node)
            identifier = f.args.args[0].arg
            # print(identifier)
            # pp(f.body)
            if isinstance(f.body, ast.Call):
                func_name = f.body.func.id
                if func_name == identifier:
                    # print('bind lambda')
                    expr = f.body.args[0]
                    bind_lambda = node.args[0]
                    bind_name = bind_lambda.args.args[0].arg
                    # print('bind', bind_name, 'to', ast.dump(expr))
                    self.statements.append(ast.Assign(
                        targets=[ast.Name(id=bind_name, ctx=ast.Store())],
                        value=expr
                    ))
                    # pp(bind_lambda)
                    self.visit(bind_lambda.body)
                    return node
        self.visit(node)
        return node