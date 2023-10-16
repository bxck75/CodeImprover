import asyncio
import sys
from pathlib import Path
from typing import List

import g4f
from g4f import ChatCompletion, models, Provider


sys.path.append(str(Path(__file__).parent.parent.parent))

print("create:", end=" ", flush=True)
for response in ChatCompletion.create(
    model=models.gpt_4_32k_0613,
    provider=Provider.GptGod,
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    temperature=0.1,
    stream=True
):
    print(response, end="", flush=True)
print()


async def run_async() -> None:
    response = await ChatCompletion.create_async(
        model=models.gpt_35_turbo_16k_0613,
        provider=Provider.GptGod,
        messages=[{"role": "user", "content": "hello!"}],
    )
    print("create_async:", response)


# asyncio.run(run_async())  # Uncomment this line if you want to run the async function


def main() -> None:
    asyncio.run(run_async())
    

if __name__ == "__main__":
    main()