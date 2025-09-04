# TME 310 Environment Setup Guide for Instructors

This template provides a complete development environment for students with automatic virtual environment activation and AI chat capabilities through marimo and GitHub Copilot.

## What's Configured

### 1. Automatic Virtual Environment
- **devcontainer.json**: Configures the codespace with Python 3.10, Node.js, and required extensions
- **postCreateCommand**: Automatically creates virtual environment and installs dependencies
- **VS Code settings**: Ensures new terminals automatically activate the virtual environment
- **.bashrc**: Fallback activation for virtual environment

### 2. Marimo AI Chat Integration
- **marimo.toml**: Pre-configured for GitHub Copilot integration
- **AI mode**: Set to "ask" for interactive assistance
- **Custom rules**: Tailored for physical modeling assignments
- **Package manager**: Configured to use `uv`

### 3. Required Extensions
- GitHub Copilot and Copilot Chat
- Python language support
- Marimo VS Code extension

## Student Setup Process

1. **Automatic Setup**: When students open the codespace, everything is configured automatically
2. **Run Setup Script**: Students run `./setup.sh` to finalize marimo configuration
3. **GitHub Authentication**: Students run `gh auth login` if they want AI chat
4. **Start Working**: `marimo edit homework_xx.py`

## GitHub Copilot Requirements

For AI chat to work, students need:
- GitHub account with Copilot access (available free for students)
- Authentication via `gh auth login`
- Node.js (automatically installed in the devcontainer)

## Files Created/Modified

### Core Configuration
- `.devcontainer/devcontainer.json` - Codespace environment
- `.vscode/settings.json` - VS Code Python/terminal settings
- `.bashrc` - Virtual environment auto-activation
- `.config/marimo.toml` - Marimo AI configuration template

### Student Tools
- `setup.sh` - Configuration script for students
- Updated `README.md` - Student instructions

## Troubleshooting for Students

### Virtual Environment Issues
- New terminals should automatically activate the environment
- If not: `source .venv/bin/activate`
- Restart codespace if persistent

### AI Chat Issues
- Ensure GitHub Copilot access
- Run `gh auth login`
- Restart codespace after authentication
- Check Node.js is available: `node --version`

### Marimo Issues
- Always run from activated environment
- Check dependencies: `uv sync`
- Restart marimo if configuration changes

## Instructor Customization

### Assignment-Specific Setup
1. Update `homework_xx.py` with assignment content
2. Modify `.config/marimo.toml` AI rules if needed
3. Update `README.md` with assignment details
4. Test in a fresh codespace

### Disabling AI Features
If you don't want AI assistance:
- Remove GitHub Copilot extensions from devcontainer.json
- Set `mode = "manual"` in marimo.toml
- Remove copilot settings from completion section

## Security Considerations

- No API keys are stored in the repository
- GitHub authentication is handled per-student
- All AI interactions go through GitHub's Copilot service
- Students control their own authentication and AI usage

## Testing Checklist

Before distributing to students:
- [ ] Fresh codespace builds successfully
- [ ] Virtual environment activates automatically
- [ ] `./setup.sh` runs without errors
- [ ] `marimo edit homework_xx.py` starts correctly
- [ ] GitHub authentication flow works
- [ ] AI chat responds (if authenticated)
- [ ] All package dependencies install correctly
