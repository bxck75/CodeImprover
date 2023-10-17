#protected
import os
# protected
from pathlib import Path
import re
import sys

#TODOS:
# - always a mandatory comment block for todo's at the top of each script
# - begin developing and improving a Monitor class here.
#- it handles monitoring all processes in the project and managing the data it gets
#- it should store information workflow status of processes and begin and end results of actions
#- it needs to store the gathered data in a organized way ready for the Interface class to display
#- this lso includes keeping a register of classes and their current state and version nr 
#- i might also have logic to show or  relay data in a fancy way like diagrams and graphs


class Monitor():

    version: Optional[float] = (0.1) 
    path: Optional[str] = None
    log_file: Optional[str] = f"{str(Path(__file__).parent)}/Monitor_Log.txt"

    """ Mandatory  version, path, log_file and docstring above init with a short description"""
    def __init__(self):
        """
        Initializes a new instance of the Monitor class.
        """
        self.name = "Monitor";
        


















    f'''
    # -aways a mandatory comment block for description ,Usage, Use cases and proposed features at the bottom
    Description:
        <here the assistant describes script working>
    Usage:
        <here the assistant describes script usage>
    Predicted use cases:
        <here the assistant describes use cases>
    Proposed features:
        <here the assistant proposes features>
    '''