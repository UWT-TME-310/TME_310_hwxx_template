# TME 310 Assignment - GitHub Codespaces Setup

## Quick Start (No Installation Required!)

### Step 1: Open in Codespaces
1. Click the green "Code" button above
2. Select "Codespaces" tab
3. Click "Create codespace on main" (or "Open with Codespaces")
4. Wait for the environment to build (2-3 minutes first time)

### Step 2: Start marimo
1. Open terminal in VS Code: `Terminal → New Terminal`
2. Run the command: `marimo edit assignment.py`
3. Click the link that appears (usually `http://localhost:2718`)
4. Your assignment will open in a new browser tab

### Step 3: Work on Assignment
- Complete your work in the marimo notebook interface
- marimo automatically saves to `assignment.py`
- Your changes are automatically synced to the Codespace

### Step 4: Submit Your Work
1. In VS Code, go to Source Control panel (Ctrl/Cmd + Shift + G)
2. Stage your changes (click + next to `assignment.py`)
3. Write a commit message (e.g., "Complete assignment")
4. Click "Commit" then "Sync Changes"

## Troubleshooting

**If marimo doesn't start:**
```bash
pip install marimo
marimo edit assignment.py
```

**If you see "port already in use":**
- Close any existing marimo tabs
- Run: `pkill marimo` then try again

**If Codespace seems slow:**
- Codespaces can take a moment to "wake up"
- Try refreshing the browser tab

## Need Help?
- Use VS Code's built-in GitHub Copilot for coding assistance
- Ask questions in our class discussion forum
- Attend office hours for conceptual help

---

*This assignment uses marimo notebooks - a reactive Python environment that automatically updates dependent cells when you make changes.*