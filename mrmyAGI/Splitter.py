#protected
import os
# protected
from pathlib import Path
import re
import sys
from typing import Optional
import os
from pathlib import Path
import re

#TODOS:
# - always a mandatory comment block for todo's at the top of each script
# - begin developing and improving a splitternerger class here.
#- it handles splitting and merging of scripts int seperate method or class codeblocks
#- i should store information on how scripts where layed out so when merging improved codeblocks it knows how to
#- although improved and different then at splitting after merging scripts should have the same layout as before
#- mandatory comment blocks at top and bottom should als be blocks and retain there content throughout the improvment process
#- after a split improve and merge action the version nr, Todo', Descriptions, usage, usec ases and proposed features need updating
#- if needed this process needs a llm agent to lead and oversee the process and log exactly conform format determined by the Logger class



class SplitterMerger:
    version: Optional[float] = 0.3
    path: Optional[str] = None
    log_file: Optional[str] = f"{str(Path(__file__).parent)}/SplitMerge_Log.txt"

    def __init__(self, path: str):
        self.path = path

    def split_script(self) -> list[str]:
        with open(self.path, 'r') as f:
            content = f.read()
            code_blocks = re.findall(r"(?:(?:def|class)\s+\w+[\w\s\:\(\)\,]*)|(?:@[\w\s]*\n(?:def|class)\s+\w+[\w\s\:\(\)\,]*)", content, re.MULTILINE)
            return code_blocks

    def merge_code_blocks(self, code_blocks: dict[str, str]) -> None:
        with open(self.path, 'r') as f:
            content = f.read()
            for code_block in code_blocks:
                content = content.replace(code_block, code_blocks[code_block])
        with open(self.path, 'w') as f:
            f.write(content)

    def update_script_info(self, new_info: dict[str, str]) -> None:
        with open(self.path, 'r') as f:
            content = f.read()
            content = re.sub(r"(Description:)(.*?)(Predicted use cases:)",
                             rf"\1\n    {new_info['description']}\n\3", content, flags=re.DOTALL)
            content = re.sub(r"(Usage:)(.*?)(Proposed features:)",
                             rf"\1\n    {new_info['usage']}\n\3", content, flags=re.DOTALL)
            content = re.sub(r"(Predicted use cases:)(.*?)(Version:)",
                             rf"\1\n    {new_info['predicted_use_cases']}\n\3", content, flags=re.DOTALL)
            content = re.sub(r"(Proposed features:)(.*?)(Description:)",
                             rf"\1\n    {new_info['proposed_features']}\n\3", content, flags=re.DOTALL)
        with open(self.path, 'w') as f:
            f.write(content)

    def log(self, message: str) -> None:
        with open(self.log_file, 'a') as f:
            f.write(message + '\n')

    def improve_code_block(self, code_block: str) -> str:
        # Todo: Implement your code improvement logic here
        return code_block

    def update_version(self) -> None:
        self.version += 0.1

    def update_todos(self, todos: str) -> None:
        with open(self.path, 'r') as f:
            content = f.read()
            content = re.sub(r"(TODOS:)(.*?)(\n\s*'''|$)",
                             rf"\1\n    {todos}\n\3", content, flags=re.DOTALL)
        with open(self.path, 'w') as f:
            f.write(content)


if __name__ == '__main__':
    splitter_merger = SplitterMerger('path/to/your/script.py')
    code_blocks = splitter_merger.split_script()
    improved_code_blocks = {}
    for code_block in code_blocks:
        improved_code_block = splitter_merger.improve_code_block(code_block)
        improved_code_blocks[code_block] = improved_code_block
    splitter_merger.merge_code_blocks(improved_code_blocks)
    splitter_merger.update_script_info({
        'description': 'Improved script',
        'usage': 'python script.py',
        'predicted_use_cases': 'Improved use cases',
        'proposed_features': 'Improved features'
    })
    splitter_merger.update_version()
    splitter_merger.update_todos("")

    splitter_merger.log('Script improved')


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