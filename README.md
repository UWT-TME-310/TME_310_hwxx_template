# TME 310 Assignment - GitHub Codespaces with Jupyter

## Quick Start (No Installation Required!)

### Step 1: Open in Codespaces
1. Click the green "Code" button above
2. Select "Codespaces" tab  
3. Click "Create codespace on main" (or "Open with Codespaces")
4. Wait for the environment to build (2-3 minutes first time)

### Step 2: Open the Assignment
1. In VS Code, click on `assignment.ipynb` in the file explorer
2. If prompted to "Select Kernel", choose "Python 3.11.x"
3. The Jupyter notebook will open directly in VS Code
4. You're ready to start coding!

### Step 3: Work on Your Assignment
- **Run cells:** Use Shift+Enter or click the play button (▶️) next to each cell
- **Add cells:** Use the +Code or +Markdown buttons in the toolbar
- **Save automatically:** VS Code saves your work continuously
- **Use AI assistance:** GitHub Copilot is enabled - use Ctrl+I for inline suggestions

### Step 4: Submit Your Work
1. **Save your notebook:** Ctrl+S (should already be auto-saved)
2. **Open Source Control:** Click the branch icon (🔀) in the left sidebar
3. **Stage changes:** Click the + next to `assignment.ipynb`
4. **Commit:** Write a message like "Complete assignment" and click ✓
5. **Push:** Click "Sync Changes" to submit to GitHub

## Working with Jupyter in VS Code

### Essential Shortcuts
- **Run cell:** Shift+Enter
- **Run cell and insert below:** Alt+Enter  
- **Add cell above:** A (in command mode)
- **Add cell below:** B (in command mode)
- **Delete cell:** DD (in command mode)
- **Change to markdown:** M (in command mode)
- **Change to code:** Y (in command mode)

### Using AI Assistance Effectively
1. **Inline suggestions:** Start typing and Copilot will suggest completions
2. **AI chat:** Use Ctrl+I to open inline chat for specific help
3. **Context-aware help:** Select code and ask Copilot to explain or improve it
4. **Remember to validate:** Always check that AI suggestions make physical sense!

## Troubleshooting

### Notebook Won't Open
- Refresh the browser tab
- Try closing and reopening `assignment.ipynb`
- Check that Python kernel is selected (bottom right of VS Code)

### Kernel Issues
- Click "Restart" in the kernel status area
- If persistent: Terminal → New Terminal → Run `pip install jupyter`

### Plots Not Showing
- Make sure you have `%matplotlib inline` in your first code cell
- Try `plt.show()` after your plotting commands

### Git Submission Problems
- Make sure you've saved the notebook (Ctrl+S)
- Check that `assignment.ipynb` appears in the Source Control panel
- If stuck, ask for help in office hours!

## Assignment Requirements

### Code Quality
- Include clear comments explaining your approach
- Use descriptive variable names
- Validate your results against physical expectations
- Handle edge cases appropriately

### Documentation Requirements
- Complete the AI interaction log with your actual experiences
- Fill out all reflection questions thoughtfully
- Include physical validation of your results
- Create meaningful visualizations

### Submission Checklist
- [ ] All code cells execute without errors
- [ ] Results are physically reasonable
- [ ] AI interaction log is completed
- [ ] Reflection questions are answered
- [ ] Visualizations support your conclusions
- [ ] Work is committed and pushed to GitHub

## Need Help?
- **Technical issues:** Use the class discussion forum
- **Conceptual questions:** Attend office hours (right after class!)
- **AI assistance:** Remember to document your interactions in the notebook
- **Collaboration:** You can discuss approaches with classmates, but submit individual work

---

*This assignment uses Jupyter notebooks in VS Code - a powerful environment for scientific computing that you'll encounter in your engineering career.*