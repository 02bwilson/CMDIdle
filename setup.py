from distutils.core import setup
import py2exe

setup(console=['main.py'])

import sys
main_script_dir = "../main.py"
main_folder = main_script_dir.rsplit("\\",1)[0]
sys.path.append(main_folder)