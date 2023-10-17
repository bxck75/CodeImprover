import os
from typing import Dict, Any
#import openai
#openai.api_key = os.environ.get("OPENAI_API_KEY")

from langchain_g4f import G4FLLM
from llama_index.llms import OpenAI, ChatMessage
from llama_index.tools import BaseTool, FunctionTool
from llama_index.agent import OpenAIAgent
from llama_index.agent.react.base import ReActAgent
from llama_index.llms import OpenAI

def bash_shell(command: str) -> str:
    """Run a bash command and return its """
    return os.popen(command).read()

def python_fun(script: str) -> None:
    """
    Run a python script, save outut in `result` variable
    args:
        script: a string of python code
    return:
        local variable named `result`
    """
    # execute the argument as a python script
    print ("executing python script: ---", script)
    print("   ---   ")
    loc = {}
    exec(script, {}, loc)
    return loc.get("result", None)

def multiply(a: int, b: int) -> int:
    """Multiple two integers and returns the result integer"""
    return a * b

def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    return a + b

multiply_tool = FunctionTool.from_defaults(fn=multiply)
add_tool = FunctionTool.from_defaults(fn=add)
bash_tool = FunctionTool.from_defaults(fn=bash_shell)
python_tool = FunctionTool.from_defaults(fn=python_fun)

llm = G4FLLM
agent = ReActAgent.from_tools(
    [multiply_tool, add_tool, bash_tool, python_tool],
    llm=llm, 
    verbose=True
)

response = agent.chat("What is (121 * 3) + 42?")
print(str(response))

#response = agent.chat("Draw me a cool picture using matplotlib")
#print(str(response))