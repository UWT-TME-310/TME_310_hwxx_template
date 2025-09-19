"""
Tests for TME 310 Assignment XX (hwXX.ipynb)

This module contains pytest tests to validate student submissions
for a homework assignment template. It will need to be updated for each new assignment.

The module is organized into:
- Fixtures: notebook() and answer_registry() for efficient data loading
- Utility functions: get_cell_tags() and get_script_code_for_problem()
- TestNotebookStructure: Tests for notebook organization and structure
- TestNotebookContent: Tests for response content and quality

Constants:
    ASSIGNMENT_ID: The assignment identifier (update for each assignment)
    NOTEBOOK_PATH: Path to the notebook file being tested
    REQUIRED_SUBPROBLEMS: List of required subproblem tags in sequence
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import nbformat
import pytest
from nbconvert.preprocessors import ExecutePreprocessor

ASSIGNMENT_ID = "XX"
NOTEBOOK_PATH = Path(__file__).parent / f"hw{ASSIGNMENT_ID}.ipynb"
TEST_PARAMS_PATH = Path(__file__).parent / "test_params.json"
REQUIRED_SUBPROBLEMS = ["summarize", "plan", "script", "reflect"]


@pytest.fixture(scope="function")
def current_problem_number(request) -> int:
    """Get the current problem number from the test item."""
    return getattr(request.node, "problem_number", 1)


@pytest.fixture(scope="function")
def problem_script_code(
    current_problem_number: int,
    notebook: Dict[str, Any],
    answer_registry: Dict[str, List[int]],
) -> str:
    """Get script code for the current problem being tested."""
    return get_script_code_for_problem(
        current_problem_number, notebook, answer_registry
    )


@pytest.fixture(scope="function")
def problem_execution_results(
    current_problem_number: int,
    execution_results: Dict[str, Any],
    notebook: Dict[str, Any],
) -> Dict[str, Any]:
    """Get execution results for the current problem being tested."""
    if execution_results.get("execution_failed", False):
        return {"execution_failed": True, "error": execution_results.get("error", "")}

    # Find the problem-specific section key
    cells = notebook["cells"]
    problem_indices = []
    for i, cell in enumerate(cells):
        tags = get_cell_tags(cell)
        if "problem" in tags:
            problem_indices.append(i)

    if current_problem_number > len(problem_indices):
        return {"no_problem_found": True}

    problem_idx = problem_indices[current_problem_number - 1]
    next_problem_idx = (
        problem_indices[current_problem_number]
        if current_problem_number < len(problem_indices)
        else len(cells)
    )

    # Find script sections for this problem
    problem_results = execution_results.get("problem_results", {})
    for section_key, results in problem_results.items():
        if section_key.startswith("script_"):
            section_cell_idx = int(section_key.split("_")[1])
            if problem_idx < section_cell_idx < next_problem_idx:
                return results

    return {"no_execution_data": True}


@pytest.fixture(scope="function")
def problem_content_assertions(
    current_problem_number: int, test_params: Dict[str, Any]
) -> Dict[str, Any]:
    """Get content assertions for the current problem."""
    problem_key = f"problem_{current_problem_number}"
    problem_config = test_params.get(problem_key, {})
    return problem_config.get("content_assertions", {})


@pytest.fixture(scope="function")
def problem_execution_assertions(
    current_problem_number: int, test_params: Dict[str, Any]
) -> Dict[str, Any]:
    """Get execution assertions for the current problem."""
    problem_key = f"problem_{current_problem_number}"
    problem_config = test_params.get(problem_key, {})
    return problem_config.get("execution_assertions", {})


@pytest.fixture(scope="session")
def test_params() -> Dict[str, Any]:
    """Load and return the test parameters configuration."""
    try:
        with open(TEST_PARAMS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Return empty config if file doesn't exist
        return {}


@pytest.fixture(scope="session")
def notebook() -> Dict[str, Any]:
    """Load and return the notebook data."""
    with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def answer_registry(notebook: Dict[str, Any]) -> Dict[str, List[int]]:
    """Build a registry of answer cells for each subproblem section."""
    cells = notebook["cells"]
    answer_registry = {}

    for i, cell in enumerate(cells):
        tags = get_cell_tags(cell)

        for subproblem in REQUIRED_SUBPROBLEMS:
            if subproblem in tags:
                # Find the next subproblem or problem tag
                next_section_idx = len(cells)

                for j in range(i + 1, len(cells)):
                    next_tags = get_cell_tags(cells[j])
                    if "problem" in next_tags or any(
                        sp in next_tags for sp in REQUIRED_SUBPROBLEMS
                    ):
                        next_section_idx = j
                        break

                # Store answer cell indices for this subproblem
                answer_cells = list(range(i + 1, next_section_idx))
                answer_registry[f"{subproblem}_{i}"] = answer_cells

    return answer_registry


@pytest.fixture(scope="session")
def executed_notebook(notebook: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Execute the notebook and return results, handling errors gracefully."""
    try:
        # Read the notebook file directly with nbformat to ensure proper format
        with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        # Configure preprocessor to continue on errors
        ep = ExecutePreprocessor(
            timeout=60,
            kernel_name="python3",
            allow_errors=True,  # Continue execution even if cells fail
        )

        # Execute the notebook
        ep.preprocess(nb, {"metadata": {"path": str(NOTEBOOK_PATH.parent)}})

        # Convert back to dict format for consistency using the notebook's dict representation
        return dict(nb)

    except Exception as e:
        # If execution fails completely, add error info to original notebook
        notebook_copy = notebook.copy()
        notebook_copy["metadata"] = notebook_copy.get("metadata", {})
        notebook_copy["metadata"]["execution_error"] = str(e)
        return notebook_copy


