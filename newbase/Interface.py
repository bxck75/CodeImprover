# do not change above line #
import os
from pathlib import Path
import re
import sys

# todos:
# - Create a class named "Interface" to handle visualizing data and project history
# - Add a central dashboard panel with status bars, diagrams, graphs, and data tables
# - Make the dashboard panel visually appealing and informative for project workflow
# - Provide bug tracking and bottleneck solving functionality
# - Implement the ability to save media of data or history upon request


class Interface:
    version: float = 0.1
    path: str = None
    log_file: str = f"{str(Path(__file__).parent)}/interface_log.txt"

    def __init__(self):
        self.name = "interface"


if __name__ == "__main__":
    interface = Interface()

'''
description:
    The Interface class represents a visual interface for displaying project data and history. It includes a central dashboard panel with various visualizations, such as status bars, diagrams, graphs, and data tables. The interface can be used for bug tracking, bottleneck solving, and generating saved media of project data or history.
usage:
    1. Create an instance of the Interface class.
    2. Access and use the visual interface features to analyze project data and history.
predicted use cases:
    - Analyzing project workflow
    - Bug tracking and debugging
    - Identifying bottlenecks and performance issues
proposed features:
    - Ability to export/save visualizations and project data
    - I propose making a flask app that can have a fancy Panel and can show live data as its generated or show historic data from the sqlite DB
'''
