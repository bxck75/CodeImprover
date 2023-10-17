# Do Not Change Above Line#

import os
from typing import Optional
from pathlib import Path
from enum import Enum


class Monitor:
    version: Optional[float] = 0.1
    class MonitorLevel(Enum):
        INFO = 1
        WARNING = 2
        ERROR = 3

    def __init__(self, path: Optional[str] = None):
        self.name = "Monitor"
        self.monitor_file = f"{str(Path(__file__).parent)}/Monitor_Monitor.txt" if path is None else path

    def monitor(self, message: str, level: MonitorLevel = MonitorLevel.INFO):
        with open(self.monitor_file, "a") as monitor_file:
            monitor_file.write(f"{level.name}: {message}\n")


# Adding if __name__ == "__main__"
if __name__ == "__main__":
    monitor = Monitor()
# protected
f'''
Description:
    The Monitor class provides a basic structure for monitorging in a Python project.
    It allows you to monitor messages with different types (info, error, warning) to a specified monitor file.

Usage:
    1. Create an instance of the Monitor class.
    2. Use the instance to monitor messages using the `monitor_message` method, specifying the monitor type.
    3. Optionally, use the `set_monitor_file` method to set a custom monitor file path.

Predicted use cases:
    - Monitoring errors, warnings, and information for debugging and monitoring.
    - Centralized monitorging for tracking the flow of your Python project.

Proposed features:
    - Monitor rotation to manage monitor file size.
    - Option to monitor to different files based on monitor type.
    - Monitoring to remote servers or services.
'''
