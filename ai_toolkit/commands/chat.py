import typer
import time
import threading
import shutil
import os
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from ai_toolkit.core.client import ask

os.system("")

app = typer.Typer()
console = Console()

SPINNER_FRAMES = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]


def print_user_box(question: str):
    console.print()
    console.print(Panel(
        Text(question, style="bold bright_blue"),
        title="[bold bright_blue] YOU [/bold bright_blue]",
        border_style="bright_blue",
        padding=(1, 2),
    ))


def spinning_live(stop_event):
    """Rich live spinner inside a panel."""
    i = 0
    with Live(console=console, refresh_per_second=15) as live:
        while not stop_event.is_set():
            frame = SPINNER_FRAMES[i % len(SPINNER_FRAMES)]
            live.update(Panel(
                Text(f"{frame}  Thinking...", style="bold cyan"),
                title="[bold magenta] AI [/bold magenta]",
                border_style="magenta",
                padding=(1, 2),
            ))
            time.sleep(0.08)
            i += 1


def typewriter_live(text: str, title: str = "AI"):
    displayed = ""
    words = text.split(" ")

    with Live(console=console, refresh_per_second=30) as live:
        for word in words:
            displayed += word + " "
            live.update(Panel(
                Markdown(displayed + "▌"),
                title=f"[bold magenta] {title} [/bold magenta]",
                border_style="magenta",
                padding=(1, 2),
                subtitle="[dim]powered by OpenRouter[/dim]",
            ))
            time.sleep(0.045)

        # Remove cursor on last frame — no second print outside
        live.update(Panel(
            Markdown(displayed.strip()),
            title=f"[bold magenta] {title} [/bold magenta]",
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
    console.print()

    # Fetch with spinner
    response_holder = {}
    stop_event = threading.Event()

    def fetch():
        try:
            response_holder["result"] = ask(question, model=model)
        except Exception as e:
            response_holder["result"] = f"Error: {e}"
        stop_event.set()

    thread = threading.Thread(target=fetch, daemon=True)
    thread.start()
    spinning_live(stop_event)
    thread.join()

    # Typewriter response
    typewriter_live(response_holder.get("result", "No response."))
