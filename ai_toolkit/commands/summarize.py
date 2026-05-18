import time
import threading
import typer
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from ai_toolkit.core.client import ask
import os

os.system("")

app = typer.Typer()
console = Console()

SPINNER_FRAMES = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]


def print_input_box(label: str, content: str):
    console.print()
    console.print(Panel(
        Text(content, style="bold bright_blue"),
        title=f"[bold bright_blue] {label} [/bold bright_blue]",
        border_style="bright_blue",
        padding=(1, 2),
    ))
    console.print()


def spinning_live(stop_event, label: str = "Summarizing"):
    i = 0
    with Live(console=console, refresh_per_second=15) as live:
        while not stop_event.is_set():
            frame = SPINNER_FRAMES[i % len(SPINNER_FRAMES)]
            live.update(Panel(
                Text(f"{frame}  {label}...", style="bold cyan"),
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


def run(prompt: str, input_label: str, input_preview: str, model: str):
    print_input_box(input_label, input_preview)

    response_holder = {}
    stop_event = threading.Event()

    def fetch():
        try:
            response_holder["result"] = ask(prompt, model=model)
        except Exception as e:
            response_holder["result"] = f"Error: {e}"
        stop_event.set()

    thread = threading.Thread(target=fetch, daemon=True)
    thread.start()
    spinning_live(stop_event)
    thread.join()

    typewriter_live(response_holder.get("result", "No response."))


@app.command()
def file(
    path: Path = typer.Argument(..., help="File to summarize"),
    model: str = typer.Option("google/gemini-flash-1.5:free", "--model", "-m"),
):
    """Summarize a text file."""
    if not path.exists():
        console.print(f"\n[red]  ✗ File not found: {path}[/red]\n")
        raise typer.Exit()

    content = path.read_text(encoding="utf-8")
    preview = content[:120].replace(
        "\n", " ") + ("..." if len(content) > 120 else "")
    run(
        prompt=f"Summarize this:\n\n{content}",
        input_label=f" 📄 {path.name} ",
        input_preview=preview,
        model=model,
    )


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def text(
    ctx: typer.Context,
    model: str = typer.Option("minimax/minimax-m2.5:free", "--model", "-m"),
):
    """Summarize a string of text."""
    input_text = " ".join(ctx.args).strip()
    if not input_text:
        console.print("\n[red]  ✗ Please provide text to summarize.[/red]\n")
        raise typer.Exit()

    run(
        prompt=f"Summarize: {input_text}",
        input_label=" 📝 TEXT ",
        input_preview=input_text[:120] +
        ("..." if len(input_text) > 120 else ""),
        model=model,
    )
