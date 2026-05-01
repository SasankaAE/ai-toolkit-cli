# ai-toolkit

`ai-toolkit` is a small Typer-based command-line app for AI-assisted terminal workflows.

## Commands

The CLI is organized into three command groups:

- `chat`
- `code`
- `summarize`

The top-level entry point is `ai`.

## Project Layout

- `main.py` - Typer application and command registration
- `commands/` - command group modules
- `core/` - client and configuration helpers
- `utils/` - shared formatting helpers

## Requirements

The project currently depends on:

- `typer`
- `rich`
- `openai`
- `python-dotenv`

## Setup

1. Create and activate a Python 3.12 virtual environment.
2. Install the project dependencies.
3. Run the CLI help to verify the app loads.

Example:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
ai --help
```

## Environment

Store local configuration in a `.env` file. Keep API keys and machine-specific values out of version control.

## Notes

The repository is still in an early stage, so command modules and supporting helpers are intentionally lightweight. Add usage examples here as the CLI grows.
