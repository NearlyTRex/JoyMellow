# Imports
import os
import os.path
import sys

# Custom imports
lib_folder = os.path.realpath(os.path.dirname(__file__))
sys.path.append(lib_folder)
import config
import command
import programs
import system
import environment
import iso
import archive
import sandbox

# Check if disc chd is mounted
def IsDiscCHDMounted(chd_file, mount_dir):
    return (
        os.path.isfile(chd_file) and
        os.path.isdir(mount_dir) and
        not system.IsDirectoryEmpty(mount_dir)
    )

# Create disc chd
def CreateDiscCHD(chd_file, source_iso, delete_original = False, verbose = False, exit_on_failure = False):

    # Get prefix
    prefix_dir = programs.GetProgramPrefixDir("MameToolsChdman")
    prefix_name = programs.GetProgramPrefixName("MameToolsChdman")

    # Get tool
    chd_tool = None
    if command.IsRunnableCommand(config.default_mame_chdman_exe, config.default_mame_chdman_install_dirs):
        chd_tool = command.GetRunnableCommandPath(config.default_mame_chdman_exe, config.default_mame_chdman_install_dirs)
    elif programs.IsToolInstalled("MameToolsChdman"):
        chd_tool = programs.GetToolProgram("MameToolsChdman")
    if not chd_tool:
        return False

    # Get create command
    create_command = [
        chd_tool,
        "createcd",
        "-i", source_iso,
        "-o", chd_file
    ]

    # Run create command
    command.RunBlockingCommand(
        cmd = create_command,
        options = command.CommandOptions(
            prefix_dir = prefix_dir,
            prefix_name = prefix_name,
            is_wine_prefix = sandbox.ShouldBeRunViaWine(chd_tool),
            is_sandboxie_prefix = sandbox.ShouldBeRunViaSandboxie(chd_tool),
            output_paths = [chd_file],
            blocking_processes = [chd_tool]),
        verbose = verbose,
        exit_on_failure = exit_on_failure)

    # Clean up
    if delete_original:
        system.RemoveFile(source_iso)

    # Check result
    return os.path.exists(chd_file)

# Extract disc chd
def ExtractDiscCHD(chd_file, binary_file, toc_file, delete_original = False, verbose = False, exit_on_failure = False):

    # Get prefix
    prefix_dir = programs.GetProgramPrefixDir("MameToolsChdman")
    prefix_name = programs.GetProgramPrefixName("MameToolsChdman")

    # Get tool
    chd_tool = None
    if command.IsRunnableCommand(config.default_mame_chdman_exe, config.default_mame_chdman_install_dirs):
        chd_tool = command.GetRunnableCommandPath(config.default_mame_chdman_exe, config.default_mame_chdman_install_dirs)
    elif programs.IsToolInstalled("MameToolsChdman"):
        chd_tool = programs.GetToolProgram("MameToolsChdman")
    if not chd_tool:
        return False

    # Get extract command
    extract_cmd = [
        chd_tool,
        "extractcd",
        "-i", chd_file,
        "-o", toc_file,
        "-ob", binary_file
    ]

    # Run extract command
    command.RunBlockingCommand(
        cmd = extract_cmd,
        options = command.CommandOptions(
            prefix_dir = prefix_dir,
            prefix_name = prefix_name,
            is_wine_prefix = sandbox.ShouldBeRunViaWine(chd_tool),
            is_sandboxie_prefix = sandbox.ShouldBeRunViaSandboxie(chd_tool),
            output_paths = [toc_file, binary_file],
            blocking_processes = [chd_tool]),
        verbose = verbose,
        exit_on_failure = exit_on_failure)

    # Clean up
    if delete_original:
        system.RemoveFile(chd_file)

    # Check result
    return os.path.exists(binary_file)

