import ast
from utils import pp


class VariableReferenceChecker(ast.NodeVisitor):
    def __init__(self, variable_name):
        self.variable_name = variable_name
        self.referenced = False

    def visit_Name(self, node):
        if node.id == self.variable_name:
            self.referenced = True
        self.generic_visit(node)

    def check_referenced(self, tree):
        self.visit(tree)
        return self.referenced

class NormalizeTransformer(ast.NodeTransformer):
    def visit_Module(self, node):
        self.assignments = []
        self.counter = 0

        statements = node.body
        new_body = []
        for stmt in statements:
            if isinstance(stmt, ast.Assign):
                body = self.__rec_transform(stmt.value, toplevel=True)
                stmt.value = body
                for x in self.assignments:
                    new_body.append(x)
                self.assignments = []
                new_body.append(stmt)
        node.body = new_body
        return node
    
    def __rec_transform(self, node, toplevel = False, bound_names = []):

        if isinstance(node, ast.Call):
            func = self.__rec_transform(node.func, bound_names=bound_names)
            args = [self.__rec_transform(arg, bound_names=bound_names) for arg in node.args]
            keywords = []
            call = ast.Call(func=func, args=args, keywords=keywords)
            if toplevel:
                return call
            for name in bound_names:
                if VariableReferenceChecker(name).check_referenced(node):
                    return call
            new_name = f'_x{self.counter}'
            self.counter += 1
            self.assignments.append(ast.Assign(targets=[ast.Name(new_name, ast.Store())], value=call))
            return ast.Name(new_name, ast.Load())
        elif isinstance(node, ast.Lambda):
            # recur on the body, but add the arguments to the bound names
            new_body = self.__rec_transform(node.body, bound_names=bound_names + [arg.arg for arg in node.args.args])
            node.body = new_body
            return node
        elif isinstance(node, ast.IfExp):
            test = self.__rec_transform(node.test, bound_names=bound_names)
            body = self.__rec_transform(node.body, bound_names=bound_names)
            orelse = self.__rec_transform(node.orelse, bound_names=bound_names)
            return ast.IfExp(test=test, body=body, orelse=orelse)
        elif isinstance(node, ast.List) and node.elts != []:
            elts = [self.__rec_transform(elt, bound_names=bound_names) for elt in node.elts]
            return ast.List(elts=elts, ctx=ast.Load())
        else:
            for name in bound_names:
                if VariableReferenceChecker(name).check_referenced(node):
                    return node
            if isinstance(node, ast.Call):
                new_value = self.__rec_transform(node, bound_names=bound_names)
            else:
                new_value = node
            if toplevel:
                return new_value
            new_name = f'_x{self.counter}'
            self.counter += 1
            self.assignments.append(ast.Assign(targets=[ast.Name(new_name, ast.Store())], value=new_value))
            return ast.Name(new_name, ast.Load())