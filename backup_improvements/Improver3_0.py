import argparse
import subprocess
import sys
from pathlib import Path
import re
import random
import os
from g4f import ChatCompletion,models,Provider
from glob import glob
from typing import Optional
from langchain_g4f import G4FLLM
import autopep8
import tempfile
import coverage
 
# TODO: this one has prio above all the first part of the improve method is a chaos of if's and else's and should be re-done.
# TODO: second most important is the part where the temp file is written in the generate_coverage_report this is because when the tempfile is made the OS locks it and can not be written unless you close it after its made with delete on false the OS releases it the and it can be directly written. i fixed thos ones but it was undone
# TODO: Its very important that we make our improver 100% bug free becausee to many times i need to manualy fetch the updat from logs.
# TODO: self improve has a bug where by the improving crashes mostlikely because its active and beeing overe written by itself
# TODO: the improving agent should also be able to search online durig the improving process to reach up to date info.
# TODO: the improving agent should also be able to open other scripts during improving to lay links betwee the multiple scipts
# TODO: the improving agent should also be able to send email messages with a simple python mailing scripts.
# TODO: after improving a script thre should be a check to read the imptoved script and ee if it was reaaly update
# TODO: More advanced code analysis and recommendations.
# TODO: Integration with version control systems.

class CodeImprover:
    version: Optional[float] = 2.9
    script_path: Optional[str] = None
    log_file: str = f"{str(Path(__file__).parent)}/changes.txt"
    python_mark: Optional[str] = r"```(python|py|)\n(?P<code>[\s\S]+?)\n```"

    def __init__(self):
        pass

    @staticmethod
    def read_code(text: str, code_mark: str) -> str: # type: ignore
        match = re.search(code_mark, text)
        if match:
            return match.group("code")

    def save_changes(self, text: str) -> None:
        with open(self.log_file, "a") as file: # type: ignore
            file.write(text)
        print(f"Changes saved to log {self.log_file}")

    def check_syntax_errors(self, code: str, filename: str = "<string>") -> bool:
        try:
            compile(code, filename, mode="exec")
        except SyntaxError as e:
            raise SyntaxError(f"Syntax Error in {filename}: Line {e.lineno}: {e.msg}")
        return True

    def format_code(self, code: str) -> str:
        return autopep8.fix_code(code)

    def generate_coverage_report(self, code: str) -> None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(code.encode())
            temp_file_path = temp_file.name

        cov = coverage.Coverage(data_file=temp_file.name)
        cov.start()
        subprocess.run(["python", temp_file.name])
        cov.stop()
        cov.save()
        cov.report(show_missing=True, skip_covered=True, ignore_errors=True)

        os.remove(temp_file.name)
        os.remove(".coverage")

    def improve_code(self, path: Optional[str] = None) -> None:
        """Improves the code in a given file or all files in a given directory."""
        if self.script_path and os.path.exists(self.script_path):
            path = self.script_path
        else:
            parser = argparse.ArgumentParser(description="Improves the code in a given file or all files in a given directory.")
            parser.add_argument("path", nargs="?", help="The path of the file you want to improve")
            args = parser.parse_args()
            path = args.path

        if path != "":
            if os.path.isfile(path):
                paths = [path]
            elif os.path.isdir(path):
                print(os.path.isdir(path))
                paths = list(Path(path).rglob("*.py"))
            else:
                print("Invalid path.")
                return
        else:
            for file_path in glob(os.path.join(path, "*.py")):
                try:
                    with open(file_path, "r") as file:
                        code = file.read()

                    prompt = f"""
                    You are a pragmatic, procedural, and organized code analyzing and improving agent. 
                    You can ingest, analyze, improve and upgrade scripts.
                    Rules:
                    - Always start the new script with the imports above '#Do Not Change Above Line#'
                    - Don't make a new comment block at the end of the script if one exists, just add or subtract info as needed.
                    - Don't change or move methods, classes or variables that have '#protected' above the definition.
                    - Don't remove any functionality only add functionality.
                    - Don't remove the imports at the top of the script.
                    - Don't add type hints to kwargs.
                    - Don't remove license comments.
                    - The 'Description:' in the bottom 'comment block' is where you describe the script
                    - The 'Usage:' description in the bottom 'comment block' is where you explain the usage.
                    - The 'Use cases:' in the bottom 'comment block' is where you list predicted use cases.
                    - The 'Proposed extra features:' in the bottom 'comment block' is where you list proposed new features.
                    - The 'TODOS:' in the top 'comment block' is where the user will list the todo's.
                    - Create or Update the 'version' variable by adding 0.1 to it.
                    - List the changes you made starting with 'I made the following changes:'.
                    - The 'comment block' at the top of the script is always formatted like this:
                    f'''
                    TODOS:
                            <here the user places todos he wants implemented>
                    '''
                    f'''
                    - The 'comment block' at the bottom of the script is always formatted like this:                     
                    Description:
                        <here the assistant describes script working>
                    Usage:
                        <here the assistant describes script usage>
                    Predicted use cases:
                        <here the assistant describes use cases>
                    Proposed features:
                        <here the assistant proposes features>
                    '''
                    """

                    improve_task = f"""
                    Tasks:
                    - 1 Refactor the code into a callable class if needed.
                    - 2 Add a __name__ == "__main__" if needed.
                    - 3 Implement the items the user listed under 'TODOS:' in the top 'comment block'.
                    - 4 Add or change variables, methods, enums, classes and logic to improve and enhance the script.
                    - 5 Add type hints.
                    - 6 Update the bottom 'comment block' with relevant information.
                    Now improve the  code in this file:
                    ```py
                    {code}
                    ```
                    """

                    response = []
                    model = models.gpt_35_turbo
                    for chunk in ChatCompletion(
                        model=model,
                        messages=[
                            {"role": "system", "content": prompt},
                            {"role": "user", "content": improve_task},
                        ],
                        timeout=6000,
                        stream=False,
                    ):
                        response.append(chunk)
                        print(chunk, end="", flush=True)
                    response = "".join(response)
                    code = self.read_code(response, self.python_mark)

                    if code:
                        self.check_syntax_errors(code)
                        code = self.format_code(code)
                        new_file_path = str(Path(path).with_name(
                            f"{Path(path).stem}_generated_{str(self.version).replace('.', '_')}_improvement{Path(path).suffix}"))
                        with open(new_file_path, "w") as file:
                            file.write(code)
                        print(f"Improved code saved to {new_file_path}")
                    changes = response.split("I made the following changes:")
                    changes = f"I made the following changes in version {self.version}:\n{changes.pop()}"
                    self.save_changes(changes)
                except FileNotFoundError:
                    print("Invalid file path.")

if __name__ == "__main__":
    CodeImprover().improve_code()

"""
Description:
This script is a code improvement tool that allows you to analyze and enhance the quality of Python scripts. 
It uses a GPT-3 model for natural language processing to interact with the user and make iterative improvements to the code. 
The code is checked for syntax errors, formatted using autopep8, and a code coverage report is generated. 
The improved code is then saved to a new file.

Usage:
1. Run the script.
2. Enter the path of the file you want to improve or leave it empty to self-improve.
3. Follow the prompts and suggestions provided by the assistant.
4. The improved code will be saved to a new file with the version number and "improvement" in the filename.

Predicted use cases:
- Improving the quality and readability of existing Python scripts.
- Learning Python best practices and coding standards.
- Generating code coverage reports for testing purposes.

Proposed features:

- Support for other programming languages.
"""