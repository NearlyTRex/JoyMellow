# Imports
import os, os.path
import sys

# Base tool
class ToolBase:

    # Get name
    def GetName(self):
        return ""

    # Get config
    def GetConfig(self):
        return {}

    # Download
    def Download(self, force_downloads = False, verbose = False, exit_on_failure = False):
        pass

    # Setup
    def Setup(self, verbose = False, exit_on_failure = False):
        pass
