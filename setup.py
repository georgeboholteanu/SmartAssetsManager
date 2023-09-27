import sys
import os
from cx_Freeze import setup, Executable
from dotenv import load_dotenv
load_dotenv()

# ADD FILES
files = ["C:/Program Files/WinRAR/Rar.exe", "C:/Program Files (x86)/UnrarDLL/x64/UnRAR64.dll"]

# TARGET
target = Executable(
    script="SAM.py",
    base="Win32GUI",
    icon=f"{os.getenv('proj_path')}" + "/assets/SAM.ico"
)

# SETUP CX FREEZE
setup(
    name = "Smart Assets Manager",
    version = "1.0",
    description = "SAM",
    author = "George Boholteanu",
    options = {'build.exe': {'include_files' : files}},
    executables = [target]
)
