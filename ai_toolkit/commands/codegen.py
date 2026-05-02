import typer
import time
import threading
from rich.syntax import Syntax
from rich.console import Console
from ai_toolkit.core.client import ask

app = typer.Typer()
console = Console()

SPINNER_FRAMES = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]


def spinning(stop_event):
    i = 0
    while not stop_event.is_set():
        frame = SPINNER_FRAMES[i % len(SPINNER_FRAMES)]
        print(f"\r\033[96m  {frame} Generating code...\033[0m", end="", flush=True)
        time.sleep(0.08)
        i += 1
    print("\r" + " " * 40 + "\r", end="", flush=True)


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def generate(
    ctx: typer.Context,
    lang: str = typer.Option("python", "--lang", "-l", help="Programming language"),
    model: str = typer.Option("minimax/minimax-m2.5:free", "--model", "-m", help="Model to use"),
):
    """Generate code from a description."""
    task = " ".join(ctx.args).strip()

    if not task:
        print("\n\033[38;5;213m  ✦  Usage:\033[0m  \033[38;5;240mai code generate <task> --lang python\033[0m\n")
        raise typer.Exit()

    prompt = f"Write {lang} code to: {task}. Return only the code, no explanation."

    response_holder = {}
    stop_event = threading.Event()

    def fetch():
        try:
            response_holder["result"] = ask(prompt, model=model)
        except Exception as e:
            response_holder["result"] = f"# Error: {e}"
        stop_event.set()

    thread = threading.Thread(target=fetch)
    thread.start()
    spinning(stop_event)
    thread.join()

    code = response_holder.get("result", "# No response.")

    # strip markdown fences if model returns them
    if code.startswith("```"):
        lines = code.split("\n")
        code = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

    print()
    syntax = Syntax(code, lang, theme="monokai", line_numbers=True)
    console.print(syntax)
    print()