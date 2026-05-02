import time
import threading
import typer
from pathlib import Path
from ai_toolkit.core.client import ask

import os
os.system("")  # enable ANSI on Windows

app = typer.Typer()

SPINNER_FRAMES = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]


def spinning(stop_event):
    i = 0
    while not stop_event.is_set():
        frame = SPINNER_FRAMES[i % len(SPINNER_FRAMES)]
        print(f"\r\033[96m  {frame} Summarizing...\033[0m", end="", flush=True)
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
def file(path: Path = typer.Argument(..., help="File to summarize")):
    """Summarize a text file."""
    content = path.read_text()

    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinning, args=(stop_event,))
    spinner_thread.start()

    try:
        summary = ask(f"Summarize this:\n\n{content}")
    finally:
        stop_event.set()
        spinner_thread.join()

    typewriter(summary)


@app.command()
def text(input: str = typer.Argument(...)):
    """Summarize a string of text."""
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinning, args=(stop_event,))
    spinner_thread.start()

    try:
        result = ask(f"Summarize: {input}")
    finally:
        stop_event.set()
        spinner_thread.join()

    typewriter(result)