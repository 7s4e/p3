import sys
import os

# Ensure src/ directory is included in sys.path for test modules
sys.path.insert(0, 
                os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                             '../src')))
