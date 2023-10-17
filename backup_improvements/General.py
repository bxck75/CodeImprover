#protected
import os
# protected
from pathlib import Path
import re
import sys

#TODOS:
# - this class houses methods variables enums etc that do not realy fit under any  other class
# - It also could have experimental codes and mostlikly be connected to every class with methodsassist 
#- the name says it all its improving codeblocks it gets handed by the Splitter

class General():

    version: Optional[float] = (0.1) 
    path: Optional[str] = None
    log_file: Optional[str] = f"{str(Path(__file__).parent)}/General_Log.txt"

    """ Mandatory  version, path, log_file and docstring above init with a short description"""
    def __init__(self):
        self.name = "General";
        


















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