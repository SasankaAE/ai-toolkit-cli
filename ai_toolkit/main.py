import typer
import time
import os
import sys
from ai_toolkit.commands import chat, summarize, codegen
from ai_toolkit.core.client import save_api_key, load_api_key

os.system("")

app = typer.Typer(
    name="ai",
    help="🤖 AI Toolkit CLI — powered by OpenRouter",
    invoke_without_command=True,
    no_args_is_help=False,
)

app.add_typer(chat.app, name="chat")
app.add_typer(summarize.app, name="summarize")
app.add_typer(codegen.app, name="code")

@app.command()
def setup():
    """Save your OpenRouter API key permanently."""
    print("\n\033[96m  ╔══════════════════════════════════════╗\033[0m")
    print("\033[96m  ║        AI Toolkit — Setup            ║\033[0m")
    print("\033[96m  ╚══════════════════════════════════════╝\033[0m\n")

    # Check if already set
    existing = load_api_key()
    if existing:
        print(f"\033[92m  ✓ API key already saved: {existing[:12]}...\033[0m")
        overwrite = input("\n  Overwrite? (y/n): ").strip().lower()
        if overwrite != "y":
            print("\n\033[90m  Keeping existing key.\033[0m\n")
            raise typer.Exit()

    print("  Get your free key at: \033[96mhttps://openrouter.ai/keys\033[0m\n")
    key = input("  Paste your API key: ").strip()

    if not key.startswith("sk-"):
        print("\n\033[91m  ✗ Invalid key. Should start with sk-\033[0m\n")
        raise typer.Exit(1)

    save_api_key(key)
    print("\033[90m  You won't need to enter it again.\033[0m\n")


def show_banner():
    banner = """
\033[96m  ╔══════════════════════════════════════════╗
  ║                                          ║
  ║  \033[94m █████╗ ██╗    ████████╗ ██████╗ \033[96m       ║
  ║  \033[94m██╔══██╗██║       ██║   ██╔═══██╗\033[96m       ║
  ║  \033[94m███████║██║       ██║   ██║   ██║\033[96m       ║
  ║  \033[94m██╔══██║██║       ██║   ██║   ██║\033[96m       ║
  ║  \033[94m██║  ██║███████╗  ██║   ╚██████╔╝\033[96m       ║
  ║  \033[94m╚═╝  ╚═╝╚══════╝  ╚═╝    ╚═════╝ \033[96m       ║
  ║                                          ║
  ║  \033[97m🤖 AI Toolkit CLI  v1.0.0           \033[96m    ║
  ║  \033[92m⚡ Powered by OpenRouter            \033[96m    ║
  ║                                          ║
  ╚══════════════════════════════════════════╝\033[0m"""
    for line in banner.split("\n"):
        print(line)
        time.sleep(0.04)
    tagline = "\n  → Type  ai --help  to get started\n"
    print("\033[93m", end="", flush=True)
    for char in tagline:
        print(char, end="", flush=True)
        time.sleep(0.03)
    print("\033[0m")


@app.callback()
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        show_banner()


if __name__ == "__main__":
    app()