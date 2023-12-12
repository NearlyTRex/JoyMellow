# Imports
import os, os.path
import sys

# Custom imports
lib_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(lib_folder)
import config
import environment
import system
import network
import programs
import nintendo
import launchcommon
import gui

# Local imports
from . import base

# Config files
config_files = {}
config_files["Cemu/windows/settings.xml"] = ""
config_files["Cemu/windows/keys.txt"] = ""
config_files["Cemu/linux/Cemu.AppImage.home/.config/Cemu/settings.xml"] = ""
config_files["Cemu/linux/Cemu.AppImage.home/.local/share/Cemu/keys.txt"] = ""

# Cemu emulator
class Cemu(base.EmulatorBase):

    # Get name
    def GetName(self):
        return "Cemu"

    # Get platforms
    def GetPlatforms(self):
        return [
            "Nintendo Wii U",
            "Nintendo Wii U eShop"
        ]

    # Get config
    def GetConfig(self):
        return {
            "Cemu": {
                "program": {
                    "windows": "Cemu/windows/Cemu.exe",
                    "linux": "Cemu/linux/Cemu.AppImage"
                },
                "save_dir": {
                    "windows": "Cemu/windows/mlc01/usr/save/00050000",
                    "linux": "Cemu/linux/Cemu.AppImage.home/.local/share/Cemu/mlc01/usr/save/00050000"
                },
                "setup_dir": {
                    "windows": "Cemu/windows",
                    "linux": "Cemu/linux/Cemu.AppImage.home/.local/share/Cemu"
                },
                "config_file": {
                    "windows": "Cemu/windows/settings.xml",
                    "linux": "Cemu/linux/Cemu.AppImage.home/.config/Cemu/settings.xml"
                },
                "keys_file": {
                    "windows": "Cemu/windows/keys.txt",
                    "linux": "Cemu/linux/Cemu.AppImage.home/.local/share/Cemu/keys.txt"
                },
                "run_sandboxed": {
                    "windows": False,
                    "linux": False
                }
            }
        }

    # Install add-ons
    def InstallAddons(self, dlc_dirs = [], update_dirs = [], verbose = False, exit_on_failure = False):
        for package_dirset in [dlc_dirs, update_dirs]:
            for package_dir in package_dirset:
                for tik_file in system.BuildFileListByExtensions(package_dir, extensions = [".tik"]):
                    if tik_file.endswith("title.tik"):
                        tik_dir = system.GetFilenameDirectory(tik_file)
                        nintendo.InstallWiiUNusPackage(
                            nus_package_dir = tik_dir,
                            nand_dir = os.path.join(programs.GetEmulatorPathConfigValue("Cemu", "setup_dir"), "mlc01"),
                            verbose = verbose,
                            exit_on_failure = exit_on_failure)

    # Download
    def Download(self, force_downloads = False, verbose = False, exit_on_failure = False):
        if force_downloads or programs.ShouldProgramBeInstalled("Cemu", "windows"):
            network.DownloadLatestGithubRelease(
                github_user = "cemu-project",
                github_repo = "Cemu",
                starts_with = "cemu",
                ends_with = "windows-x64.zip",
                search_file = "Cemu.exe",
                install_name = "Cemu",
                install_dir = programs.GetProgramInstallDir("Cemu", "windows"),
                verbose = verbose,
                exit_on_failure = exit_on_failure)
        if force_downloads or programs.ShouldProgramBeInstalled("Cemu", "linux"):
            network.DownloadLatestGithubRelease(
                github_user = "cemu-project",
                github_repo = "Cemu",
                starts_with = "Cemu",
                ends_with = ".AppImage",
                search_file = "Cemu.AppImage",
                install_name = "Cemu",
                install_dir = programs.GetProgramInstallDir("Cemu", "linux"),
                verbose = verbose,
                exit_on_failure = exit_on_failure)

    # Setup
    def Setup(self, verbose = False, exit_on_failure = False):

        # Create config files
        for config_filename, config_contents in config_files.items():
            system.TouchFile(
                src = os.path.join(environment.GetEmulatorsRootDir(), config_filename),
                contents = config_contents,
                verbose = verbose,
                exit_on_failure = exit_on_failure)

    # Launch
    def Launch(
        self,
        launch_name,
        launch_platform,
        launch_file,
        launch_artwork,
        launch_save_dir,
        launch_general_save_dir,
        launch_capture_type,
        fullscreen = False,
        verbose = False,
        exit_on_failure = False):

        # Get launch categories
        launch_supercategory, launch_category, launch_subcategory = metadata.DeriveMetadataCategoriesFromPlatform(launch_platform)

        # Install game to cache
        cache.InstallGameToCache(
            game_platform = launch_platform,
            game_name = launch_name,
            game_file = launch_file,
            game_artwork = launch_artwork,
            verbose = verbose,
            exit_on_failure = exit_on_failure)

        # Get directories
        cache_dir = environment.GetCachedRomDir(launch_category, launch_subcategory, launch_name)

        # Update keys
        for key_file in system.BuildFileListByExtensions(cache_dir, extensions = [".txt"]):
            if key_file.endswith(".key.txt"):
                for platform in ["windows", "linux"]:
                    nintendo.UpdateWiiUKeys(
                        src_key_file = key_file,
                        dest_key_file = programs.GetEmulatorPathConfigValue("Cemu", "keys_file", platform),
                        verbose = verbose,
                        exit_on_failure = exit_on_failure)

        # Get launch command
        launch_cmd = [
            programs.GetEmulatorProgram("Cemu"),
            "-g", config.token_game_file
        ]
        if fullscreen:
            launch_cmd += [
                "-f"
            ]

        # Launch game
        launchcommon.SimpleLaunch(
            launch_cmd = launch_cmd,
            launch_name = launch_name,
            launch_platform = launch_platform,
            launch_file = launch_file,
            launch_artwork = launch_artwork,
            launch_save_dir = launch_save_dir,
            launch_capture_type = launch_capture_type,
            verbose = verbose,
            exit_on_failure = exit_on_failure)
