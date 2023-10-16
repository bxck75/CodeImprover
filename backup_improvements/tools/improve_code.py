
import sys, re
from pathlib import Path
from os import path

sys.path.append(str(Path(__file__).parent.parent.parent))

from g4f import ChatCompletion, models
def read_code(text: str) -> str:
    """
    Extracts code snippets from a given text using regular expressions.

    Args:
        text (str): The text that may contain a code snippet.

    Returns:
        str: The extracted code snippet from the given text.
    """
    pattern = r"```(python|py|)\n(?P<code>[\S\s]+?)\n```"
    match = re.search(pattern, text)
    if match:
        return match.group("code")
    
path = input("Path: ")

with open(path, "r") as file:
    code = file.read()

ingesting_and_analizing_role = f"""You Are a pragmatic, procedural and organized CodeAnalizing Agent.
        Its the year 3145 and ur Task is to ingest and analyze a multi script project inside this folder:
    """

analize_prompt = f"""
Read and analyze all scripts in this folder. Try to get a project wide understanding of this codebase:
```py
{code}
```
Refactor the code into a fully OOP callable class with __name__ == :__main__: and argparse
Don't remove anything only addfunctionality 
Feel free to add methods,enums or classes.
Add typehints if possible.
Add CamelAgent agents to automaatee if possible.
add all new and experimental code in a try-except block
Don't add any typehints to kwargs.
Don't remove license comments.
"""

prompt = f"""
Improve the code in this file:
```py
{code}
```
Don't remove anything.
Add typehints if possible.
Don't add any typehints to kwargs.
Don't remove license comments.
"""

print("Create code...")
response = []
system_prompt = phase_picked_role
user_prompt = phase_picked_prompt
messages = [
    {"role": "system", "content": ingesting_and_analizing_role},
    {"role": "user", "content": analize_prompt}
]
for chunk in ChatCompletion.create(
    model=models.gpt_35_turbo,
    messages=messages,
    timeout=300,
    stream=True
):
    # Process the response chunk
    response.append(chunk)

code = read_code(response)
if code:
    with open(path, "w") as file:
        file.write(code)