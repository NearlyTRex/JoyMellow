# Imports
import os
import os.path
import sys

# Local imports
import config
import environment
import system
import network
import programs
import gui
import emulatorcommon
import emulatorbase

# Config files
config_files = {}
config_files["Xenia/windows/portable.txt"] = ""
config_files["Xenia/windows/xenia.config.toml"] = """
[Storage]
content_root = "$GAME_SAVE_DIR"
"""

# Xenia emulator
class Xenia(emulatorbase.EmulatorBase):

    # Get name
    def GetName(self):
        return "Xenia"

    # Get platforms
    def GetPlatforms(self):
        return [
            config.game_subcategory_microsoft_xbox_360,
            config.game_subcategory_microsoft_xbox_360_god,
            config.game_subcategory_microsoft_xbox_360_xbla,
            config.game_subcategory_microsoft_xbox_360_xig
        ]

    # Get config
    def GetConfig(self):
        return {
            "Xenia": {
                "program": {
                    "windows": "Xenia/windows/xenia.exe",
                    "linux": "Xenia/windows/xenia.exe"
                },
                "save_dir": {
                    "windows": "Xenia/windows/content",
                    "linux": "Xenia/windows/content"
                },
                "config_file": {
                    "windows": "Xenia/windows/xenia.config.toml",
                    "linux": "Xenia/windows/xenia.config.toml"
                },
                "run_sandboxed": {
                    "windows": False,
                    "linux": True
                }
            }
        }

    # Download
    def Download(self, force_downloads = False, verbose = False, exit_on_failure = False):
        if force_downloads or programs.ShouldProgramBeInstalled("Xenia", "windows"):
            network.DownloadLatestGithubRelease(
                github_user = "xenia-project",
                github_repo = "release-builds-windows",
                starts_with = "xenia_master",
                ends_with = "master.zip",
                search_file = "xenia.exe",
                install_name = "Xenia",
                install_dir = programs.GetProgramInstallDir("Xenia", "windows"),
                get_latest = True,
                verbose = verbose,
                exit_on_failure = exit_on_failure)

    # Setup
    def Setup(self, verbose = False, exit_on_failure = False):

        # Create config files
        for config_filename, config_contents in config_files.items():
            system.TouchFile(
                src = os.path.join(environment.GetEmulatorsRootDir(), config_filename),
                contents = config_contents.strip(),
                verbose = verbose,
                exit_on_failure = exit_on_failure)

    # Launch
    def Launch(
        self,
        json_data,
        capture_type,
        fullscreen = False,
        verbose = False,
        exit_on_failure = False):

        # Get launch command
        launch_cmd = [
            programs.GetEmulatorProgram("Xenia"),
            config.token_game_file
        ]
        if fullscreen:
            launch_cmd += [
                "--fullscreen=true"
            ]

        # Launch game
        emulatorcommon.SimpleLaunch(
            json_data = json_data,
            launch_cmd = launch_cmd,
            capture_type = capture_type,
            verbose = verbose,
            exit_on_failure = exit_on_failure)
