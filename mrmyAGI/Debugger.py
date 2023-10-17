# TODO: Scart making a Debugger class here
import logging

# Do Not Change Above Line#
# TODO: Implement the following features:
    # - Ask the user to input two numbers
    # - Call the add_numbers function to add the two numbers and print the result
    # - Call the subtract_numbers function to subtract the second number from the first number and print the result

class Debugger:
    def __init__(self, level=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        self.handler = logging.StreamHandler()
        self.handler.setLevel(level)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

def add_numbers(num1: int, num2: int) -> int:
    return num1 + num2

def subtract_numbers(num1: int, num2: int) -> int:
    return num1 - num2

if __name__ == "__main__":
    
    # Initialize the debugger
    debugger = Debugger()

    # Ask the user to input two numbers
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))

    # Call the add_numbers function to add the two numbers and print the result
    result = add_numbers(num1, num2)
    debugger.info(f"The sum of {num1} and {num2} is {result}")

    # Call the subtract_numbers function to subtract the second number from the first number and print the result
    result = subtract_numbers(num1, num2)
    debugger.info(f"The difference between {num1} and {num2} is {result}")

    # Description:
    #   This script adds and subtracts two numbers entered by the user and prints the results.
    # Usage:
    #   1. Run the script.
    #   2. Enter two numbers when prompted.
    # Predicted use cases:
    #   - Basic addition and subtraction of two numbers.
    # Proposed features:
    #   - None
