# do not change above line#

import os
from typing import Optional
from pathlib import Path
from enum import Enum


class Monitor:
    version: Optional[float] = 0.2

    class MonitorLevel(Enum):
        INFO = 1
        WARNING = 2
        ERROR = 3

    def __init__(self, monitor_file: Optional[str] = None):
        """
        Initializes a Monitor instance.

        :param monitor_file: Path to the monitor file. If not provided, uses the default path.
        """
        self.name = "monitor"
        self.monitor_file = (
            f"{str(Path(__file__).parent)}/monitor_monitor.txt" if monitor_file is None else monitor_file
        )

    def monitor_message(self, message: str, level: MonitorLevel = MonitorLevel.INFO):
        """
        Logs a monitored message with the specified level.

        :param message: The message to be logged.
        :param level: The level of the monitored message.
        """
        with open(self.monitor_file, "a") as monitor_file:
            monitor_file.write(f"{level.name}: {message}\n")


# adding if __name__ == "__main__"
if __name__ == "__main__":
    monitor_instance = Monitor()

"""
todos:
    - Implement monitor rotation to manage monitor file size.
    - Add option to monitor to different files based on monitor type.
    - Implement monitoring to remote servers or services.
"""

"""
description:
    The Monitor class provides a basic structure for monitoring in a Python project.
    It allows you to monitor messages with different types (info, error, warning) to a specified monitor file.

usage:
    1. Create an instance of the Monitor class.
    2. Use the instance to monitor messages using the `monitor_message` method, specifying the monitor type.
    3. Optionally, use the `set_monitor_file` method to set a custom monitor file path.

predicted use cases:
    - Monitoring errors, warnings, and information for debugging and monitoring.
    - Centralized monitoring for tracking the flow of your Python project.

proposed features:
    - Monitor rotation to manage monitor file size.
    - Option to monitor to different files based on monitor type.
    - Monitoring to remote servers or services.
"""
