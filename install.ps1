# AI Toolkit CLI - One-line installer
# Usage: powershell -c "irm https://raw.githubusercontent.com/YOUR_USERNAME/ai-toolkit-cli/main/install.ps1 | iex"

Write-Host ""
Write-Host "  ╔══════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "  ║      AI Toolkit CLI Installer        ║" -ForegroundColor Magenta
Write-Host "  ║      Powered by OpenRouter           ║" -ForegroundColor DarkGray
Write-Host "  ╚══════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""

# ── Step 1: Check Python ──────────────────────────────
Write-Host "  [1/4] Checking Python..." -ForegroundColor Cyan
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "  [ERROR] Python not found." -ForegroundColor Red
    Write-Host "  Install from: https://python.org" -ForegroundColor Yellow
    exit 1
}
$pyVersion = python --version 2>&1
Write-Host "  ✓ Found $pyVersion" -ForegroundColor Green

# ── Step 2: Install ───────────────────────────────────
Write-Host ""
Write-Host "  [2/4] Installing AI Toolkit CLI..." -ForegroundColor Cyan
pip install ai-toolkit-cli --upgrade -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [ERROR] Installation failed." -ForegroundColor Red
    Write-Host "  Try manually: pip install ai-toolkit-cli" -ForegroundColor Yellow
    exit 1
}
Write-Host "  ✓ Installed successfully" -ForegroundColor Green

# ── Step 3: Verify ────────────────────────────────────
Write-Host ""
Write-Host "  [3/4] Verifying installation..." -ForegroundColor Cyan
if (-not (Get-Command ai -ErrorAction SilentlyContinue)) {
    Write-Host "  [ERROR] 'ai' command not found." -ForegroundColor Red
    Write-Host "  Try: pip install ai-toolkit-cli" -ForegroundColor Yellow
    exit 1
}
Write-Host "  ✓ 'ai' command is ready" -ForegroundColor Green

# ── Step 4: Setup API key ─────────────────────────────
Write-Host ""
Write-Host "  [4/4] Setting up API key..." -ForegroundColor Cyan
Write-Host ""

$configDir  = "$HOME\.ai-toolkit"
$configFile = "$configDir\config.env"

# Check if key already saved
if (Test-Path $configFile) {
    $existing = Get-Content $configFile | Where-Object { $_ -match "OPENROUTER_API_KEY=(.+)" }
    if ($existing) {
        Write-Host "  ✓ API key already saved — skipping setup" -ForegroundColor Green
        Write-Host "  Run 'ai setup' to change it anytime." -ForegroundColor DarkGray
    }
} else {
    Write-Host "  Get your free key at: https://openrouter.ai/keys" -ForegroundColor Cyan
    Write-Host ""
    $key = Read-Host "  Paste your OpenRouter API key"

    if ($key -and $key.StartsWith("sk-")) {
        # Save the key
        if (-not (Test-Path $configDir)) {
            New-Item -ItemType Directory -Path $configDir | Out-Null
        }
        Set-Content -Path $configFile -Value "OPENROUTER_API_KEY=$key"
        Write-Host ""
        Write-Host "  ✓ API key saved to $configFile" -ForegroundColor Green
        Write-Host "  You won't need to enter it again." -ForegroundColor DarkGray
    } else {
        Write-Host ""
        Write-Host "  ✗ Invalid key — skipping." -ForegroundColor Yellow
        Write-Host "  Run 'ai setup' later to add your key." -ForegroundColor DarkGray
    }
}

# ── Done ──────────────────────────────────────────────
Write-Host ""
Write-Host "  ╔══════════════════════════════════════╗" -ForegroundColor Green
Write-Host "  ║   Installation complete!             ║" -ForegroundColor Green
Write-Host "  ╚══════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "  Try it now:" -ForegroundColor White
Write-Host "  ai" -ForegroundColor Yellow
Write-Host '  ai chat ask-cmd "What is Python"' -ForegroundColor Yellow
Write-Host "  ai summarize file README.md" -ForegroundColor Yellow
Write-Host '  ai summarize text "Hello, World!"' -ForegroundColor Yellow
Write-Host '  ai code generate "How to create a Python function"' -ForegroundColor Yellow
Write-Host "  ai --help" -ForegroundColor Yellow
Write-Host ""