import logging

# Do Not Change Above Line#


class MathDebugger:
    version: Optional[float] = 0.1
    def __init__(self, level: int = logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        self.handler = logging.StreamHandler()
        self.handler.setLevel(level)
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def set_level(self, level: int) -> None:
        self.logger.setLevel(level)
        self.handler.setLevel(level)

    def set_format(self, format: str) -> None:
        self.formatter = logging.Formatter(format)
        self.handler.setFormatter(self.formatter)

    def set_handler(self, handler: logging.Handler) -> None:
        self.logger.handlers = [handler]

    def set_logger(self, logger: logging.Logger) -> None:
        self.logger = logger

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)


class MathOperations:
    def __init__(self, debugger: MathDebugger) -> None:
        self.debugger = debugger

    def add_numbers(self, num1: int, num2: int) -> int:
        return num1 + num2

    def subtract_numbers(self, num1: int, num2: int) -> int:
        return num1 - num2


if __name__ == "__main__":
    # Initialize the debugger
    debugger = MathDebugger()

    # Initialize the MathOperations class
    math_ops = MathOperations(debugger)

    # Ask the user to input two numbers
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))

    # Call the add_numbers function to add the two numbers and print the result
    result = math_ops.add_numbers(num1, num2)
    debugger.info(f"The sum of {num1} and {num2} is {result}")

    # Call the subtract_numbers function to subtract the second number from the first number and print the result
    result = math_ops.subtract_numbers(num1, num2)
    debugger.info(f"The difference between {num1} and {num2} is {result}")