@pytest.fixture(scope="session")
def execution_results(
    executed_notebook: Optional[Dict[str, Any]], answer_registry: Dict[str, List[int]]
) -> Dict[str, Any]:
    """Extract and organize execution results by problem section."""
    if executed_notebook is None:
        return {}

    # Check for complete execution failure
    if "execution_error" in executed_notebook.get("metadata", {}):
        return {
            "execution_failed": True,
            "error": executed_notebook["metadata"]["execution_error"],
            "problem_results": {},
        }

    cells = executed_notebook["cells"]
    problem_results = {}

    # Map results to problems using existing answer_registry
    for section_key, cell_indices in answer_registry.items():
        if section_key.startswith("script_"):  # Focus on script sections
            section_results = {
                "successful_cells": [],
                "failed_cells": [],
                "outputs": [],
                "has_errors": False,
            }

            for cell_idx in cell_indices:
                if cell_idx < len(cells):
                    cell = cells[cell_idx]
                    if cell.get("cell_type") == "code":
                        cell_result = {
                            "cell_index": cell_idx,
                            "execution_count": cell.get("execution_count"),
                            "outputs": cell.get("outputs", []),
                            "source": cell.get("source", ""),
                        }

                        # Check for errors in this cell
                        cell_error = None
                        for output in cell.get("outputs", []):
                            if output.get("output_type") == "error":
                                cell_error = {
                                    "ename": output.get("ename"),
                                    "evalue": output.get("evalue"),
                                    "traceback": output.get("traceback", []),
                                }
                                break

                        if cell_error:
                            cell_result["error"] = cell_error
                            section_results["failed_cells"].append(cell_result)
                            section_results["has_errors"] = True
                        else:
                            section_results["successful_cells"].append(cell_result)

                        # Collect all outputs for this section
                        section_results["outputs"].extend(cell.get("outputs", []))

            problem_results[section_key] = section_results

    return {
        "execution_failed": False,
        "problem_results": problem_results,
        "total_problems": len(
            [k for k in problem_results.keys() if k.startswith("script_")]
        ),
        "problems_with_errors": len(
            [v for v in problem_results.values() if v["has_errors"]]
        ),
    }


def get_cell_tags(cell: Dict[str, Any]) -> List[str]:
    """Extract tags from a notebook cell."""
    metadata = cell.get("metadata", {})
    tags = metadata.get("tags", [])
    return tags


def get_script_code_for_problem(
    problem_number: int, notebook: Dict[str, Any], answer_registry: Dict[str, List[int]]
) -> str:
    """Get all code from script sections for a specific problem.

    Args:
        problem_number: The problem number (1-based)
        notebook: The notebook data
        answer_registry: The answer registry mapping

    Returns:
        Combined code from all script sections for the problem
    """
    cells = notebook["cells"]

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


