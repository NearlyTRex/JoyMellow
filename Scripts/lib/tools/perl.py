# Imports
import os, os.path
import sys

# Local imports
import ini
import toolbase

# Perl tool
class Perl(toolbase.ToolBase):

    # Get name
    def GetName(self):
        return "Perl"

    # Get config
    def GetConfig(self):

        # Get git info
        perl_exe = ini.GetIniValue("Tools.Perl", "perl_exe")
        perl_install_dir = ini.GetIniPathValue("Tools.Perl", "perl_install_dir")

        # Return config
        return {

            # Perl
            "Perl": {
                "program": os.path.join(perl_install_dir, perl_exe)
            }
        }
