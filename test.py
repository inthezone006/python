def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b

def calculator():
    print("Welcome to the Four-Function Calculator!")
    print("Select an operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")

    while True:
        try:
            choice = int(input("Enter your choice (1/2/3/4): "))

            if choice not in [1, 2, 3, 4]:
                print("Invalid input. Please select a valid operation.")
                continue

            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            if choice == 1:
                print(f"The result is: {add(num1, num2)}")
            elif choice == 2:
                print(f"The result is: {subtract(num1, num2)}")
            elif choice == 3:
                print(f"The result is: {multiply(num1, num2)}")
            elif choice == 4:
                print(f"The result is: {divide(num1, num2)}")
        
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            continue

        next_calculation = input("Do you want to perform another calculation? (yes/no): ").lower()
        if next_calculation != 'yes':
            print("Thank you for using the calculator. Goodbye!")
            break

if __name__ == "__main__":
    calculator()
