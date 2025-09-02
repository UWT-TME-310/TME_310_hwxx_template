import marimo

__generated_with = "0.4.8"
app = marimo.App()


@app.cell
def header():
    """
    # Homework Assignment XX

    **Name:**  
    **Student ID:**  
    **Date:**  

    ---
    """
    return


@app.cell
def instructions():
    """
    ## Instructions

    - Complete all questions below.
    - You may use additional cells for calculations or explanations.
    - Submit your completed notebook as instructed.
    """
    return


@app.cell
def question_1():
    """
    ## Question 1

    _Describe the physical model you are analyzing. What are its key assumptions?_
    """
    # Your answer here:
    answer_1 = ""
    return answer_1


@app.cell
def question_2():
    """
    ## Question 2

    _Write Python code to simulate the model. Show your results below._
    """
    # Your code here:
    import numpy as np
    import matplotlib.pyplot as plt

    # Example simulation (replace with your own)
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    plt.plot(x, y)
    plt.title("Example Simulation")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
    return x, y


@app.cell
def reflection():
    """
    ## Reflection

    _What did you learn from this assignment?_
    """
    # Your reflection here:
    reflection_text = ""
    return reflection_text


if __name__ == "__main__":
    app.run()