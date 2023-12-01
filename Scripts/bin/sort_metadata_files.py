#!/usr/bin/env python3

# Imports
import os
import os.path
import sys
import argparse
import pathlib

# Custom imports
lib_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "lib"))
sys.path.append(lib_folder)
import config
import command
import environment
import metadata
import setup

# Main
def main():

    # Check requirements
    setup.CheckRequirements()

    # Sort metadata files
    for game_category in metadata.GetMetadataCategories():
        for game_subcategory in metadata.GetMetadataSubcategories(game_category):

            # Sort gamelist file
            gamelist_file = metadata.DeriveMetadataFile(game_category, game_subcategory, config.metadata_format_gamelist)
            if os.path.isfile(gamelist_file):
                metadata_gamelist = metadata.Metadata()
                metadata_gamelist.import_from_gamelist_file(gamelist_file)
                metadata_gamelist.export_to_gamelist_file(gamelist_file)

            # Sort pegasus file
            pegasus_file = metadata.DeriveMetadataFile(game_category, game_subcategory, config.metadata_format_pegasus)
            if os.path.isfile(pegasus_file):
                metadata_pegasus = metadata.Metadata()
                metadata_pegasus.import_from_pegasus_file(pegasus_file)
                metadata_pegasus.export_to_pegasus_file(pegasus_file)

# Start
environment.RunAsRootIfNecessary(main)
