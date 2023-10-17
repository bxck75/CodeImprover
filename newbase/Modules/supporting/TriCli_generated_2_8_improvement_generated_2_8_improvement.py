import argparse
import os
from typing import List
from huggingface_hub import InferenceClient
from secret import HUGGINGFACE_TOKEN

# Define STOP_SEQUENCES here
STOP_SEQUENCES = ["\nUser:", "", " User:", "###"]


class FalconChatCLI:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.seed = 666

    def format_prompt(self, message: str, history: List[str], system_prompt: str) -> str:
        prompt = ""
        if system_prompt:
            prompt += f"System: {system_prompt}\n"
        for user_prompt, bot_response in history:
            prompt += f"User: {user_prompt}\n"
            # Response already contains "Falcon: "
            prompt += f"Falcon: {bot_response}\n"
        prompt += f"""User: {message}
Falcon:"""
        return prompt

    def generate(
        self, prompt: str, history: List[str], system_prompt: str = "", temperature: float = 0.9,
        max_new_tokens: int = 256, top_p: float = 0.95, repetition_penalty: float = 1.0,
    ) -> str:
        temperature = float(temperature)
        if temperature < 1e-2:
            temperature = 1e-2
        top_p = float(top_p)
        generate_kwargs = dict(
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            stop_sequences=STOP_SEQUENCES,
            do_sample=True,
            seed=self.seed,
        )
        self.seed = self.seed + 1
        formatted_prompt = self.format_prompt(prompt, history, system_prompt)

        stream = client.text_generation(
            formatted_prompt, **generate_kwargs, stream=True, details=True, return_full_text=False)
        output = ""

        for response in stream:
            output += response.token.text

            for stop_str in STOP_SEQUENCES:
                if output.endswith(stop_str):
                    output = output[:-len(stop_str)]
                    output = output.rstrip()
                    yield output
            yield output
        return output

    def main(self):
        parser = argparse.ArgumentParser(description="Falcon-180B Chat CLI")
        parser.add_argument("message", type=str, help="The user's message")
        parser.add_argument("--system-prompt", type=str,
                            help="Optional system prompt")
        parser.add_argument("--temperature", type=float,
                            default=0.9, help="Temperature (default: 0.9)")
        parser.add_argument("--max-new-tokens", type=int,
                            default=256, help="Max new tokens (default: 256)")
        parser.add_argument("--top-p", type=float, default=0.90,
                            help="Top-p (nucleus sampling) (default: 0.90)")
        parser.add_argument("--repetition-penalty", type=float,
                            default=1.2, help="Repetition penalty (default: 1.2)")

        args = parser.parse_args()

        HF_TOKEN = os.environ.get("HF_TOKEN", self.api_token)
        print(HF_TOKEN)
        API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-180B-chat"

        client = InferenceClient(
            API_URL,
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
        )

        history = []  # Store conversation history here
        system_prompt = args.system_prompt if args.system_prompt else ""
        message = args.message

        generator = self.generate(
            message,
            history,
            system_prompt=system_prompt,
            temperature=args.temperature,
            max_new_tokens=args.max_new_tokens,
            top_p=args.top_p,
            repetition_penalty=args.repetition_penalty,
        )

        for response in generator:
            print(response)


if __name__ == "__main__":
    falcon_chat_cli = FalconChatCLI(api_token=HUGGINGFACE_TOKEN)
    falcon_chat_cli.main()
#protected
f'''
Description:
    <here the assistant describes script working>
Usage:
    <here the assistant describes script usage>
Predicted use cases:
    <here the assistant describes use cases>
Proposed features:
    <here the assistant proposes features>
'''
