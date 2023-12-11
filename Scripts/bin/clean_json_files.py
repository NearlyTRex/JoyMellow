#!/usr/bin/env python3

# Imports
import os, os.path
import sys
import json
import argparse

# Custom imports
lib_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib"))
sys.path.append(lib_folder)
import config
import environment
import metadata
import transform
import system
import setup

# Parse arguments
parser = argparse.ArgumentParser(description="Clean json files.")
args, unknown = parser.parse_known_args()

# Main
def main():

    # Check requirements
    setup.CheckRequirements()

    # Clean json files
    for game_category in metadata.GetMetadataCategories():
        for game_subcategory in sorted(metadata.GetMetadataSubcategories(game_category)):
            game_platform = metadata.DeriveMetadataPlatform(game_category, game_subcategory)
            for game_name in metadata.GetPossibleGameNames(environment.GetJsonRomsMetadataRootDir(), game_category, game_subcategory):

                # Get json file path
                json_file_path = environment.GetJsonRomMetadataFile(game_category, game_subcategory, game_name)

                # Clean json file
                system.CleanJsonFile(
                    src = json_file_path,
                    sort_keys = True,
                    remove_empty_values = True,
                    verbose = config.default_flag_verbose,
                    exit_on_failure = config.default_flag_exit_on_failure)

# Start
environment.RunAsRootIfNecessary(main)
