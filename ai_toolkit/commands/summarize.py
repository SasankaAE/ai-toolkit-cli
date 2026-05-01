import typer
from pathlib import Path
from ai_toolkit.core.client import ask

app = typer.Typer()

@app.command()
def file(path: Path = typer.Argument(..., help="File to summarize")):
    """Summarize a text file."""
    content = path.read_text()
    summary = ask(f"Summarize this:\n\n{content}")
    print(summary)

@app.command()
def text(input: str = typer.Argument(...)):
    """Summarize a string of text."""
    print(ask(f"Summarize: {input}"))