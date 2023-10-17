# Do Not Change Above Line#

from dotenv import load_dotenv
import os
from pathlib import Path
import huggingface_hub
from transformers.tools import HfAgent
from secret import HUGGINGFACE_EMAIL, HUGGINGFACE_PASS, HUGGINGFACE_TOKEN
from hfAgent import agents

load_dotenv()


class ChatAgent:
    def __init__(self):
        emailHF = os.getenv("emailHF", HUGGINGFACE_EMAIL)
        pswHF = os.getenv("pswHF", HUGGINGFACE_PASS)
        tokenHF = os.getenv("HUGGINGFACE_TOKEN", HUGGINGFACE_TOKEN)

        if emailHF != "your-emailHF" or pswHF != "your-pswHF" or tokenHF != "your-huggingface-token":
            os.environ["HUGGINGFACEHUB_API_TOKEN"] = tokenHF
            os.environ["emailHF"] = emailHF
            os.environ["pswHF"] = pswHF

        self.HuggingAgent = agents.HuggingChatAgent()
        self.StarCoder_agent = HfAgent(
            url_endpoint="https://api-inference.huggingface.co/models/bigcode/starcoder")
        self.OAS_agent = HfAgent(
            url_endpoint="https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5")

    def run(self):
        prompt = input(">>> Input prompt:\n>")
        while prompt != "exit":
            result = self.StarCoder_agent.run(prompt, remote=True)
            final_result = self.OAS_agent.run(result, remote=True)
            print(final_result)
            prompt = input(">>> Input prompt:\n>")


if __name__ == "__main__":
    chat_agent = ChatAgent()
    chat_agent.run()

'''
TODOS:
    - Refactor the code into a callable class.
    - Add a __name__ == "__main__" block.
    - Implement the user's TODOs.
    - Add type hints.
'''

# Do Not Change Below Line#
'''
Description:
    This script initializes a chat agent that interacts with Hugging Face models for generating responses to user prompts.
Usage:
    Run the script, and it will continuously prompt for user input until "exit" is entered.
Predicted use cases:
    - Quick interactions with Hugging Face models for generating text-based responses.
Proposed features:
    - Allow customization of the Hugging Face models used.
    - Add error handling for unexpected input.
    - Save chat history to a file.
'''
