import typer
from rich.syntax import Syntax
from rich.console import Console
from ai_toolkit.core.client import ask

app = typer.Typer()
console = Console()

@app.command()
def generate(
    task: str = typer.Argument(..., help="What code to generate"),
    lang: str = typer.Option("python", "--lang", "-l")
):
    """Generate code from a description."""
    prompt = f"Write {lang} code to: {task}. Return only the code."
    code = ask(prompt)
    syntax = Syntax(code, lang, theme="monokai", line_numbers=True)
    console.print(syntax)