# Archive disc chd
def ArchiveDiscCHD(chd_file, zip_file, disc_type = None, delete_original = False, verbose = False, exit_on_failure = False):

    # Create temporary directory
    tmp_dir_success, tmp_dir_result = system.CreateTemporaryDirectory(verbose = verbose)
    if not tmp_dir_success:
        return False

    # Mount chd
    success = MountDiscCHD(
        chd_file = chd_file,
        mount_dir = tmp_dir_result,
        disc_type = disc_type,
        verbose = verbose,
        exit_on_failure = exit_on_failure)
    if not success:
        return False

    # Archive contents
    success = archive.CreateZipFromFolder(
        zip_file = zip_file,
        source_dir = tmp_dir_result,
        verbose = verbose,
        exit_on_failure = exit_on_failure)
    if not success:
        return False

    # Clean up
    if delete_original:
        system.RemoveFile(chd_file, verbose = verbose)
    system.RemoveDirectory(tmp_dir_result, verbose = verbose)

    # Check result
    return os.path.exists(zip_file)

# Verify disc chd
def VerifyDiscCHD(chd_file, verbose = False, exit_on_failure = False):

    # Get tool
    chd_tool = None
    if command.IsRunnableCommand(config.default_mame_chdman_exe, config.default_mame_chdman_install_dirs):
        chd_tool = command.GetRunnableCommandPath(config.default_mame_chdman_exe, config.default_mame_chdman_install_dirs)
    elif programs.IsToolInstalled("MameToolsChdman"):
        chd_tool = programs.GetToolProgram("MameToolsChdman")
    if not chd_tool:
        return False

    # Get verify command
    verify_cmd = [
        chd_tool,
        "verify",
        "-i", chd_file
    ]

    # Run verify command
    verify_output = command.RunOutputCommand(
        cmd = verify_cmd,
        verbose = verbose,
        exit_on_failure = exit_on_failure)

    # Check verification output
    if "Overall SHA1 verification successful!" in verify_output.decode():
        return True
    return False

# Mount disc chd
def MountDiscCHD(chd_file, mount_dir, disc_type = None, verbose = False, exit_on_failure = False):

    # Check if mounted
    if IsDiscCHDMounted(chd_file, mount_dir):
        return True

    # Create temporary directory
    tmp_dir_success, tmp_dir_result = system.CreateTemporaryDirectory(verbose = verbose)
    if not tmp_dir_success:
        return False

    # Get temporary files
    temp_iso_file = os.path.join(tmp_dir_result, system.GetFilenameBasename(chd_file) + ".iso")
    temp_toc_file = os.path.join(tmp_dir_result, system.GetFilenameBasename(chd_file) + ".toc")

    # Extract iso from chd
    success = ExtractDiscCHD(
        chd_file = chd_file,
        binary_file = temp_iso_file,
        toc_file = temp_toc_file,
        verbose = verbose,
        exit_on_failure = exit_on_failure)
    if not success:
        return False

    # Make mount directories
    system.MakeDirectory(mount_dir, verbose = verbose, exit_on_failure = exit_on_failure)

    # Extract iso files to mount point
    if disc_type == config.disc_type_macwin:
        success = archive.ExtractArchive(
            archive_file = temp_iso_file,
            extract_dir = mount_dir,
            delete_original = True,
            verbose = verbose,
            exit_on_failure = exit_on_failure)
    else:
        success = iso.ExtractISO(
            iso_file = temp_iso_file,
            extract_dir = mount_dir,
            delete_original = True,
            verbose = verbose,
            exit_on_failure = exit_on_failure)
        if not success:
            return False

    # Delete temporary directory
    system.RemoveDirectory(tmp_dir_result, verbose = verbose)

    # Check result
    return IsDiscCHDMounted(chd_file, mount_dir)

# Unmount disc chd
def UnmountDiscCHD(chd_file, mount_dir, verbose = False, exit_on_failure = False):

    # Check if mounted
    if not IsDiscCHDMounted(chd_file, mount_dir):
        return True

    # Remove mount point
    system.RemoveDirectory(
        dir = mount_dir,
        verbose = verbose,
        exit_on_failure = exit_on_failure)

    # Check result
    return not IsDiscCHDMounted(chd_file, mount_dir)