@pytest.mark.structure
class TestNotebookStructure:
    """Tests that validate the overall structure and organization of the notebook."""

    def test_notebook_exists(self):
        """Test that the notebook file exists."""
        assert NOTEBOOK_PATH.exists(), f"Notebook file {NOTEBOOK_PATH} does not exist"

    def test_problem_subproblem_sequence(self, notebook):
        """Test that every problem is followed by the correct sub-problem tags sequence."""
        cells = notebook["cells"]

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
                for subproblem in REQUIRED_SUBPROBLEMS:
                    if subproblem in tags and subproblem not in found_subproblems:
                        found_subproblems.append(subproblem)

            # Verify all required subproblems are found in order
            missing_subproblems = [
                sp for sp in REQUIRED_SUBPROBLEMS if sp not in found_subproblems
            ]
            assert len(missing_subproblems) == 0, (
                f"Problem at cell {problem_idx} missing subproblems: {missing_subproblems}"
            )

    def test_cells_exist_after_subproblem_tags(self, answer_registry):
        """Test that cells exist after each sub-problem tag."""

        for section_key, answer_cell_indices in answer_registry.items():
            subproblem = section_key.split("_")[0]
            assert len(answer_cell_indices) > 0, (
                f"No response cells found after '{subproblem}' section"
            )


@pytest.mark.content
class TestNotebookContent:
    """Tests that validate the actual content and quality of notebook responses."""

    def test_problem_responses_not_empty(
        self,
        current_problem_number: int,
        notebook: Dict[str, Any],
        answer_registry: Dict[str, List[int]],
    ):
        """Test that response cells for the current problem have content."""
        cells = notebook["cells"]

        # Find problem boundaries
        problem_indices = []
        for i, cell in enumerate(cells):
            tags = get_cell_tags(cell)
            if "problem" in tags:
                problem_indices.append(i)

        assert current_problem_number <= len(problem_indices), (
            f"Problem {current_problem_number} not found in notebook"
        )

        problem_idx = problem_indices[current_problem_number - 1]
        next_problem_idx = (
            problem_indices[current_problem_number]
            if current_problem_number < len(problem_indices)
            else len(cells)
        )

        # Check sections within this problem
        problem_sections_found = False
        for section_key, answer_cell_indices in answer_registry.items():
            subproblem = section_key.split("_")[0]
            section_cell_idx = int(section_key.split("_")[1])

            # Only check sections that belong to current problem
            if problem_idx < section_cell_idx < next_problem_idx:
                problem_sections_found = True

                # Check that all cells in this section have content
                all_empty = True
                for cell_idx in answer_cell_indices:
                    if cell_idx < len(cells):
                        cell = cells[cell_idx]
                        source = cell.get("source", "")

                        # Handle both string and list formats for source
                        if isinstance(source, list):
                            source = "".join(source)

                        # If any cell has content, the section is not empty
                        if source.strip():
                            all_empty = False
                            break

                assert not all_empty, (
                    f"All response cells are empty for '{subproblem}' section in problem {current_problem_number}"
                )

        assert problem_sections_found, (
            f"No sections found for problem {current_problem_number}"
        )

    def test_problem_script_content(
        self,
        current_problem_number: int,
        problem_script_code: str,
        problem_content_assertions: Dict[str, Any],
    ):
        """Test script content for the current problem using test_params.json assertions."""
        assert len(problem_script_code.strip()) > 0, (
            f"Problem {current_problem_number} script section contains no code"
        )

        # Apply content assertions from test_params.json
        self._apply_content_assertions(
            current_problem_number, problem_script_code, problem_content_assertions
        )

    def _apply_content_assertions(
        self,
        problem_number: int,
        script_code: str,
        assertions: Dict[str, Any],
    ):
        """Apply content assertions to script code."""

        # Check required strings/keywords
        if "script_contains" in assertions:
            for required_text in assertions["script_contains"]:
                assert required_text in script_code, (
                    f"Problem {problem_number} script missing required text: '{required_text}'"
                )

        # Check regex patterns
        if "script_patterns" in assertions:
            for pattern in assertions["script_patterns"]:
                assert re.search(pattern, script_code), (
                    f"Problem {problem_number} script missing required pattern: '{pattern}'"
                )

        # Check minimum lines
        if "min_lines" in assertions:
            code_lines = [line for line in script_code.split("\n") if line.strip()]
            assert len(code_lines) >= assertions["min_lines"], (
                f"Problem {problem_number} script has {len(code_lines)} lines, "
                f"expected at least {assertions['min_lines']}"
            )

        # Check for required variables/functions
        if "required_variables" in assertions:
            for var_name in assertions["required_variables"]:
                pattern = rf"\b{re.escape(var_name)}\s*="
                assert re.search(pattern, script_code), (
                    f"Problem {problem_number} script missing required variable: '{var_name}'"
                )

        if "required_functions" in assertions:
            for func_name in assertions["required_functions"]:
                pattern = rf"\bdef\s+{re.escape(func_name)}\s*\("
                assert re.search(pattern, script_code), (
                    f"Problem {problem_number} script missing required function: '{func_name}'"
                )

        # Check for forbidden functions/keywords
        if "forbidden_functions" in assertions:
            for forbidden in assertions["forbidden_functions"]:
                assert forbidden not in script_code, (
                    f"Problem {problem_number} script contains forbidden function: '{forbidden}'"
                )


