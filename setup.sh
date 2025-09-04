#!/bin/bash

# TME 310 Environment Setup Script
# This script configures the marimo environment with AI chat capabilities

echo "🔧 Setting up TME 310 environment..."

# Ensure virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
fi

# Create marimo config directory
mkdir -p ~/.config/marimo

# Copy marimo configuration
echo "⚙️  Configuring marimo..."
cp .config/marimo.toml ~/.config/marimo/marimo.toml

# Check if GitHub Copilot is available
if command -v gh >/dev/null 2>&1; then
    echo "🤖 GitHub CLI found. Checking Copilot access..."
    if gh auth status >/dev/null 2>&1; then
        echo "✅ GitHub authentication verified."
        echo "🎯 Marimo AI chat should work with GitHub Copilot!"
    else
        echo "⚠️  GitHub authentication needed. Run: gh auth login"
        echo "   Then restart the codespace to enable AI chat."
    fi
else
    echo "⚠️  GitHub CLI not found. Installing..."
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
    sudo apt update && sudo apt install gh -y
    echo "   Run: gh auth login"
    echo "   Then restart the codespace to enable AI chat."
fi

echo ""
echo "🚀 Setup complete! You can now:"
echo "   1. Run 'marimo edit homework_xx.py' to start working"
echo "   2. Use AI chat in marimo (if GitHub Copilot is configured)"
echo "   3. All new terminals will automatically use the virtual environment"
echo ""
echo "💡 If AI chat doesn't work, make sure you have GitHub Copilot access"
echo "   and run 'gh auth login' to authenticate."
