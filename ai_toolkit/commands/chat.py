import typer
import time
import threading
import os
import shutil
from ai_toolkit.core.client import ask

os.system("")  # enable ANSI on Windows

app = typer.Typer()

SPINNER_FRAMES = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]

def spinning(stop_event):
    i = 0
    while not stop_event.is_set():
        frame = SPINNER_FRAMES[i % len(SPINNER_FRAMES)]
        print(f"\r\033[96m  {frame} Thinking...\033[0m", end="", flush=True)
        time.sleep(0.08)
        i += 1
    print("\r" + " " * 30 + "\r", end="", flush=True)

def typewriter(text: str):
    print("\n\033[96m  ╔═ AI ════════════════════════════╗\033[0m")
    print("  \033[97m", end="", flush=True)
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.008)
    print("\n\033[96m  ╚═════════════════════════════════╝\033[0m\n")

@app.command()
def ask_cmd(
    question: str = typer.Argument(..., help="Question to ask the AI"),
    model: str = typer.Option("minimax/minimax-m2.5:free", "--model", "-m"),
):
    """Ask the AI a question."""
    response_holder = {}
    stop_event = threading.Event()

    def fetch():
        response_holder["result"] = ask(question, model=model)
        stop_event.set()

    thread = threading.Thread(target=fetch)
    thread.start()
    spinning(stop_event)
    thread.join()

    typewriter(response_holder["result"])