@pytest.mark.execution
class TestNotebookExecution:
    """Tests that validate notebook code execution and results."""

    def test_problem_execution_status(
        self, current_problem_number: int, problem_execution_results: Dict[str, Any]
    ):
        """Test that the current problem's code executed successfully."""

        # Check for complete execution failure
        if problem_execution_results.get("execution_failed", False):
            pytest.fail(
                f"Problem {current_problem_number} execution failed: {problem_execution_results.get('error', 'Unknown error')}"
            )

        # Check if problem was found
        if problem_execution_results.get("no_problem_found", False):
            pytest.fail(f"Problem {current_problem_number} not found in notebook")

        # Check if execution data exists
        if problem_execution_results.get("no_execution_data", False):
            pytest.fail(f"No execution data found for problem {current_problem_number}")

        # Validate execution data structure
        assert "successful_cells" in problem_execution_results, (
            f"Missing success data for problem {current_problem_number}"
        )
        assert "failed_cells" in problem_execution_results, (
            f"Missing failure data for problem {current_problem_number}"
        )
        assert "has_errors" in problem_execution_results, (
            f"Missing error status for problem {current_problem_number}"
        )

        # Should have attempted to execute at least one cell
        total_cells = len(problem_execution_results["successful_cells"]) + len(
            problem_execution_results["failed_cells"]
        )
        assert total_cells > 0, (
            f"No execution attempts found for problem {current_problem_number}"
        )

    def test_problem_execution_results(
        self,
        current_problem_number: int,
        problem_execution_results: Dict[str, Any],
        problem_execution_assertions: Dict[str, Any],
    ):
        """Test execution results for the current problem using test_params.json assertions."""
        # Skip if no execution data
        if problem_execution_results.get(
            "no_execution_data", False
        ) or problem_execution_results.get("execution_failed", False):
            pytest.skip(
                f"No execution data available for problem {current_problem_number}"
            )

        # Apply execution assertions from test_params.json
        self._apply_execution_assertions(
            current_problem_number,
            problem_execution_results,
            problem_execution_assertions,
        )

    def _apply_execution_assertions(
        self,
        problem_number: int,
        execution_results: Dict[str, Any],
        assertions: Dict[str, Any],
    ):
        """Apply execution assertions to execution results."""

        # Check for no errors requirement
        if assertions.get("no_errors", False):
            assert not execution_results.get("has_errors", False), (
                f"Problem {problem_number} execution has errors but none were expected"
            )

        # Check minimum successful cells
        if "min_successful_cells" in assertions:
            successful_count = len(execution_results.get("successful_cells", []))
            assert successful_count >= assertions["min_successful_cells"], (
                f"Problem {problem_number} has {successful_count} successful cells, "
                f"expected at least {assertions['min_successful_cells']}"
            )

        # Check expected outputs
        if "expected_outputs" in assertions:
            all_outputs = execution_results.get("outputs", [])
            output_text = self._extract_output_text(all_outputs)

            for expected_output in assertions["expected_outputs"]:
                assert expected_output in output_text, (
                    f"Problem {problem_number} missing expected output: '{expected_output}'"
                )

        # Check output patterns
        if "output_patterns" in assertions:
            all_outputs = execution_results.get("outputs", [])
            output_text = self._extract_output_text(all_outputs)

            for pattern in assertions["output_patterns"]:
                assert re.search(pattern, output_text), (
                    f"Problem {problem_number} output missing required pattern: '{pattern}'"
                )

        # Check expected variables (this would require more complex execution analysis)
        if "expected_variables" in assertions:
            # This is a placeholder - implementing variable checking would require
            # more sophisticated execution result parsing
            pass

    def _extract_output_text(self, outputs: List[Dict[str, Any]]) -> str:
        """Extract text content from execution outputs."""
        output_text = ""
        for output in outputs:
            if output.get("output_type") == "stream":
                output_text += output.get("text", "")
            elif output.get("output_type") == "execute_result":
                data = output.get("data", {})
                if "text/plain" in data:
                    output_text += data["text/plain"]
            elif output.get("output_type") == "display_data":
                data = output.get("data", {})
                if "text/plain" in data:
                    output_text += data["text/plain"]
        return output_text


if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])
