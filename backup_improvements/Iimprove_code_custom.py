# protected
import sys
# protected
from pathlib import Path
# protected

# Do Not Change Above Line#
import re
import random
import os
from typing import Optional
from g4f import ChatCompletion, models, Provider
import autopep8
import coverage
#protected
'''
Todo
Make method of getting file name of improved script back to original name by splitting in _ then taking the part befor the first split and mergin it with the.py ext do this if the name is  longer then 20 characters
Try to Develop infr_agent.py 
'''

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
        """
        Check for syntax errors in the given code.

        Args:
            code (str): The code to be checked for syntax errors.
            filename (str, optional): The name of the file from which the code originates. Defaults to "<string>".

        Returns:
            bool: True if the code has no syntax errors, False otherwise.
        """
        try:
            compile(code, filename, mode="exec")
        except SyntaxError as e:
            raise SyntaxError(f"Syntax Error in {filename}: Line {e.lineno}: {e.msg}")
        return True

    def format_code(self, code: str) -> str:
        return autopep8.fix_code(code)

    def generate_coverage_report(self, code: str) -> None:
        print(f"this is the path {str(Path(__file__).parent)}/temp.py")
        with open(f"{str(Path(__file__).parent)}/temp.py", "w") as file:
            file.write(code)
        cov = coverage.Coverage(data_file=f"{str(Path(__file__).parent)}/temp.py")
        cov.start()
        os.system(f"python {str(Path(__file__).parent)}/temp.py")
        cov.stop()
        cov.save()
        cov.report(show_missing=True,skip_covered=True,ignore_errors=True)
        os.remove(f"{str(Path(__file__).parent)}/temp.py")
        os.remove(f"{str(Path(__file__).parent)}/.coverage")

    def improve_code(self, path: Optional[str] = None) -> None:
        """Improves the code in a given file or all files in a given directory."""

        if self.script_path and os.path.exists(self.script_path):
            path = self.script_path
        else:
            path = input(
                "Enter the path of the file you want to improve:(enter to self-improve) ")

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
                print(path)
                with open(path, "r") as file:
                    code = file.read()
                # TODO: Move prompting texts into a prompts.py file
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
                    try:
                        # Check for syntax errors
                        self.check_syntax_errors(code)
                    except:
                        print("syntax error")

                    # Format the code
                    code = self.format_code(code)

                    try:
                        # Generate a code coverage report
                        self.generate_coverage_report(code)
                    except:
                        print("no data to show")

                    new_file_path = str(Path(path).with_name(
                        f"{Path(path).stem}_generated_{str(self.version).replace('.', '_')}_improvement{Path(path).suffix}"))
                    with open(new_file_path, "w") as file:
                        file.write(code)
                    print(f"Improved code saved to {new_file_path}")
                # split off the changes and save them
                #changes = response.split("I made the following changes:")
                #changes = f"I made the following changes in version {self.version}:\n{changes.pop()}"
                self.save_changes(response)

            except FileNotFoundError:
                print("Invalid file path.")


if __name__ == "__main__":
    CodeImprover().improve_code()
# protected
