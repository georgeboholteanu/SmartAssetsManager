import sys
from cx_Freeze import setup, Executable
from dotenv import load_dotenv
load_dotenv()

# ADD FILES
include_files = [("C:/Program Files/WinRAR/Rar.exe", "C:/Program Files (x86)/UnrarDLL/x64/UnRAR64.dll", "assets", ".env")]

base = None

if sys.platform == "win32":
    base = "Win32GUI"  # Use "Win32GUI" to create a GUI application on Windows

# TARGET
target = Executable(
    script="SAM.py",
    base="Win32GUI",
    icon="assets/SAM.ico"
)

# SETUP CX FREEZE
setup(
    name = "Smart Assets Manager",
    version = "1.0",
    description = "SAM",
    author = "George Boholteanu",
    options = {'build.exe': {'include_files' : include_files}},
    executables = [target]
)
