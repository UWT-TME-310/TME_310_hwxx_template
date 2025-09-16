"""
Tests for TME 310 Assignment XX (hwXX.ipynb)

This module contains pytest tests to validate student submissions
for a homework assignment template.
It will need to be updated for each new assignment.
"""

import json
from pathlib import Path

import pytest

ASSIGNMENT_ID = "XX"
NOTEBOOK_PATH = Path(__file__).parent / f"hw{ASSIGNMENT_ID}.ipynb"


def load_notebook():
    """Load and return the notebook data."""
    with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_cell_tags(cell):
    """Extract tags from a notebook cell."""
    metadata = cell.get("metadata", {})
    tags = metadata.get("tags", [])
    return tags


def build_answer_registry(cells):
    """Build a registry of answer cells for each subproblem section."""
    required_subproblems = ["summarize", "plan", "script", "reflect"]
    answer_registry = {}

    for i, cell in enumerate(cells):
        tags = get_cell_tags(cell)

        for subproblem in required_subproblems:
            if subproblem in tags:
                # Find the next subproblem or problem tag
                next_section_idx = len(cells)

                for j in range(i + 1, len(cells)):
                    next_tags = get_cell_tags(cells[j])
                    if "problem" in next_tags or any(
                        sp in next_tags for sp in required_subproblems
                    ):
                        next_section_idx = j
                        break

                # Store answer cell indices for this subproblem
                answer_cells = list(range(i + 1, next_section_idx))
                answer_registry[f"{subproblem}_{i}"] = answer_cells

    return answer_registry


def test_notebook_exists():
    """Test that the notebook file exists."""
    assert NOTEBOOK_PATH.exists(), f"Notebook file {NOTEBOOK_PATH} does not exist"


def test_problem_subproblem_sequence():
    """Test that every problem is followed by the correct sub-problem tags sequence."""
    notebook = load_notebook()
    cells = notebook["cells"]

    required_subproblems = ["summarize", "plan", "script", "reflect"]
    problem_indices = []

    # Find all cells with "problem" tag
    for i, cell in enumerate(cells):
        tags = get_cell_tags(cell)
        if "problem" in tags:
            problem_indices.append(i)

    assert len(problem_indices) > 0, "No cells with 'problem' tag found"

    # Check sequence after each problem
    for problem_idx in problem_indices:
        found_subproblems = []

        # Look ahead from this problem until next problem or end
        next_problem_idx = len(cells)  # Default to end of notebook
        for next_idx in problem_indices:
            if next_idx > problem_idx:
                next_problem_idx = next_idx
                break

        # Check cells between this problem and next problem
        for i in range(problem_idx + 1, next_problem_idx):
            if i >= len(cells):
                break
            tags = get_cell_tags(cells[i])
            for subproblem in required_subproblems:
                if subproblem in tags and subproblem not in found_subproblems:
                    found_subproblems.append(subproblem)

        # Verify all required subproblems are found in order
        missing_subproblems = [
            sp for sp in required_subproblems if sp not in found_subproblems
        ]
        assert len(missing_subproblems) == 0, (
            f"Problem at cell {problem_idx} missing subproblems: {missing_subproblems}"
        )


def test_cells_exist_after_subproblem_tags():
    """Test that cells exist after each sub-problem tag."""
    notebook = load_notebook()
    cells = notebook["cells"]
    answer_registry = build_answer_registry(cells)

    for section_key, answer_cell_indices in answer_registry.items():
        subproblem = section_key.split("_")[0]
        assert len(answer_cell_indices) > 0, (
            f"No response cells found after '{subproblem}' section"
        )


def test_responses_not_empty():
    """Test that all response cells in each section have content."""
    notebook = load_notebook()
    cells = notebook["cells"]
    answer_registry = build_answer_registry(cells)

    for section_key, answer_cell_indices in answer_registry.items():
        subproblem = section_key.split("_")[0]

        # Check that all cells in this section have content
        all_empty = True
        for cell_idx in answer_cell_indices:
            cell = cells[cell_idx]
            source = cell.get("source", "")

            # Handle both string and list formats for source
            if isinstance(source, list):
                source = "".join(source)

            # If any cell has content, the section is not empty
            if source.strip():
                all_empty = False
                break

        assert not all_empty, f"All response cells are empty for '{subproblem}' section"


def test_script_contains_code_cell():
    """Test that at least one response cell for 'script' sections is a code cell."""
    notebook = load_notebook()
    cells = notebook["cells"]
    answer_registry = build_answer_registry(cells)

    script_sections = {
        k: v for k, v in answer_registry.items() if k.startswith("script_")
    }

    for section_key, answer_cell_indices in script_sections.items():
        has_code_cell = False

        for cell_idx in answer_cell_indices:
            cell = cells[cell_idx]
            cell_type = cell.get("cell_type", "")

            if cell_type == "code":
                has_code_cell = True
                break

        assert has_code_cell, f"No code cells found in script section '{section_key}'"


def get_script_code_for_problem(problem_number):
    """Get all code from script sections for a specific problem.

    Args:
        problem_number (int): The problem number (1-based)

    Returns:
        str: Combined code from all script sections for the problem
    """
    notebook = load_notebook()
    cells = notebook["cells"]
    answer_registry = build_answer_registry(cells)

    # Find problem cells
    problem_indices = []
    for i, cell in enumerate(cells):
        tags = get_cell_tags(cell)
        if "problem" in tags:
            problem_indices.append(i)

    if problem_number > len(problem_indices):
        return ""

    problem_idx = problem_indices[problem_number - 1]

    # Find script sections that belong to this problem
    next_problem_idx = (
        problem_indices[problem_number]
        if problem_number < len(problem_indices)
        else len(cells)
    )

    script_code = []
    for section_key, answer_cell_indices in answer_registry.items():
        if section_key.startswith("script_"):
            section_cell_idx = int(section_key.split("_")[1])

            # Check if this script section belongs to the current problem
            if problem_idx < section_cell_idx < next_problem_idx:
                for cell_idx in answer_cell_indices:
                    cell = cells[cell_idx]
                    if cell.get("cell_type") == "code":
                        source = cell.get("source", "")
                        if isinstance(source, list):
                            source = "".join(source)
                        script_code.append(source)

    return "\n".join(script_code)


def test_script_content_template():
    """Template test for script content validation.

    This test can be customized for specific assignments by:
    1. Checking for specific imports
    2. Validating function definitions
    3. Testing for specific patterns or logic
    4. Verifying output format

    Example customizations:
    - assert 'import pandas' in code
    - assert 'def calculate_' in code
    - assert 'plt.show()' in code
    """
    # Example: Test that problem 1 script contains some code
    code = get_script_code_for_problem(1)
    assert len(code.strip()) > 0, "Problem 1 script section contains no code"

    # Add specific content checks here as needed for each assignment
    # Examples:
    # assert 'import' in code, "No import statements found"
    # assert 'def ' in code, "No function definitions found"


if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])
