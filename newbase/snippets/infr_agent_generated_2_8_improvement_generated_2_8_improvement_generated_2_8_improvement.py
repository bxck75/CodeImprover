from typing import List


class CodeAnalyzer:
    def __init__(self, script: str):
        self.script = script

    def analyze(self) -> List[str]:
        lines = self.script.split("\n")
        imports = []
        classes = []
        methods = []
        variables = []

        for line in lines:
            if line.startswith("import") or line.startswith("from"):
                imports.append(line)
            elif line.startswith("class"):
                classes.append(line)
            elif line.startswith("def"):
                methods.append(line)
            elif "=" in line:
                variables.append(line)

        return imports, classes, methods, variables


if __name__ == "__main__":
    script = '''
    #Do Not Change Above Line#

    import os
    import sys

    #protected
    class MyClass:
        def __init__(self, name: str):
            self.name = name

        def say_hello(self):
            print("Hello, " + self.name)
    
    def my_function():
        print("This is a function")

    my_variable: int = 10

    #protected
    def another_function():
        print("Another function")

    #Do Not Change Below Line#
    '''

    code_analyzer = CodeAnalyzer(script)
    imports, classes, methods, variables = code_analyzer.analyze()

    print("Imports:")
    for imp in imports:
        print(imp)

    print("Classes:")
    for cls in classes:
        print(cls)

    print("Methods:")
    for method in methods:
        print(method)

    print("Variables:")
    for var in variables:
        print(var)
