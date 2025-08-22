from flask import Flask, render_template, request

app = Flask(__name__)

#calculator functions

def add(a , b):
    return a + b
def subtract(a , b):
    return a - b
def multiply(a , b):
    return a * b
def divide(a , b):
    try:
        return(a / b)
    except ZeroDivisionError:
        return "Error: Division by Zero"

@app.route("/", methods= ["GET", "POST"])
def calculator():
    result = None
    error = None


    if request.method == "POST":
        try:
            x = float(request.form["x"])  # Accepts both int and float
            y = float(request.form["y"])
            operation = request.form["operation"]

            if operation == "add":
                result = add(x, y)
            elif operation == "subtract":
                result = subtract(x, y)
            elif operation == "multiply":
                result = multiply(x, y)
            elif operation == "divide":
                result = divide(x, y)
            else:
                error = "Invalid Operation"
        except ValueError:
            error = "Please enter valid numbers"

    return render_template("calculator.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)

