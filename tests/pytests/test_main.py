# PyTest for testMain.c as an argument passed into main.py

import subprocess

def test_main_c_compilation():
    """Test that testMain.c compiles successfully."""
    result = subprocess.run(["gcc", "tests/source_files/testMain.c", "-o", "tests/source_files/testMain"], capture_output=True)
    assert result.returncode == 0, f"Compilation failed with error: {result.stderr.decode()}"
    
def test_python_script_execution():
    result = subprocess.run(["python", "main.py", "-L", "tests/source_files/testMain.c"], capture_output=True)
    assert result.returncode == 0, f"Execution failed with error: {result.stderr.decode()}"