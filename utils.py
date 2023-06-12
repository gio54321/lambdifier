import ast

def pp(node):
    print(ast.dump(node, indent=4))