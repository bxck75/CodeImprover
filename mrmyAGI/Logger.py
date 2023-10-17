#protected
import os
# protected
from pathlib import Path
import re
import sys
from typing import Optional
#TODOS:
# - always a mandatory comment block for todo's at the top of each script
# - begin developing and improving a general logger class here.
#- it needs to be available throughout the project
#- i should store its logs in a central place but still organized so i caan see what happended where and when
#- it should be able to log anything from txt to failed api requests to failing ai and everything in between.
#- it shpould also be easy to digest for agents that have the task of bugg fixing bit also be browsable by humans
#- please think of a 'all telling' label style log that alsways looks the same but can have an array of different data.


class Logger():

    version: Optional[float] = (0.1) 
    path: Optional[str] = None
    log_file: Optional[str] = f"{str(Path(__file__).parent)}/Logger_Log.txt"

    """ Mandatory  version, path, log_file and docstring above init with a short description"""
    def __init__(self):
        self.name = "Logger";
        


















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