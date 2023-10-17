from typing import Optional, List, Mapping, Any
from time import sleep
from dotenv import load_dotenv
from hugchat import hugchat
from hugchat.login import Login
from langchain.llms.base import LLM

load_dotenv()


class HuggingChat(LLM):
    def __init__(self, email: str, psw: str):
        self.email = email
        self.psw = psw
        self.chatbot: Optional[hugchat.ChatBot] = None
        self.conversation: str = ""
        self.history_data: List[Mapping[str, str]] = []
        super().__init__()

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        if self.chatbot is None:
            if self.email is None or self.psw is None:
                raise ValueError(
                    "Email and Password are required. Please check the documentation on GitHub.")
            else:
                if self.conversation == "":
                    sign = Login(self.email, self.psw)
                    cookies = sign.login()
                    sign.saveCookiesToDir()
                    self.chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
                else:
                    raise ValueError("Something went wrong")

        sleep(2)
        data = self.chatbot.chat(prompt, temperature=0.5, stream=False)

        # Add to history
        self.history_data.append({"prompt": prompt, "response": data})

        return data

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "HuggingCHAT"}


if __name__ == "__main__":
    from secret import HUGGINGFACE_EMAIL, HUGGINGFACE_PASS

    llm = HuggingChat(email=HUGGINGFACE_EMAIL, psw=HUGGINGFACE_PASS)

    print(llm("Hello, how are you?"))
    # Add more interactions here

# Do not change below this line
"""
Description:
This script defines a class for interacting with the Hugging Face ChatGPT API. It allows users to have conversations with the ChatGPT model.

Usage:
1. Create an instance of the HuggingChat class, providing your Hugging Face email and password.
2. Call the instance with a prompt to interact with the model and get a response.

Predicted use cases:
- Interacting with the Hugging Face ChatGPT API for various conversational tasks.

Proposed features:
- Implement methods for conversation management.
- Improve error handling and logging.
- Implement more advanced interactions with the ChatGPT model.
"""
