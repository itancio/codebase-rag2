import os
import sys

def set_module():
    # Add PYTHONPATH to sys.path
    python_path = os.getenv("PYTHONPATH")
    # Dynamically add the parent directory of 'app' to sys.path
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_path and project_path not in sys.path:
        sys.path.append(python_path)
