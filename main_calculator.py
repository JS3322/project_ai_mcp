from pymcp import PyMCP

def add(a: int, b: int) -> int:
    """
    Add two numbers
    """
    return a + b

def subtract(a: int, b: int) -> int:
    """
    Subtract two numbers
    """
    return a - b

def multiply(a: int, b: int) -> int:
    """
    Multiply two numbers
    """
    return a * b

def divide(a: int, b: int) -> int:
    """
    Divide tow numbers
    """
    if b == 0:
        return "Cannot divide by zero"
    return a / b

# Combine multiple functions into one server
calculator = PyMCP(name="Calculator Server", instructions="A Server providing calculator funtions")
calculator.add_function(add)
calculator.add_function(subtract)
calculator.add_function(multiply)
calculator.add_function(divide)

# Run the server
calculator.run()

