import os
import sys

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

def get_app_root_directory():
    if getattr(sys, 'frozen', False):
        exe_path = os.path.abspath(sys.executable)
        return os.path.dirname(exe_path)
    else:
        return os.path.abspath(os.path.dirname(__file__))