"""
Test file for TME 310 Assignment
This file shows how to test functions extracted from Jupyter notebooks
"""

import pytest
import numpy as np
import sys
import os

# Add the current directory to path so we can import extracted functions
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_notebook_executes():
    """Test that the notebook can be executed without errors"""
    import subprocess
    result = subprocess.run([
        'jupyter', 'nbconvert', '--to', 'notebook', '--execute', 
        'assignment.ipynb', '--output', 'test_executed.ipynb'
    ], capture_output=True, text=True)
    
    assert result.returncode == 0, f"Notebook execution failed: {result.stderr}"

def test_required_imports():
    """Test that required libraries are imported"""
    try:
        # Import the extracted Python file
        import extracted_functions
        
        # Check that numpy is available (imported in notebook)
        assert hasattr(extracted_functions, 'np') or 'numpy' in dir(extracted_functions)
        
    except ImportError:
        # If extraction failed, check the converted Python file
        with open('assignment_extracted.py', 'r') as f:
            content = f.read()
        
        assert 'import numpy' in content, "NumPy import not found"
        assert 'import matplotlib' in content, "Matplotlib import not found"

def test_function_exists():
    """Test that main function exists"""
    try:
        import extracted_functions
        # Look for common function names students might use
        function_names = ['solve_problem', 'main', 'calculate', 'compute']
        
        has_function = any(hasattr(extracted_functions, name) for name in function_names)
        assert has_function, f"Expected to find one of {function_names} functions"
        
    except ImportError:
        # Check that some function is defined in the code
        with open('assignment_extracted.py', 'r') as f:
            content = f.read()
        
        assert 'def ' in content, "No function definitions found"

def test_basic_functionality():
    """Test basic functionality - customize this for each assignment"""
    try:
        import extracted_functions
        
        # Example test - customize for your specific assignment
        # if hasattr(extracted_functions, 'solve_problem'):
        #     result = extracted_functions.solve_problem()
        #     assert result is not None, "Function should return a result"
        #     assert isinstance(result, (int, float, np.ndarray)), "Result should be numeric"
        
        print("✓ Basic functionality test passed")
        
    except ImportError:
        # If import fails, just check that code exists
        with open('assignment_extracted.py', 'r') as f:
            content = f.read()
        
        # Basic sanity checks
        assert len(content.strip()) > 100, "Assignment appears too short"
        assert 'def ' in content, "No functions defined"

def test_physical_validation():
    """Test that student included validation logic"""
    try:
        import extracted_functions
        
        # Look for validation functions
        validation_functions = ['validate', 'check', 'verify']
        has_validation = any(hasattr(extracted_functions, name) for name in validation_functions)
        
        if not has_validation:
            # Check for validation in the code text
            import inspect
            all_functions = [obj for name, obj in inspect.getmembers(extracted_functions) 
                           if inspect.isfunction(obj)]
            
            for func in all_functions:
                source = inspect.getsource(func)
                if any(word in source.lower() for word in ['validate', 'check', 'verify', 'reasonable']):
                    has_validation = True
                    break
        
        # Don't fail the test, but note if validation is missing
        if not has_validation:
            print("⚠ No explicit validation found - consider adding validation checks")
        else:
            print("✓ Validation logic found")
            
    except ImportError:
        print("⚠ Could not check for validation logic")

if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])