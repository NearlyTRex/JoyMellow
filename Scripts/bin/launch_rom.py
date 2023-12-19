#!/usr/bin/env python3

# Imports
import os, os.path
import sys
import argparse

# Custom imports
lib_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib"))
sys.path.append(lib_folder)
import config
import environment
import launcher
import cache
import setup
import gameinfo
import gui
import ini

# Setup argument parser
parser = argparse.ArgumentParser(description="Launch json file.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("path", help="Json path to launch")
parser.add_argument("-f", "--force_cache_refresh", action="store_true", help="Force refresh of cached files")
parser.add_argument("-c", "--capture_type",
    choices=[
        config.capture_type_none,
        config.capture_type_screenshot,
        config.capture_type_video,
    ],
    default=config.capture_type_none, help="Capture type"
)

# Parse arguments
args, unknownargs = parser.parse_known_args()
if not args.rom:
    parser.print_help()
    sys.exit(1)

# Main
def main():

    # Check requirements
    setup.CheckRequirements()

    # Get flags
    verbose = ini.GetIniBoolValue("UserData.Flags", "verbose")
    exit_on_failure = ini.GetIniBoolValue("UserData.Flags", "exit_on_failure")
    fullscreen = ini.GetIniBoolValue("UserData.Flags", "fullscreen")

    # Get json file
    json_file = args.path
    if not os.path.isfile(json_file):
        json_file = os.path.join(environment.GetJsonRomsMetadataRootDir(), json_file)
    if not os.path.isfile(json_file):
        gui.DisplayErrorPopup(
            title_text = "Json file not found",
            message_text = "Json file %s was not found" % json_file)

    # Get json info
    json_data = gameinfo.ParseGameJson(json_file, verbose = verbose, exit_on_failure = exit_on_failure)
    json_base_name = json_data[config.json_key_base_name]
    json_platform = json_data[config.json_key_platform]

    # Force cache refresh
    if args.force_cache_refresh:
        cache.RemoveGameFromCache(
            game_platform = json_platform,
            game_name = json_base_name,
            game_file = json_file,
            verbose = verbose,
            exit_on_failure = exit_on_failure)

    # Launch game
    launcher.LaunchGame(
        game_platform = json_platform,
        game_file = json_file,
        capture_type = args.capture_type,
        fullscreen = fullscreen,
        verbose = verbose,
        exit_on_failure = exit_on_failure)

# Start
main()
