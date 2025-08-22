from flask import Flask, render_template, request

def get_number(prompt):
    while True:
        try:
            value = input(prompt)
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            print("Invalid Input. Please enter a valid input")

def add(a, b):
    return a + b
def subtract(a, b):
    return a - b
def multiply(a, b):
    return a * b
def divide(a, b):
    return a / b

while True:
    title = "Simple Calculator".upper()
    print("=" * 40)
    print(title.center(40))
    print("=" * 40)

    print("Choose operation: ")
    print("1) add (+)")
    print("2) subtract (-)")
    print("3) mutiply (*)")
    print("4) divide (/)")

    choice = input("Enter 1/2/3/4: ").strip()

    x=get_number("Enter fisrt number: ")
    y=get_number("Enter second number: ") 

    if choice == "1":
       result = add(x, y)
    elif choice == "2":
       result = subtract(x, y)
    elif choice == "3":
       result = multiply(x, y)
    elif choice == "4":
       result = divide(x, y)
    else:
       result = "Invalid Choice"

    print(f"Result: {result}")

    again = input("Do you want to continue? (y/n): ").strip().lower()
    if again != "y":
        print("Goodbye!")
        break

