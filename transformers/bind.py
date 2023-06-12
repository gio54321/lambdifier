import ast
from utils import pp

"""
transform

x = body1
y = body2

into 

(lambda g: g(body1))(lambda x: (lambda g: g(body2))(lambda y: ...)

"""


class BindTransformer(ast.NodeTransformer):
    # visit assignments
    def visit_Module(self, node):
        statements = node.body
        # last body is identity
        body = ast.Lambda(
            args=ast.arguments(
                args=[ast.arg(arg='x')],
                defaults=[],
                vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                posonlyargs=[],
            ),
            body=ast.Name(id='x', ctx=ast.Load()),
        )

        for stmt in statements[::-1]:
            if isinstance(stmt, ast.Assign):
                name = stmt.targets[0].id
                value = stmt.value
                continuation = ast.Lambda(
                    args=ast.arguments(
                        args=[ast.arg(arg='g')],
                        defaults=[],
                        vararg=None,
                        kwonlyargs=[],
                        kw_defaults=[],
                        kwarg=None,
                        posonlyargs=[],
                    ),
                    body=ast.Call(
                        func=ast.Name(id='g', ctx=ast.Load()),
                        args=[value],
                        keywords=[],
                    ),
                )
                body = ast.Call(
                    func=continuation,
                    args=[ast.Lambda(
                        args=ast.arguments(
                            args=[ast.arg(arg=name)],
                            defaults=[],
                            vararg=None,
                            kwonlyargs=[],
                            kw_defaults=[],
                            kwarg=None,
                            posonlyargs=[],
                        ),
                        body=body
                    )],
                    keywords=[],
                )
        return body