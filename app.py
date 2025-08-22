from flask import Flask, render_template, request
import ast
import operator
import math

app = Flask(__name__)

# Supported operators
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg  # Unary negative, e.g. -5
}

# Supported functions (e.g. sqrt)
allowed_names = {
    'sqrt': math.sqrt
}

def evaluate_expression(expr):
    """
    Safely evaluates a mathematical expression string using AST.
    Supports +, -, *, /, **, sqrt() and negative numbers.
    """
    def _eval(node):
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in operators:
                return operators[op_type](left, right)
            else:
                raise TypeError("Unsupported operator")
        elif isinstance(node, ast.UnaryOp):  # e.g. -5
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in operators:
                return operators[op_type](operand)
            else:
                raise TypeError("Unsupported unary operator")
        elif isinstance(node, ast.Call):  # e.g. sqrt(9)
            if isinstance(node.func, ast.Name) and node.func.id in allowed_names:
                func = allowed_names[node.func.id]
                args = [_eval(arg) for arg in node.args]
                return func(*args)
            else:
                raise TypeError("Unsupported function")
        elif isinstance(node, ast.Num):  # Python < 3.8
            return node.n
        elif isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.Expression):
            return _eval(node.body)
        else:
            raise TypeError("Unsupported expression type")

    parsed = ast.parse(expr, mode='eval')
    return _eval(parsed.body)

import re

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = ""
    if request.method == "POST":
        expression = request.form.get("expression", "")

        # Replace UI symbols with Python equivalents
        expression = expression.replace('÷', '/')
        expression = expression.replace('%', '/100')
        expression = expression.replace('√(', 'sqrt(')

        # Insert * for implicit multiplication between:
        # number and sqrt (e.g. 8sqrt(5) -> 8*sqrt(5))
        expression = re.sub(r'(\d)(sqrt)', r'\1*\2', expression)

        # number followed by '(' (e.g. 2(3+4) -> 2*(3+4))
        expression = re.sub(r'(\d)\(', r'\1*(', expression)

        # ')' followed by '(' (e.g. (2+3)(4+5) -> (2+3)*(4+5))
        expression = re.sub(r'\)(\()', r')*(', expression)

        # Auto-close parentheses if needed
        open_count = expression.count('(')
        close_count = expression.count(')')
        if open_count > close_count:
            expression += ')' * (open_count - close_count)

        try:
            result = str(evaluate_expression(expression))
        except ZeroDivisionError:
            result = "Error: Division by zero"
        except Exception:
            result = "Invalid Expression"
    return render_template("calculator_buttons.html", result=result)



if __name__ == "__main__":
    app.run(debug=True)
