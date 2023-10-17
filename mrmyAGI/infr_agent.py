from langchain_g4f import G4FLLM
from langchain.llms.base import LLM
from g4f import Provider, models
from llama_index import ServiceContext
from llama_index.llms import ChatMessage
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.tools import BaseTool, FunctionTool
from langchain.chains.summarize import load_summarize_chain
from inspect import signature
from typing import Any, Awaitable, Callable, Optional, Type
from llama_index.bridge.langchain import StructuredTool, Tool
from llama_index.bridge.pydantic import BaseModel
from llama_index.tools.types import AsyncBaseTool, ToolMetadata, ToolOutput
from llama_index.tools.utils import create_schema_from_function
from llama_index.memory import ConversationBufferMemory, DocumentMemory
from llama_index.agents import ReActAgent

f'''
#Todos
    - first make a tool like the 'python_fun' tool base on a function to search on the search url https://api.python.langchain.com/en/latest/search.html?q=buffer+memory
    - think of more ways to us this documents VectorStore
    - think of more ways to gather data for in VestorStore 
    - try making more agent that uses the tools
    - try making more tools
    - try giving agents memory
    - try using new React agents with new tools using the VectorStore 

ReActAgent class is used to create an agent for the ReAct logic. It has the following parameters:
    The ReActAgent class does not require a specific OpenAI LLM. It can work with any LLM that implements the required interface. In the provided code snippet, the llm parameter is an instance of the LLM class, which represents the language model used by the agent. The specific OpenAI LLM used in the code snippet is initialized with the OpenAI class from the langchain.llms module.
    The ReActAgent class has the following methods:You can use different  LLMs or even LLMs from other providers by creating an instance of the respective LLM class and passing it as the llm parameter when creating an instance of the ReActAgent class. Just make sure that the LLM class you use implements the required interface for interacting with the language model.
    The ReActAgent class has the following methods:
    • tools: A sequence of BaseTool objects that the agent has access to.
    • llm: An instance of the LLM class, which represents the language model used by the agent.
    • memory: An instance of the BaseMemory class, which represents the agent's memory.
    • max_iterations: The maximum number of iterations the agent will perform.
    • react_chat_formatter: An optional ReActChatFormatter object used to format the chat messages.
    • output_parser: An optional ReActOutputParser object used to parse the agent's output.
    • callback_manager: An optional CallbackManager object used to manage callbacks.
    • verbose: A boolean indicating whether the agent should be verbose or not.
    • tool_retriever: An optional ObjectRetriever[BaseTool] object used to retrieve tools based on the input message.
    • from_tools: A class method that creates an instance of ReActAgent from the provided tools, llm, chat history, memory, and other optional parameters.
Tool class: The Tool class is a base class that represents a tool or function. It contains properties and methods that define the behavior and execution of the tool.
    • from_function method: The from_function class method is a convenient way to create a Tool object from a regular Python function. It takes in a function as a parameter and returns a Tool object that wraps the function. The from_function method automatically infers the schema from the function's signature and can also accept additional arguments to customize the tool's behavior.
    • from_class method: The from_class class method is another way to create a Tool object, but instead of using a function, it takes in a class as a parameter. The class should implement the __call__ method, which defines the behavior of the tool. The from_class method creates a Tool object that wraps the class and allows it to be used as a tool within an agent.
Memory types:
    • ConversationBufferMemory: A memory type that stores chat messages in a buffer and allows for reading and writing of the chat history.
    • PersistentMemory: A memory type that stores chat messages in a persistent database, allowing for long-term storage and retrieval of conversation history.
    • EntityMemory: A memory type that focuses on storing and retrieving information about entities mentioned in the conversation, allowing for entity-based querying and retrieval.
    • ContextualMemory: A memory type that maintains a context-specific memory of past interactions, allowing for context-aware responses and information retrieval.
Memory methods:
    • add_user_message(message: str): This method is used to add a user message to the memory. It takes a string parameter representing the user's message and adds it to the memory.
    • add_ai_message(message: str): This method is used to add an AI-generated message to the memory. It takes a string parameter representing the AI's message and adds it to the memory.
    • read_memory() -> List[ChatMessage]: This method is used to read the contents of the memory. It returns a list of ChatMessage objects representing the chat history stored in the memory.
    • write_memory(chat_history: List[ChatMessage]): This method is used to write the chat history to the memory. It takes a list of ChatMessage objects representing the chat history and writes it to the memory.
    • clear_memory(): This method is used to clear the contents of the memory. It removes all stored chat messages from the memory.
'''

document_memory = DocumentMemory()
document_memory.load_document("path/to/document.txt")
#Add the document memory to the agent's memory:
memory.add_memory(document_memory)
#Create the ReAct agent with the defined memory:
agent = ReActAgent(tools=[], llm=None, memory=memory)

llmA: LLM = G4FLLM(model=models.gpt_35_long)
llmB: LLM = G4FLLM(model=models.gpt_35_turbo)
llmC: LLM = G4FLLM(model=models.gpt_4)

# define many tool
def bash_shell(command: str) -> str:
    """Run a bash command and return its """
    return os.popen(command).read()

def python_fun(script: str) -> None:
    """
    Run a python script, save output in `result` variable
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

tools = [multiply_tool, add_tool, bash_tool, python_tool]

agent_long = ReActAgent.from_tools(
    tools,
    llm=llmA, 
    verbose=True
)
agent_turbo = ReActAgent.from_tools(
    tools,
    llm=llmB, 
    verbose=True
)
agent_gpt4 = ReActAgent.from_tools(
    tools,
    llm=llmC, 
    verbose=True
)

service_context = ServiceContext.from_defaults(llm=llmA)
documents = SimpleDirectoryReader('data').load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(service_context=service_context, similarity_top_k=5)
response = query_engine.query("What did the author do growing up?")


print(response)

# Define the memory
memory = ConversationBufferMemory()
# Create a ReAct agent with the defined memory
agent = ReActAgent(tools=[], llm=None, memory=memory)
# Add user and AI messages to the memory
memory.add_user_message("Hello, how can I assist you?")
memory.add_ai_message("I'm an AI assistant. How can I help?")
# Read the contents of the memory
chat_history = memory.read_memory()
for message in chat_history:
    print(f"{message.sender}: {message.content}")


'''
In this example, we first import the necessary modules, including ConversationBufferMemory from the langchain.memory module and ReActAgent from the langchain.agents module. 
Next, we define the memory using the ConversationBufferMemory class. This memory type stores chat messages in a buffer.
Then, we create a ReAct agent by passing an empty list of tools, None for the LLM, and the defined memory.
We can then add user and AI messages to the memory using the add_user_message and add_ai_message methods.
Finally, we read the contents of the memory using the read_memory method and iterate over the chat history to print the sender and content of each message.
Please note that this is a simplified example to demonstrate the basic usage of memory in a ReAct agent. In a real-world scenario, you would typically have more complex interactions and use additional methods and functionalities provided by the Langchain framework.
'''


