# Imports
import os, os.path
import sys

# Custom imports
lib_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(lib_folder)
import config
import network
import programs

# Local imports
from . import base

# ExtractXIso tool
class ExtractXIso(base.ToolBase):

    # Get name
    def GetName():
        return "ExtractXIso"

    # Get config
    def GetConfig():
        return {
            "ExtractXIso": {
                "program": {
                    "windows": "ExtractXIso/windows/extract-xiso.exe",
                    "linux": "ExtractXIso/linux/ExtractXIso.AppImage"
                },
                "run_sandboxed": {
                    "windows": False,
                    "linux": False
                }
            }
        }

    # Download
    def Download(force_downloads = False):
        if force_downloads or programs.ShouldProgramBeInstalled("ExtractXIso", "windows"):
            network.DownloadLatestGithubRelease(
                github_user = "XboxDev",
                github_repo = "extract-xiso",
                starts_with = "extract-xiso",
                ends_with = "win32-release.zip",
                search_file = "extract-xiso.exe",
                install_name = "ExtractXIso",
                install_dir = programs.GetProgramInstallDir("ExtractXIso", "windows"),
                install_files = ["extract-xiso.exe"],
                verbose = config.default_flag_verbose,
                exit_on_failure = config.default_flag_exit_on_failure)
        if force_downloads or programs.ShouldProgramBeInstalled("ExtractXIso", "linux"):
            network.BuildAppImageFromSource(
                release_url = "https://github.com/NearlyTRex/ExtractXIso.git",
                output_name = "ExtractXIso",
                output_dir = programs.GetProgramInstallDir("ExtractXIso", "linux"),
                build_cmd = [
                    "cmake", "..",
                    "&&",
                    "make"
                ],
                build_dir = "Build",
                internal_copies = [
                    {"from": "Source/Build/extract-xiso", "to": "AppImage/usr/bin/extract-xiso"},
                    {"from": "AppImageTool/linux/app.desktop", "to": "AppImage/app.desktop"},
                    {"from": "AppImageTool/linux/icon.png", "to": "AppImage/icon.png"}
                ],
                internal_symlinks = [
                    {"from": "usr/bin/extract-xiso", "to": "AppRun"}
                ],
                verbose = config.default_flag_verbose,
                exit_on_failure = config.default_flag_exit_on_failure)