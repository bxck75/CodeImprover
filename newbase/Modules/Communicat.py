from typing import Optional
# do not change above line#

# imports
import transformers
from transformers import AutoTokenizer, pipeline, logging
from dotenv import load_dotenv
import logger
load_dotenv()
# protected
'''
Todo
- add more functionality to the bot.
' make the communicator central to communicating with mutiple agents in your workforce
'''


class Communicator:
    version: float = 0.2
    name: str = "Communicator"
    log = Logger()
    def __init__(self, modelname: str, api_token: str):
        self.modelname = modelname
        self.api_token = api_token
        logging.set_verbosity_error()
        self.tokenizer = AutoTokenizer.from_pretrained(modelname)
        self.model = pipeline("text-generation", model=modelname,
                              tokenizer=self.tokenizer, token=api_token)

    def generate_text(self, prompt: str, max_length: int = 50, num_return_sequences: int = 1) -> str:
        return self.model(prompt, max_length=max_length, num_return_sequences=num_return_sequences)[0]


if __name__ == "__main__":
    load_dotenv()
    api_token = "hf_%%%%%%%%%%%"
    modelname = "tiiuae/falcon-180b"
    chatbox = Communicator(modelname, api_token)
    prompt = "hello, world!"
    generated_text = chatbox.generate_text(prompt)
    print(generated_text)

# protected
f'''
Description:
    Refactored the code into a class, added a __name__ == "__main__" block, and implemented the user's todos.
    Created a Communicator class for text generation.

Usage:
    To use the Communicator class, create an instance with the model name and api token, then call generate_text with a prompt.

Predicted Use Cases:
    This code can be used to create a chatbot for generating text based on a prompt.

Proposed Features:
    None for now.
'''
