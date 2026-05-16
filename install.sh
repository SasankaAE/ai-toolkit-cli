#!/bin/bash
echo ""
echo "  AI Toolkit CLI Installer"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "  [ERROR] Python not found. Install from https://python.org"
    exit 1
fi

echo "  [1/3] Checking Python..."
python3 --version

echo "  [2/3] Installing AI Toolkit..."
pip3 install ai-toolkit-cli --upgrade -q

echo "  [3/3] Verifying..."
if command -v ai &> /dev/null; then
    echo ""
    echo "  Done! Run: ai chat ask-cmd "What is Python" "
    echo ""
else
    echo "  [ERROR] Failed. Try: pip3 install ai-toolkit-cli"
fi