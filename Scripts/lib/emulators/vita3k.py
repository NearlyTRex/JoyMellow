# Imports
import os
import os.path
import sys

# Custom imports
lib_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(lib_folder)
import config
import environment
import system
import network
import programs
import launchcommon
import gui

# Local imports
from . import base

# Config files
config_files = {}
config_files["Vita3K/windows/config.yml"] = """
---
pref-path: $EMULATOR_MAIN_ROOT/Vita3K/windows/data
...
"""
config_files["Vita3K/linux/Vita3K.AppImage.home/.config/Vita3K/config.yml"] = """
---
pref-path: $EMULATOR_MAIN_ROOT/Vita3K/linux/Vita3K.AppImage.home/.local/share/Vita3K/Vita3K/
...
"""

# Vita3K emulator
class Vita3K(base.EmulatorBase):

    # Get name
    def GetName(self):
        return "Vita3K"

    # Get platforms
    def GetPlatforms(self):
        return config.vita3k_platforms

    # Get config
    def GetConfig(self):
        return {
            "Vita3K": {
                "program": {
                    "windows": "Vita3K/windows/Vita3K.exe",
                    "linux": "Vita3K/linux/Vita3K.AppImage"
                },
                "save_dir": {
                    "windows": "Vita3K/windows/data/ux0/user",
                    "linux": "Vita3K/linux/Vita3K.AppImage.home/.local/share/Vita3K/Vita3K/ux0/user"
                },
                "app_dir": {
                    "windows": "Vita3K/windows/data/ux0/app",
                    "linux": "Vita3K/linux/Vita3K.AppImage.home/.local/share/Vita3K/Vita3K/ux0/app"
                },
                "setup_dir": {
                    "windows": "Vita3K/windows/data",
                    "linux": "Vita3K/linux/Vita3K.AppImage.home/.local/share/Vita3K/Vita3K"
                },
                "config_file": {
                    "windows": "Vita3K/windows/config.yml",
                    "linux": "Vita3K/linux/Vita3K.AppImage.home/.config/Vita3K/config.yml"
                },
                "run_sandboxed": {
                    "windows": False,
                    "linux": False
                }
            }
        }

    # Download
    def Download(self, force_downloads = False):
        if force_downloads or programs.ShouldProgramBeInstalled("Vita3K", "windows"):
            network.DownloadLatestGithubRelease(
                github_user = "Vita3K",
                github_repo = "Vita3K",
                starts_with = "windows-latest",
                ends_with = ".zip",
                search_file = "Vita3K.exe",
                install_name = "Vita3K",
                install_dir = programs.GetProgramInstallDir("Vita3K", "windows"),
                get_latest = True,
                verbose = config.default_flag_verbose,
                exit_on_failure = config.default_flag_exit_on_failure)
        if force_downloads or programs.ShouldProgramBeInstalled("Vita3K", "linux"):
            network.DownloadLatestGithubRelease(
                github_user = "Vita3K",
                github_repo = "Vita3K",
                starts_with = "Vita3K-x86_64",
                ends_with = ".AppImage",
                search_file = "Vita3K-x86_64.AppImage",
                install_name = "Vita3K",
                install_dir = programs.GetProgramInstallDir("Vita3K", "linux"),
                get_latest = True,
                verbose = config.default_flag_verbose,
                exit_on_failure = config.default_flag_exit_on_failure)

    # Setup
    def Setup(self):
        for obj in ["os0", "sa0", "vs0"]:
            if not os.path.exists(os.path.join(programs.GetEmulatorPathConfigValue("Vita3K", "setup_dir", "linux"), obj)):
                archive.ExtractArchive(
                    archive_file = os.path.join(environment.GetSyncedGameEmulatorSetupDir("Vita3K"), obj + ".zip"),
                    extract_dir = os.path.join(programs.GetEmulatorPathConfigValue("Vita3K", "setup_dir", "linux"), obj),
                    skip_existing = True,
                    verbose = config.default_flag_verbose,
                    exit_on_failure = config.default_flag_exit_on_failure)
            if not os.path.exists(os.path.join(programs.GetEmulatorPathConfigValue("Vita3K", "setup_dir", "windows"), obj)):
                archive.ExtractArchive(
                    archive_file = os.path.join(environment.GetSyncedGameEmulatorSetupDir("Vita3K"), obj + ".zip"),
                    extract_dir = os.path.join(programs.GetEmulatorPathConfigValue("Vita3K", "setup_dir", "windows"), obj),
                    skip_existing = True,
                    verbose = False,
                    exit_on_failure = False)

    # Launch
    def Launch(
        self,
        launch_name,
        launch_platform,
        launch_file,
        launch_artwork,
        launch_save_dir,
        launch_general_save_dir,
        launch_capture_type):

        # Get launch command
        launch_cmd = [
            programs.GetEmulatorProgram("Vita3K")
        ]

        # Launch game
        launchcommon.SimpleLaunch(
            launch_cmd = launch_cmd,
            launch_name = launch_name,
            launch_platform = launch_platform,
            launch_file = launch_file,
            launch_artwork = launch_artwork,
            launch_save_dir = launch_save_dir,
            launch_capture_type = launch_capture_type)
