# Imports
import os, os.path
import sys

# Local imports
import config
import command
import archive
import programs
import system
import ini
import storebase

# Epic store
class Epic(storebase.StoreBase):

    # Constructor
    def __init__(self):
        super().__init__()

        # Get user details
        self.username = ini.GetIniValue("UserData.Epic", "epic_username")
        if not self.username:
            raise RuntimeError("Ini file does not have a valid epic user details")

        # Get install dir
        self.install_dir = ini.GetIniPathValue("UserData.Epic", "epic_install_dir")
        if not system.IsPathValid(self.install_dir) or not system.DoesPathExist(self.install_dir):
            raise RuntimeError("Ini file does not have a valid epic install dir")

    # Get name
    def GetName(self):
        return "Epic"

    # Get platform
    def GetPlatform(self):
        return config.platform_computer_epic_games

    # Get category
    def GetCategory(self):
        return config.game_category_computer

    # Get subcategory
    def GetSubcategory(self):
        return config.game_subcategory_epic_games

    # Get key
    def GetKey(self):
        return config.json_key_epic

    # Get user name
    def GetUserName(self):
        return self.username

    # Get install dir
    def GetInstallDir(self):
        return self.install_dir

    ############################################################

    # Login
    def Login(
        self,
        verbose = False,
        exit_on_failure = False):

        # Get tool
        python_tool = None
        if programs.IsToolInstalled("PythonVenvPython"):
            python_tool = programs.GetToolProgram("PythonVenvPython")
        if not python_tool:
            system.LogError("PythonVenvPython was not found")
            return False

        # Get script
        legendary_script = None
        if programs.IsToolInstalled("Legendary"):
            legendary_script = programs.GetToolProgram("Legendary")
        if not legendary_script:
            system.LogError("Legendary was not found")
            return False

        # Get login command
        login_cmd = [
            python_tool,
            legendary_script,
            "auth"
        ]

        # Run login command
        code = command.RunBlockingCommand(
            cmd = login_cmd,
            verbose = verbose,
            exit_on_failure = exit_on_failure)
        return (code == 0)

    ############################################################

    # Get purchases
    def GetPurchases(
        self,
        verbose = False,
        exit_on_failure = False):
        return []

    ############################################################

    # Get info
    def GetLatestInfo(
        self,
        identifier,
        branch = None,
        verbose = False,
        exit_on_failure = False):

        # Get tool
        python_tool = None
        if programs.IsToolInstalled("PythonVenvPython"):
            python_tool = programs.GetToolProgram("PythonVenvPython")
        if not python_tool:
            system.LogError("PythonVenvPython was not found")
            return False

        # Get script
        legendary_script = None
        if programs.IsToolInstalled("Legendary"):
            legendary_script = programs.GetToolProgram("Legendary")
        if not legendary_script:
            system.LogError("Legendary was not found")
            return False

        # Get info command
        info_cmd = [
            python_tool,
            legendary_script,
            "info", identifier
        ]

        # Run info command
        info_output = command.RunOutputCommand(
            cmd = info_cmd,
            verbose = verbose,
            exit_on_failure = exit_on_failure)
        if len(info_output) == 0 or "No game information available" in info_output:
            system.LogError("Unable to find epic information for '%s'" % identifier)
            return None

        # Build game info
        game_info = {}
        game_info[config.json_key_store_appname] = identifier
        for line in info_output.split("\n"):
            if line.startswith("- Title:"):
                game_info[config.json_key_store_name] = line.replace("- Title:", "").strip()
            elif line.startswith("- Latest version:"):
                game_info[config.json_key_store_buildid] = line.replace("- Latest version:", "").strip()
            elif line.startswith("- Cloud save folder (Windows):"):
                line_path = line.replace("- Cloud save folder (Windows):", "").strip()
                if "(None)" not in line_path:
                    base_path = None
                    if config.json_key_store_installdir in game_info:
                        base_path = game_info[config.json_key_store_installdir]
                    game_info[config.json_key_store_paths] = [
                        storebase.TranslateStorePath(line_path, base_path)
                    ]

        # Return game info
        return game_info

    ############################################################

    # Get identifier
    def GetIdentifier(self, game_info, identifier_type):
        return game_info.get_store_appname(self.GetKey())

    ############################################################

    # Get game save paths
    def GetGameSavePaths(
        self,
        game_info,
        verbose = False,
        exit_on_failure = False):
        return []

    ############################################################

    # Install by identifier
    def InstallByIdentifier(
        self,
        identifier,
        verbose = False,
        exit_on_failure = False):
        return False

    ############################################################

    # Launch by identifier
    def LaunchByIdentifier(
        self,
        identifier,
        verbose = False,
        exit_on_failure = False):
        return False

    ############################################################

    # Download by identifier
    def DownloadByIdentifier(
        self,
        identifier,
        output_dir,
        output_name = None,
        branch = None,
        clean_output = False,
        verbose = False,
        exit_on_failure = False):
        return False

    ############################################################
