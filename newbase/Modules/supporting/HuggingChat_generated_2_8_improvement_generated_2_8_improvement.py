from typing import Optional, List, Mapping, Any
from time import sleep
from dotenv import load_dotenv
from hugchat import hugchat
from hugchat.login import login
from langchain.llms.base import llm

load_dotenv()


class HuggingChat(llm):
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.chatbot: Optional[hugchat.chatbot] = None
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
            if self.email is None or self.password is None:
                raise ValueError(
                    "email and password are required. Please check the documentation on GitHub.")
            else:
                if self.conversation == "":
                    sign = login(self.email, self.password)
                    cookies = sign.login()
                    sign.savecookiestodir()
                    self.chatbot = hugchat.chatbot(cookies=cookies.get_dict())
                else:
                    raise ValueError("Something went wrong")

        sleep(2)
        data = self.chatbot.chat(prompt, temperature=0.5, stream=False)

        # add to history
        self.history_data.append({"prompt": prompt, "response": data})

        return data

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "huggingchat"}


if __name__ == "__main__":
    from secret import huggingface_email, huggingface_password

    chatbot = HuggingChat(email=huggingface_email,
                          password=huggingface_password)

    print(chatbot("Hello, how are you?"))
    # Add more interactions here

# Do not change below this line

"""
description:
This script defines a class for interacting with the Hugging Face ChatGPT API. It allows users to have conversations with the ChatGPT model.

usage:
1. Create an instance of the HuggingChat class, providing your Hugging Face email and password.
2. Call the instance with a prompt to interact with the model and get a response.

predicted use cases:
- Interacting with the Hugging Face ChatGPT API for various conversational tasks.

proposed features:
- Implement methods for conversation management.
- Improve error handling and logging.
- Implement more advanced interactions with the ChatGPT model.
"""
