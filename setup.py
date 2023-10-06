from cx_Freeze import setup, Executable
import sys

base = None
if (sys.platform == "win32"):
    base = "Win32GUI" # Tells the build script to hide the console.
    
# ADD FILES
include_files = [
    (".dependencies/readme.txt", "dependencies/readme.txt")
    (".dependencies/7z2301-x64.exe", "dependencies/7z2301-x64.exe"),
    ("eenv", "eenv"),
    ("ekey.key", "ekey.key"),
    ('assets', 'assets')
]

# TARGET
target = Executable(script="SAM.py", base=base, icon="assets/SAM.ico")

# SETUP CX FREEZE
setup(
    name="Smart Assets Manager",
    version="1.0",
    description="SAM",
    author="George Boholteanu",
    options={"build_exe": {"packages": [], 'include_files': include_files}},
    executables=[target],
)
