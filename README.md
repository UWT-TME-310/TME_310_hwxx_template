# Homework XX: [Assignment Title]

## Quick Start

1. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

2. **Start working with marimo:**
   ```bash
   marimo edit homework_xx.py
   ```

3. **Enable AI Chat (if you have GitHub Copilot):**
   - If prompted, run: `gh auth login`
   - Restart the codespace
   - AI chat will be available in the marimo interface

## Instructions
- Complete `homework_xx.py` using marimo.
- Refer to the objectives and reflection prompts in the notebook.
- Run any provided self-check tests in `/tests` as needed.
- When finished, commit and push your work to your GitHub Classroom repository.

## Assignment Details
- **Due date:** [Fill in]
- **Submission:** [Instructions for submission]
- **Resources:** See `/resources` for platform guides.

## Troubleshooting

### Virtual Environment Issues
If new terminals don't activate the virtual environment automatically:
- Run: `source .venv/bin/activate`
- Or restart the codespace

### AI Chat Not Working
- Ensure you have GitHub Copilot access through your student account
- Run: `gh auth login` and follow the prompts
- Restart the codespace after authentication

### Marimo Issues
- If marimo doesn't start: `source .venv/bin/activate && marimo edit homework_xx.py`
- Check that all dependencies are installed: `uv sync`

## Instructor Checklist (Update before creating assignment repo)
- [ ] Update assignment number/title
- [ ] Add assignment-specific instructions
- [ ] Edit starter code in notebook
- [ ] Add/remove resource files as needed
- [ ] Ensure no solution or grading code is present