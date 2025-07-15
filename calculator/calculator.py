
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Cannot divide by zero"
    return x / y


num1 = 10
num2 = 5

sum_result = add(num1, num2)
print(f"The sum of {num1} and {num2} is: {sum_result}")

difference_result = subtract(num1, num2)
print(f"The difference of {num1} and {num2} is: {difference_result}")

product_result = multiply(num1, num2)
print(f"The product of {num1} and {num2} is: {product_result}")

quotient_result = divide(num1, num2)
print(f"The quotient of {num1} and {num2} is: {quotient_result}")