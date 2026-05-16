import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# ── Config location ───────────────────────────────────
CONFIG_DIR  = Path.home() / ".ai-toolkit"
CONFIG_FILE = CONFIG_DIR / "config.env"

def save_api_key(key: str):
    CONFIG_DIR.mkdir(exist_ok=True)
    CONFIG_FILE.write_text(f"OPENROUTER_API_KEY={key}\n")
    print(f"\n\033[92m  ✓ API key saved to {CONFIG_FILE}\033[0m\n")

def load_api_key() -> str | None:
    # 1. Check environment variable first
    if os.environ.get("OPENROUTER_API_KEY"):
        return os.environ["OPENROUTER_API_KEY"]
    # 2. Check saved config file
    if CONFIG_FILE.exists():
        load_dotenv(CONFIG_FILE, override=True)
        return os.environ.get("OPENROUTER_API_KEY")
    return None

def get_client():
    key = load_api_key()
    if not key:
        print("\n\033[91m  ✗ No API key found.\033[0m")
        print("\033[93m  Run: ai setup\033[0m\n")
        raise SystemExit(1)
    return OpenAI(
        api_key=key,
        base_url="https://openrouter.ai/api/v1",
    )

def ask(prompt: str, system: str = "You are a helpful assistant.", model: str = "minimax/minimax-m2.5:free") -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt}
        ]
    )
    return response.choices[0].message.content