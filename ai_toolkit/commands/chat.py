import typer
import time
import threading
import shutil
import os
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from ai_toolkit.core.client import ask

os.system("")

app = typer.Typer()
console = Console()

SPINNER_FRAMES = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]

C_RESET  = "\033[0m"
C_BORDER = "\033[38;5;99m"
C_LABEL  = "\033[38;5;213m"
C_SPINNER= "\033[38;5;87m"


def spinning(stop_event):
    i = 0
    w = shutil.get_terminal_size((80, 20)).columns
    while not stop_event.is_set():
        frame = SPINNER_FRAMES[i % len(SPINNER_FRAMES)]
        msg = f"  {frame}  Thinking..."
        pad = " " * (w - len(msg) - 4)
        print(
            f"\r{C_BORDER}│{C_RESET} {C_SPINNER}{msg}{pad}{C_RESET} {C_BORDER}│{C_RESET}",
            end="", flush=True
        )
        time.sleep(0.08)
        i += 1
    w = shutil.get_terminal_size((80, 20)).columns
    print("\r" + " " * w + "\r", end="", flush=True)


def print_user_box(question: str):
    console.print()
    console.print(Panel(
        Text(question, style="bold bright_blue"),
        title="[bold bright_blue] YOU [/bold bright_blue]",
        border_style="bright_blue",
        padding=(1, 2),
    ))


def print_response_box(text: str):
    console.print()
    console.print(Panel(
        Markdown(text),
        title="[bold magenta] AI [/bold magenta]",
        border_style="magenta",
        padding=(1, 2),
        subtitle="[dim]powered by OpenRouter[/dim]",
    ))
    console.print()


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def ask_cmd(
    ctx: typer.Context,
    model: str = typer.Option("minimax/minimax-m2.5:free", "--model", "-m"),
):
    """Ask the AI a question."""
    question = " ".join(ctx.args).strip()

    if not question:
        console.print("\n[red]  ✗ Please provide a question.[/red]\n")
        raise typer.Exit()

    # User box
    print_user_box(question)

    # Spinner box top
    w = shutil.get_terminal_size((80, 20)).columns
    inner = w - 4
    print(f"\n{C_BORDER}│{C_RESET} {C_SPINNER}  Fetching response...{' ' * (inner - 22)}{C_RESET} {C_BORDER}│{C_RESET}")

    response_holder = {}
    stop_event = threading.Event()

    def fetch():
        try:
            response_holder["result"] = ask(question, model=model)
        except Exception as e:
            response_holder["result"] = f"Error: {e}"
        stop_event.set()

    thread = threading.Thread(target=fetch)
    thread.start()
    spinning(stop_event)
    thread.join()

    print_response_box(response_holder.get("result", "No response."))