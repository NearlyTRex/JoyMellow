# Imports
import os
import sys
import subprocess

# Local imports
import environment

###########################################################
# Packages
###########################################################
packages = [
    "pip",
    "wheel",
    "psutil",
    "selenium",
    "requests",
    "pathlib",
    "PySimpleGUI",
    "Pillow",
    "bs4",
    "lxml",
    "mergedeep",
    "fuzzywuzzy",
    "dictdiffer",
    "termcolor",
    "colorama",
    "pycryptodome",
    "pycryptodomex",
    "cryptography",
    "aenum",
    "fastxor",
    "packaging",
    "ecdsa",
    "schedule",
    "python-dateutil",
    "xxhash",
    "screeninfo",
    "tqdm",
    "GitPython",
    "PyGithub"
]
if environment.IsWindowsPlatform():
    packages += [
        "pywin32",
        "pyuac"
    ]

###########################################################
# Functions
###########################################################

# Setup
def Setup(ini_values = {}):

    # Get python tools
    python_exe = ini_values["Tools.Python"]["python_exe"]
    python_pip_exe = ini_values["Tools.Python"]["python_pip_exe"]
    python_install_dir = os.path.expandvars(ini_values["Tools.Python"]["python_install_dir"])
    python_tool = os.path.join(python_install_dir, python_exe)
    python_venv_dir = os.path.expandvars(ini_values["Tools.Python"]["python_venv_dir"])
    python_venv_pip_tool = os.path.join(python_venv_dir, "bin", python_pip_exe)
    if environment.IsWindowsPlatform():
        python_venv_pip_tool = os.path.join(python_venv_dir, "Scripts", python_pip_exe)

    # Create python virtual environment
    subprocess.run([python_tool, "-m", "venv", python_venv_dir])

    # Install python packages
    for package in packages:
        subprocess.run([python_venv_pip_tool, "install", "--upgrade", package])

# Run script
def RunScript(script_path, ini_values = {}):

    # Get python tools
    python_exe = ini_values["Tools.Python"]["python_exe"]
    python_venv_dir = os.path.expandvars(ini_values["Tools.Python"]["python_venv_dir"])
    python_venv_python_tool = os.path.join(python_venv_dir, "bin", python_exe)
    if environment.IsWindowsPlatform():
        python_venv_python_tool = os.path.join(python_venv_dir, "Scripts", python_exe)

    # Run python script
    subprocess.run([python_venv_python_tool, script_path])
