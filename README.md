# ai-toolkit-cli

AI Toolkit CLI is a small Typer-based command-line app for AI-assisted terminal workflows. It exposes a single entry point named `ai` and routes into the `chat`, `code`, and `summarize` command groups.

## Features

- Fast command-line access through the `ai` launcher
- OpenRouter-backed chat completions
- Separate command groups for chat, code generation, and summarization
- Simple environment-driven configuration

## Installation

Create a virtual environment and install the project in editable mode:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e .
```

After installation, verify the CLI loads:

```bash
ai --help
```

## Configuration

The client reads `OPENROUTER_API_KEY` from the environment. Store it in a local `.env` file so it is loaded automatically at runtime

```env
OPENROUTER_API_KEY=your_openrouter_key_here
```

Do not commit `.env` or `.pypirc` files.

## Usage

The project currently exposes these command groups:

- `ai chat`
- `ai code`
- `ai summarize`

Use `ai --help` to see the available subcommands and options for each group.

## Project Layout

- `ai_toolkit/main.py` - Typer application and command registration
- `ai_toolkit/commands/` - command group modules
- `ai_toolkit/core/` - OpenRouter client helpers and shared logic
- `install.ps1` and `install.sh` - convenience install scripts

## Publishing

The package metadata is defined in `pyproject.toml`, including the console script entry point and dependency list. Build artifacts such as `dist/` and `*.egg-info/` are already ignored for local development.

## Notes

The repository is still lightweight by design. Add command examples and screenshots here as the CLI grows.
