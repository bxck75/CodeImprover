# Do Not Change Above Line

import os
import sys
import textwrap
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from g4f import Provider, models
from langchain.llms.base import LLM
from langchain_g4f import G4FLLM
from dotenv import load_dotenv, find_dotenv
from huggingface_hub import login
from langchain import HuggingFaceHub, LLMChain
from langchain.document_loaders import YoutubeLoader
from langchain_experimental.autonomous_agents import HuggingGPT
from langchain.chains.summarize import load_summarize_chain

# Add the path to the directory containing your_script.py
script_dir = os.path.dirname(os.path.abspath(__file__))
two_folders_up = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(two_folders_up)

# Define a list of LLM agent tools
llm_agent_tools = [
    "document-question-answering",
    "text-question-answering",
    "text-to-speech",
    "huggingface-tools/text-download",
    "context_analysis",
    "knowledge_retrieval",
    "text_generation",
    "data_processing",
    "conversational_logic",
    "task_execution",
    "content_generation",
    "user_interaction",
    "contextual_decision_making",
    "human",
    "llm-math"
]


class LLMChainWrapper:
    def __init__(self, llm_agent_tools, model=models.gpt_35_turbo, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION):
        self.llm_agent_tools = llm_agent_tools
        self.model = model
        self.agent_type = agent_type

    def load_tools(self):
        return load_tools(self.llm_agent_tools)

    def initialize_agent_chain(self):
        hf_tools = self.load_tools()
        llm = G4FLLM(model=self.model)
        agent_chain = initialize_agent(
            hf_tools,
            llm,
            agent=self.agent_type,
            verbose=True,
        )
        return agent_chain

    def run_agent_chain(self, question):
        response = self.agent_chain.run(question)
        wrapped_text = textwrap.fill(
            response, width=100, break_long_words=False, replace_whitespace=False
        )
        return wrapped_text


# Create an instance of the LLMChainWrapper class
llm_chain_wrapper = LLMChainWrapper(llm_agent_tools)

if __name__ == "__main__":
    question = "How do I make a sandwich?"
    response = llm_chain_wrapper.run_agent_chain(question)
    print(response)

# Do Not Change Below Line

'''
Description:
    This script initializes an agent chain for language model tasks, provides a wrapper class to manage the chain,
    and demonstrates its usage.

Usage:
    1. Initialize the LLMChainWrapper with the desired LLM agent tools, model, and agent type.
    2. Call the run_agent_chain method with a question to get a response.

Predicted use cases:
    - Building and managing an agent chain for language model tasks.
    - Automating natural language understanding and generation.

Proposed features:
    - Allow dynamic configuration of agent tools, models, and agent types.
    - Add error handling and input validation.

Version: 0.2
'''
