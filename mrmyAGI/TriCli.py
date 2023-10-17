import argparse
import os
from huggingface_hub import InferenceClient
from secret import HUGGINGFACE_TOKEN
# ... (rest of your imports)
api_token = HUGGINGFACE_TOKEN
# stop seuence 
STOP_SEQUENCES = ["\nUser:", "", " User:", "###"]  # Define STOP_SEQUENCES here

seed =666
def format_prompt(message, history, system_prompt):
    prompt = ""
    if system_prompt:
        prompt += f"System: {system_prompt}\n"
    for user_prompt, bot_response in history:
        prompt += f"User: {user_prompt}\n"
        prompt += f"Falcon: {bot_response}\n" # Response already contains "Falcon: "
    prompt += f"""User: {message}
Falcon:"""
    return prompt

def generate(
    prompt, history, system_prompt="", temperature=0.9, max_new_tokens=256, top_p=0.95, repetition_penalty=1.0,
):
    temperature = float(temperature)
    if temperature < 1e-2:
        temperature = 1e-2
    top_p = float(top_p)
    global seed
    generate_kwargs = dict(
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        stop_sequences=STOP_SEQUENCES,
        do_sample=True,
        seed=seed,
    )
    seed = seed + 1
    formatted_prompt = format_prompt(prompt, history, system_prompt)

    stream = client.text_generation(formatted_prompt, **generate_kwargs, stream=True, details=True, return_full_text=False)
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

def main():
    parser = argparse.ArgumentParser(description="Falcon-180B Chat CLI")
    parser.add_argument("message", type=str, help="The user's message")
    parser.add_argument("--system-prompt", type=str, help="Optional system prompt")
    parser.add_argument("--temperature", type=float, default=0.9, help="Temperature (default: 0.9)")
    parser.add_argument("--max-new-tokens", type=int, default=256, help="Max new tokens (default: 256)")
    parser.add_argument("--top-p", type=float, default=0.90, help="Top-p (nucleus sampling) (default: 0.90)")
    parser.add_argument("--repetition-penalty", type=float, default=1.2, help="Repetition penalty (default: 1.2)")

    args = parser.parse_args()

    HF_TOKEN = os.environ.get("HF_TOKEN", api_token)
    print(HF_TOKEN)
    API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-180B-chat"

    client = InferenceClient(
        API_URL,
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
    )

    history = []  # Store conversation history here
    system_prompt = args.system_prompt if args.system_prompt else ""
    message = args.message

    generator = generate(
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
    main()