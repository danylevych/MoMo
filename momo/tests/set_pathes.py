import sys
import os

current_file_path = os.path.abspath(__file__)
tests_dir = os.path.dirname(current_file_path)
project_root_dir = os.path.dirname(os.path.dirname(tests_dir))
sys.path.append(project_root_dir)
