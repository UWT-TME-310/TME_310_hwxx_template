import marimo

__generated_with = "0.9.14"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __(mo):
    mo.md("""
    # TME 310 Assignment Template
    
    ## Getting Started in Codespaces
    
    1. Open terminal in VS Code (Terminal → New Terminal)
    2. Run: `marimo edit assignment.py`
    3. Click the link that appears (usually http://localhost:2718)
    4. Start coding in the marimo interface!
    
    ## Learning Objectives
    - Implement numerical methods in Python
    - Validate results against physical expectations
    - Practice effective AI-assisted programming
    """)
    return


@app.cell
def __(mo):
    mo.md("""
    ## Problem Setup
    
    Replace this cell with your problem statement.
    Use additional cells below for your implementation.
    """)
    return


@app.cell
def __():
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Your code starts here
    return np, plt


@app.cell
def __(mo):
    mo.md("""
    ## AI Interaction Log
    
    Document your AI assistance here:
    - What questions did you ask?
    - How did AI help or mislead you?
    - What validation steps did you take?
    """)
    return


@app.cell
def __(mo):
    mo.md("""
    ## Validation and Reflection
    
    ### Validation Checklist
    - [ ] Units are correct and consistent
    - [ ] Results are physically reasonable
    - [ ] Code handles edge cases appropriately
    - [ ] Compared to analytical solution (if available)
    
    ### Reflection Questions
    1. What was the most challenging aspect?
    2. How did AI assistance help your understanding?
    3. What would you do differently next time?
    """)
    return


if __name__ == "__main__":
    app.run()