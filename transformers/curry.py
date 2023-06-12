import ast

class CurryTransformer(ast.NodeTransformer):
    def visit_Lambda(self, node):
        # recurr on the body
        last_body = self.visit(node.body)

        # transform the lambda into a chain of lambdas
        for arg in node.args.args[::-1]:
            new_node = ast.Lambda(
                args=ast.arguments(
                    args=[arg],
                    defaults=[],
                    vararg=[],
                    kwonlyargs=[],
                    kw_defaults=[],
                    kwarg=None,
                    posonlyargs=[],
                ),
                body=last_body,
            )
            last_body = new_node
        return new_node

    def visit_Call(self, node):
        last_fun = self.visit(node.func)
        for arg in node.args:
            last_fun = ast.Call(
                func=last_fun,
                args=[self.visit(arg)],
                keywords=[],
            )
        return last_fun