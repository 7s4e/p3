import sys
import os

# Add the root project directory to sys.path for proper imports
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Add the `src/modules` directory to sys.path for module imports
modules_path = os.path.join(project_root, "src/modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

# Add the `scripts` directory to sys.path for script imports
scripts_path = os.path.join(project_root, "src/scripts")
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)
