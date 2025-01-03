import sys
import os

# Project paths
project_root = os.path.abspath(os.path.dirname(__file__))
modules_path = os.path.join(project_root, "src/modules")
scripts_path = os.path.join(project_root, "src/scripts")

# Add directories to sys.path for proper imports
for path in [project_root, modules_path, scripts_path]:
    if path not in sys.path:
        sys.path.insert(0, path)
