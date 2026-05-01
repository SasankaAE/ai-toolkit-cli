import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_client():
    return OpenAI(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
    )

def ask(prompt: str, system: str = "You are a helpful assistant.", model: str = "minimax/minimax-m2.5:free") -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content