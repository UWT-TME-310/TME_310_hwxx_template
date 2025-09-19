# TME 310 Homework Testing Framework

## Overview

This testing framework provides comprehensive validation for TME 310 Jupyter notebook homework assignments. It supports both structural validation and content/execution testing on a per-problem basis, making it ideal for GitHub Classroom integration.

## Test Structure

The framework is organized into three main test categories:

### 1. Structure Tests (`@pytest.mark.structure`)
- **Always run by default** - validates basic notebook organization
- Tests for required problem/subproblem sequence
- Ensures response cells exist after each section
- **Command**: `pytest` (runs structure tests only by default)

### 2. Content Tests (`@pytest.mark.content`) 
- **Requires `--problem N`** - validates response content quality
- Checks for non-empty responses
- Validates script content against JSON-configured assertions
- **Command**: `pytest --problem 1 -m content`

### 3. Execution Tests (`@pytest.mark.execution`)
- **Requires `--problem N`** - validates code execution
- Executes notebook cells and checks results
- Validates outputs against JSON-configured assertions
- **Command**: `pytest --problem 1 -m execution`

## Usage Examples

### GitHub Classroom Integration

```bash
# Structure validation only (default - runs for all submissions)
pytest

# Problem 1 content validation (specific points)
pytest --problem 1 -m content

# Problem 1 execution validation (specific points)
pytest --problem 1 -m execution

# Problem 2 full validation (content + execution)
pytest --problem 2 -m "content or execution"
```

### Development/Debugging

```bash
# Run all tests for problem 1
pytest --problem 1

# Verbose output for debugging
pytest --problem 1 -v

# Run only structure tests with details
pytest -m structure -v
```

## Configuration Files

### `test_params.json`

This file defines problem-specific assertions for content and execution testing:

```json
{
  "problem_1": {
    "content_assertions": {
      "script_contains": ["import", "def", "return"],
      "script_patterns": ["\\\\bfor\\\\b.*:", "\\\\bif\\\\b.*:"],
      "min_lines": 10,
      "required_variables": ["result", "data"],
      "required_functions": ["calculate"],
      "forbidden_functions": ["eval", "exec"]
    },
    "execution_assertions": {
      "expected_outputs": ["Hello World", "42"],
      "output_patterns": ["\\\\d+\\\\.\\\\d+", "Result: .*"],
      "no_errors": true,
      "min_successful_cells": 1
    }
  }
}
```

#### Content Assertions
- `script_contains`: Required strings/keywords in code
- `script_patterns`: Required regex patterns in code
- `min_lines`: Minimum number of non-empty code lines
- `required_variables`: Variable names that must be assigned
- `required_functions`: Function names that must be defined
- `forbidden_functions`: Functions that should not be used

#### Execution Assertions
- `expected_outputs`: Exact strings that must appear in output
- `output_patterns`: Regex patterns that must match output
- `no_errors`: Whether execution must be error-free
- `min_successful_cells`: Minimum number of cells that must execute successfully

### `pytest.ini`

Controls default test behavior:

```ini
[tool:pytest]
addopts = -m structure
markers =
    structure: Tests for notebook structure and organization
    content: Tests for response content and quality  
    execution: Tests for code execution and results
```

## File Structure

```
├── hwXX.ipynb              # Student notebook (XX = assignment number)
├── test_hwXX.py            # Main test file
├── test_params.json        # Assertion configuration
├── pytest.ini             # Pytest configuration
└── requirements.txt        # Testing dependencies
```

## Notebook Requirements

### Required Tags
Student notebooks must use these cell tags:

- `problem`: Marks the start of each problem
- `summarize`: Analysis/summary sections
- `plan`: Planning sections  
- `script`: Code implementation sections
- `reflect`: Reflection sections

### Example Notebook Structure
```
Cell 1: # Problem 1 [tag: problem]
Cell 2: ## Summarize [tag: summarize] 
Cell 3: [response content]
Cell 4: ## Plan [tag: plan]
Cell 5: [response content]
Cell 6: ## Script [tag: script]
Cell 7: [code content]
Cell 8: ## Reflect [tag: reflect]
Cell 9: [response content]
```

## Customization for New Assignments

### 1. Update Constants
```python
ASSIGNMENT_ID = "01"  # Change XX to assignment number
REQUIRED_SUBPROBLEMS = ["summarize", "plan", "script", "reflect"]  # Modify as needed
```

### 2. Configure test_params.json
Add problem-specific assertions for each problem in the assignment.

### 3. Update requirements.txt
Add any additional testing dependencies if needed.

## Integration with GitHub Classroom

### Autograding Setup

1. **Structure Check** (Always runs, base points):
   ```yaml
   - name: Test Notebook Structure
     run: pytest -v
   ```

2. **Problem-Specific Tests** (Individual point values):
   ```yaml
   - name: Problem 1 Content
     run: pytest --problem 1 -m content -v
     
   - name: Problem 1 Execution  
     run: pytest --problem 1 -m execution -v
   ```

### Point Distribution Example
- Structure: 10 points (base requirement)
- Problem 1 Content: 15 points
- Problem 1 Execution: 25 points
- Problem 2 Content: 15 points  
- Problem 2 Execution: 25 points
- Problem 3 Content: 5 points
- Problem 3 Execution: 5 points

## Troubleshooting

### Common Issues

1. **No tests run**: Make sure you're using `--problem N` for content/execution tests
2. **Import errors**: Install requirements with `pip install -r requirements.txt`
3. **Execution timeouts**: Increase timeout in `ExecutePreprocessor` configuration
4. **Missing assertions**: Check `test_params.json` exists and has correct problem keys

### Debug Commands

```bash
# Check which tests will run
pytest --collect-only

# Run with maximum verbosity
pytest --problem 1 -vvv

# Show local variables on failure
pytest --problem 1 --tb=long

# Run without capturing output (see print statements)
pytest --problem 1 -s
```