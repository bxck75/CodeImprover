
from dotenv import load_dotenv
import transformers
from transformers.tools import HfAgent
from hfAgent import agents
from secret import HUGGINGFACE_EMAIL,HUGGINGFACE_PASS,HUGGINGFACE_TOKEN
import os
import json
from json import JSONDecodeError
from pathlib import Path
import huggingface_hub

load_dotenv()


emailHF = os.getenv("emailHF", HUGGINGFACE_EMAIL)
pswHF = os.getenv("pswHF", HUGGINGFACE_PASS ) 
tokenHF = os.getenv("HUGGINGFACE_TOKEN", HUGGINGFACE_TOKEN)

if emailHF != "your-emailHF" or pswHF != "your-pswHF" or tokenHF != "your-huggingface-token":
	os.environ["HUGGINGFACEHUB_API_TOKEN"] = tokenHF
	os.environ["emailHF"] = emailHF
	os.environ["pswHF"] = pswHF

HuggingAgent = agents.HuggingChatAgent()
StarCoder_agent = HfAgent(url_endpoint="https://api-inference.huggingface.co/models/bigcode/starcoder")
OAS_agent = HfAgent(url_endpoint="https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5")


prompt = input(">>> Input prompt:\n>")
while prompt != "exit":
    result = StarCoder_agent.run(prompt, remote=True)
    finalresult = OAS_agent.run(result, remote=True)
print(finalresult)
    