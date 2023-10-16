import subprocess
# protected
import sys
# protected
from pathlib import Path

# Do Not Change Above Line#
import re
import random
import os
from typing import Optional
from g4f import ChatCompletion, models, Provider
import autopep8
import tempfile
import coverage
import os

# TODO: make a duplicate as backup and  with filename.bak then overwrite the improved file
# TODO: Have more visual status view when improvment pprocess is running
# TODO: Move prompting texts into a prompts.py file

class CodeImprover:

    version: Optional[float] = 3.0
    script_path: Optional[str] = None
    log_file: Optional[str] = f"{str(Path(__file__).parent)}/changes.txt"

    def __init__(self):
        self.python_mark: Optional[str] = r"```(python|py|)\n(?P<code>[\s\S]+?)\n```"

    @staticmethod
    def read_code(text: str, code_mark: str) -> str:
        match = re.search(code_mark, text)
        if match:
            return match.group("code")
        

    def save_changes(self, text: str) -> None:
        with open(self.log_file, "a") as file:
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
        tempfile = tempfile.NamedTemporaryFile(delete=False) # make the temp file and keep it from deleting
        tempfile.close() # close the tempfile for the os to unlock it
        tempfile.write(code.encode())# now write the damn file
        temp_file_path = tempfile.name
        cov = coverage.Coverage(data_file=tempfile.name)
        cov.start()
        subprocess.run(["python", temp_file.name])
        cov.stop()
        cov.save()
        cov.report(show_missing=True, skip_covered=True, ignore_errors=True)
        os.remove(tempfile.name)
        os.remove(".coverage")
        cov.stop()
        cov.save()
        cov.report(show_missing=True, skip_covered=True, ignore_errors=True)
        os.remove(tempfile.name)
        os.remove(".coverage")

    def improve_code(self, path: Optional[str] = None) -> None:
        """Improves the code in a given file or all files in a given directory."""
        if self.script_path and os.path.exists(self.script_path):
            path = self.script_path
        else:
            path = input("Enter the path of the file you want to improve:(enter to self-improve) ")
            path = path.replace("'","")
        if path != "":
            if os.path.isfile(path):
                paths = [path]
            elif os.path.isdir(path):
                paths = list(Path(path).rglob("*.py"))
            else:
                print("Invalid path.")
                return
        else:
            paths = [str(Path(__file__).parent)]
        for path in paths:
            try:
                with open(os.path.basename(__file__),"r") as file:
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
                - The 'comment block' at the bottom of the script is always formatted like this:
                    f'''
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
                Now improve the code in this file:
                ```py
                {code}
                ```
                """

                response = []
                model = models.gpt_35_turbo
                for chunk in ChatCompletion.create(
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
                    # Check for syntax errors
                    self.check_syntax_errors(code)
                    # Format the code
                    code = self.format_code(code)
                    # Generate a code coverage report
                    self.generate_coverage_report(code)
                    new_file_path = str(Path(path).with_name(
                        f"{Path(path).stem}_generated_{str(self.version).replace('.', '_')}_improvement{Path(path).suffix}"))
                    with open(new_file_path, "w") as file:
                        file.write(code)
                    print(f"Improved code saved to {new_file_path}")
                # split off the changes and save them
                changes = response.split("I made the following changes:")
                changes = f"I made the following changes in version {self.version}:\n{changes.pop()}"
                self.save_changes(changes)
            except FileNotFoundError:
                print("Invalid file path.")

if __name__ == "__main__":
    CodeImprover().improve_code()