import os
import sys
import inspect

CURRENT_DIR = os.path.dirname(
    os.path.abspath(
        inspect.getfile(inspect.currentframe())))

sys.path.append(os.path.abspath(os.path.join(CURRENT_DIR, os.pardir)))