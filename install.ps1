# AI Toolkit CLI - One-line installer
# Usage: powershell -c "irm https://raw.githubusercontent.com/YOUR_USERNAME/ai-toolkit-cli/main/install.ps1 | iex"

Write-Host ""
Write-Host "  AI Toolkit CLI Installer" -ForegroundColor Magenta
Write-Host "  Powered by OpenRouter" -ForegroundColor DarkGray
Write-Host ""

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "  [ERROR] Python not found. Install from https://python.org" -ForegroundColor Red
    exit 1
}

Write-Host "  [1/3] Checking Python..." -ForegroundColor Cyan
python --version

# Check pip
Write-Host "  [2/3] Installing AI Toolkit..." -ForegroundColor Cyan
pip install ai-toolkit-cli --upgrade -q

# Verify
Write-Host "  [3/3] Verifying installation..." -ForegroundColor Cyan
if (Get-Command ai -ErrorAction SilentlyContinue) {
    Write-Host ""
    Write-Host "  Installation complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Next steps:" -ForegroundColor White
    Write-Host "  1. Set your API key:" -ForegroundColor DarkGray
    Write-Host '     $env:OPENROUTER_API_KEY="sk-or-..."' -ForegroundColor Yellow
    Write-Host "  2. Run:" -ForegroundColor DarkGray
    Write-Host "     ai chat ask-cmd "What is Python"" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "  [ERROR] Installation failed. Try: pip install ai-toolkit-cli" -ForegroundColor Red
}