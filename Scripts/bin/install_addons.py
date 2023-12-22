#!/usr/bin/env python3

# Imports
import os, os.path
import sys
import argparse

# Custom imports
lib_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib"))
sys.path.append(lib_folder)
import config
import gameinfo
import addons
import setup
import ini

# Parse arguments
parser = argparse.ArgumentParser(description="Install addons.")
parser.add_argument("path", help="Input path")
args, unknown = parser.parse_known_args()
if not args.path:
    parser.print_help()
    sys.exit(-1)

# Main
def main():

    # Check requirements
    setup.CheckRequirements()

    # Get flags
    verbose = ini.GetIniBoolValue("UserData.Flags", "verbose")
    exit_on_failure = ini.GetIniBoolValue("UserData.Flags", "exit_on_failure")

    # Get json file
    json_files = [args.path]
    if os.path.isdir(args.path):
        json_files = system.BuildFileListByExtensions(args.path, extensions = [".json"])

    # Install addons
    for json_file in json_files:

        # Get game info
        game_info = gameinfo.GameInfo(
            json_file = json_file,
            verbose = verbose,
            exit_on_failure = exit_on_failure)

        # Install addons
        addon.InstallAddons(
            game_info = game_info,
            verbose = verbose,
            exit_on_failure = exit_on_failure)

# Start
main()
