import typer
import time
import os
from ai_toolkit.commands import chat, summarize, codegen

os.system("")  # enable ANSI on Windows

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


app = typer.Typer(
    name="ai",
    help="🤖 AI Toolkit CLI — powered by OpenRouter",
    invoke_without_command=True,
    no_args_is_help=False,  # ← important: don't show help when no args
)

@app.callback()
def main(ctx: typer.Context = typer.Option(None, hidden=True, is_eager=True)):
    if ctx.invoked_subcommand is None:
        show_banner()
        raise typer.Exit()

app.add_typer(chat.app, name="chat")
app.add_typer(summarize.app, name="summarize")
app.add_typer(codegen.app, name="code")

if __name__ == "__main__":
    app()