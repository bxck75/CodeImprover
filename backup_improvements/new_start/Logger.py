from typing import Optional
from pathlib import Path


class Logger:
    version: Optional[float] = 0.1
    name: str = "CodeImprover"
    log_file: str = "LOG.txt"
    script_path: Optional[str] = Path(__file__).parent

    def __init__(self, log_file: Optional[str] = None):
        """
        Initializes the Logger class.

        Args:
            log_file: The path to the log file.
        """
        if log_file:
            self.log_file = log_file
        self.log_file = self.script_path / self.log_file

    def log_message(self, message: str, log_type: str = "info"):
        """
        Logs a message with a specified log type to the log file.

        Args:
            message: The message to be logged.
            log_type: The type of the log message. Supported types: 'info', 'error', 'warning'.

        Raises:
            ValueError: If an invalid log_type is provided.
        """
        log_types = ["info", "error", "warning"]
        if log_type not in log_types:
            raise ValueError(
                "Invalid log_type. Supported types: 'info', 'error', 'warning'")
        with open(self.log_file, "a") as file:
            file.write(f"[{log_type}] {message}\n")

    def __call__(self, message: str, log_type: str = "info"):
        """
        Logs a message with a specified log type to the log file.

        Args:
            message: The message to be logged.
            log_type: The type of the log message. Supported types: 'info', 'error', 'warning'.

        Raises:
            ValueError: If an invalid log_type is provided.
        """
        self.log_message(message, log_type)


if __name__ == "__main__":
    logger = Logger()  # You can specify a log file path here as an argument.
    logger.log_message("This is a test log message")
    logger.log_message("This is an error message", "error")
    logger.log_message("This is a warning message", "warning")
