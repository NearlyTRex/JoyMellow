# Imports
import os, os.path
import sys

# Local imports
import config
import system
import environment
import platforms
import gameinfo
import install
import installer
import archive
import playlist
import iso
import chd
import playstation
import xbox

###########################################################

# Transform computer programs
def TransformComputerPrograms(
    game_info,
    source_file,
    output_dir,
    keep_setup_files = False,
    verbose = False,
    exit_on_failure = False):

    # Get game info
    game_name = game_info.get_name()
    game_category = game_info.get_category()
    game_subcategory = game_info.get_subcategory()

    # Get paths
    output_extract_dir = os.path.join(output_dir, gameinfo.DeriveRegularNameFromGameName(game_name))
    output_extract_index_file = os.path.join(output_extract_dir, config.raw_files_index)
    output_install_file = os.path.join(output_dir, game_name + ".install")
    cached_install_dir = environment.GetInstallRomDir(game_category, game_subcategory, game_name)
    cached_install_file = os.path.join(cached_install_dir, game_name + ".install")

    # Make directories
    system.MakeDirectory(output_dir, verbose = verbose, exit_on_failure = exit_on_failure)
    system.MakeDirectory(cached_install_dir, verbose = verbose, exit_on_failure = exit_on_failure)

    # Get pre-packaged archive
    prepackaged_archive = os.path.join(system.GetFilenameDirectory(source_file), game_name + ".7z.001")
    if not os.path.exists(prepackaged_archive):
        prepackaged_archive = os.path.join(system.GetFilenameDirectory(source_file), game_name + ".exe")

    # Pre-packaged archive
    if os.path.isfile(prepackaged_archive):

        # Extract file
        success = archive.ExtractArchive(
            archive_file = prepackaged_archive,
            extract_dir = output_extract_dir,
            verbose = verbose,
            exit_on_failure = exit_on_failure)
        if not success:
            return (False, "Unable to extract game")

    # Normal installer files
    else:

        # Check for existing install image
        if not os.path.exists(cached_install_file):

            # Create install image
            success = installer.InstallComputerGame(
                game_info = game_info,
                output_image = output_install_file,
                keep_setup_files = keep_setup_files,
                verbose = verbose,
                exit_on_failure = exit_on_failure)
            if not success:
                return (False, "Unable to install computer game")

            # Backup install image
            success = system.TransferFile(
                src = output_install_file,
                dest = cached_install_file,
                delete_afterwards = True,
                show_progress = True,
                verbose = verbose,
                exit_on_failure = exit_on_failure)
            if not success:
                return (False, "Unable to backup computer game install")

        # Unpack install image
        success = install.UnpackInstallImage(
            input_image = cached_install_file,
            output_dir = output_extract_dir,
            verbose = verbose,
            exit_on_failure = exit_on_failure)
        if not success:
            return (False, "Unable to unpack install image")

    # Touch index file
    success = system.TouchFile(
        src = output_extract_index_file,
        verbose = verbose,
        exit_on_failure = exit_on_failure)
    if not success:
        return (False, "Unable to create raw index")

    # Return output
    return (True, output_extract_index_file)

###########################################################

# Transform disc images
def TransformDiscImage(
    game_info,
    source_file,
    output_dir,
    verbose = False,
    exit_on_failure = False):

    # Make directories
    system.MakeDirectory(output_dir, verbose = verbose, exit_on_failure = exit_on_failure)

    # Get disc images
    disc_image_files = []
    if source_file.endswith(".chd"):
        disc_image_files = [system.GetFilenameFile(source_file)]
    if source_file.endswith(".m3u"):
        disc_image_files = playlist.ReadPlaylist(source_file, verbose = verbose, exit_on_failure = exit_on_failure)

    # Extract disc images
    for disc_image_file in disc_image_files:
        if disc_image_file.endswith(".chd"):
            success = chd.ExtractDiscCHD(
                chd_file = os.path.join(system.GetFilenameDirectory(source_file), disc_image_file),
                binary_file = os.path.join(output_dir, system.GetFilenameBasename(disc_image_file) + ".iso"),
                toc_file = os.path.join(output_dir, system.GetFilenameBasename(disc_image_file) + ".toc"),
                verbose = verbose,
                exit_on_failure = exit_on_failure)
            if not success:
                return (False, "Unable to extract disc images")

    # Write playlist
    if source_file.endswith(".m3u"):
        playlist_contents = []
        for disc_image_file in disc_image_files:
            playlist_contents += [disc_image_file.replace(".chd", ".iso")]
        success = playlist.WritePlaylist(
            output_file = os.path.join(output_dir, system.GetFilenameBasename(source_file) + ".m3u"),
            playlist_contents = playlist_contents,
            verbose = verbose,
            exit_on_failure = exit_on_failure)
        if not success:
            return (False, "Unable to write playlist")

    # Return output
    if source_file.endswith(".chd"):
        return (True, os.path.join(output_dir, system.GetFilenameBasename(source_file) + ".iso"))
    elif source_file.endswith(".m3u"):
        return (True, os.path.join(output_dir, system.GetFilenameBasename(source_file) + ".m3u"))

    # No transformation was done
    return (False, source_file)

###########################################################

# Transform Xbox disc image
def TransformXboxDiscImage(
    game_info,
    source_file,
    output_dir,
    verbose = False,
    exit_on_failure = False):

    # Make directories
    system.MakeDirectory(output_dir, verbose = verbose, exit_on_failure = exit_on_failure)

    # Get disc images
    disc_image_files = []
    if source_file.endswith(".iso"):
        disc_image_files = [system.GetFilenameFile(source_file)]
    if source_file.endswith(".m3u"):
        disc_image_files = playlist.ReadPlaylist(source_file, verbose = verbose, exit_on_failure = exit_on_failure)

    # Rewrite xbox disc images
    for disc_image_file in disc_image_files:
        if disc_image_file.endswith(".iso"):
            success = xbox.RewriteXboxISO(
                iso_file = os.path.join(system.GetFilenameDirectory(source_file), disc_image_file),
                delete_original = True,
                verbose = verbose,
                exit_on_failure = exit_on_failure)
            if not success:
                return (False, "Unable to rewrite xbox disc images")

    # Return output
    return (True, os.path.join(output_dir, system.GetFilenameFile(source_file)))

###########################################################

# Transform PS3 disc image
def TransformPS3DiscImage(
    game_info,
    source_file,
    output_dir,
    verbose = False,
    exit_on_failure = False):

    # Get game info
    game_name = game_info.get_name()
    game_source_dir = game_info.get_source_dir()

    # Make directories
    system.MakeDirectory(output_dir, verbose = verbose, exit_on_failure = exit_on_failure)

    # Get dkey file
    dkey_file = os.path.join(game_source_dir, game_name + ".dkey")
    if not os.path.exists(dkey_file):
        return (False, "Unable to find corresponding dkey file")

    # Get disc images
    disc_image_files = []
    if source_file.endswith(".iso"):
        disc_image_files = [system.GetFilenameFile(source_file)]
    if source_file.endswith(".m3u"):
        disc_image_files = playlist.ReadPlaylist(source_file, verbose = verbose, exit_on_failure = exit_on_failure)

    # Extract disc images
    for disc_image_file in disc_image_files:
        if disc_image_file.endswith(".iso"):

            # Extract ps3 disc image
            success = playstation.ExtractPS3ISO(
                iso_file = os.path.join(system.GetFilenameDirectory(source_file), disc_image_file),
                dkey_file = dkey_file,
                extract_dir = output_dir,
                verbose = verbose,
                exit_on_failure = exit_on_failure)
            if not success:
                return (False, "Unable to extract ps3 disc images")

            # Extract ps3 pkg files
            for pkg_file in system.BuildFileListByExtensions(output_dir, extensions = [".PKG", ".pkg"]):
                should_extract = False
                if "PS3_GAME/PKGDIR" in pkg_file:
                    should_extract = True
                if "PS3_EXTRA" in pkg_file:
                    should_extract = True
                if should_extract:
                    pkg_dir = system.GetFilenameDirectory(pkg_file)
                    pkg_name = system.GetFilenameBasename(pkg_file)
                    success = playstation.ExtractPSNPKG(
                        pkg_file = pkg_file,
                        extract_dir = os.path.join(pkg_dir, pkg_name),
                        verbose = verbose,
                        exit_on_failure = exit_on_failure)
                    if not success:
                        return (False, "Unable to extract ps3 pkg files")

    # Touch index file
    success = system.TouchFile(
        src = os.path.join(output_dir, config.raw_files_index),
        verbose = verbose,
        exit_on_failure = exit_on_failure)
    if not success:
        return (False, "Unable to create raw index")

    # Return output
    return (True, os.path.join(output_dir, config.raw_files_index))

###########################################################

# Transform PS3 network package
def TransformPS3NetworkPackage(
    game_info,
    source_file,
    output_dir,
    verbose = False,
    exit_on_failure = False):

    # Make directories
    system.MakeDirectory(output_dir, verbose = verbose, exit_on_failure = exit_on_failure)

    # Copy rap files
    for obj in system.GetDirectoryContents(system.GetFilenameDirectory(source_file)):
        if obj.endswith(".rap"):
            rap_file = os.path.join(system.GetFilenameDirectory(source_file), obj)
            pkg_file = os.path.join(system.GetFilenameDirectory(source_file), obj.replace(".rap", ".pkg"))
            content_id = playstation.GetPSNPackageContentID(pkg_file)
            if content_id:
                success = system.CopyFileOrDirectory(
                    src = rap_file,
                    dest = os.path.join(output_dir, content_id + ".rap"),
                    verbose = verbose,
                    exit_on_failure = exit_on_failure)
                if not success:
                    return (False, "Unable to copy rap files")

    # Extract ps3 pkg files
    for obj in system.GetDirectoryContents(system.GetFilenameDirectory(source_file)):
        if obj.endswith(".pkg"):
            pkg_file = os.path.join(system.GetFilenameDirectory(source_file), obj)
            success = playstation.ExtractPSNPKG(
                pkg_file = pkg_file,
                extract_dir = output_dir,
                verbose = verbose,
                exit_on_failure = exit_on_failure)
            if not success:
                return (False, "Unable to extract ps3 pkg files")

    # Touch index file
    success = system.TouchFile(
        src = os.path.join(output_dir, config.raw_files_index),
        verbose = verbose,
        exit_on_failure = exit_on_failure)
    if not success:
        return (False, "Unable to create raw index")

    # Return output
    return (True, os.path.join(output_dir, config.raw_files_index))

###########################################################

# Transform PSV network package
def TransformPSVNetworkPackage(
    game_info,
    source_file,
    output_dir,
    verbose = False,
    exit_on_failure = False):

    # Make directories
    system.MakeDirectory(output_dir, verbose = verbose, exit_on_failure = exit_on_failure)

    # Copy work.bin files
    for obj in system.GetDirectoryContents(system.GetFilenameDirectory(source_file)):
        if obj.endswith(".work.bin"):
            work_bin_file = os.path.join(system.GetFilenameDirectory(source_file), obj)
            success = system.CopyFileOrDirectory(
                src = os.path.join(system.GetFilenameDirectory(source_file), obj),
                dest = os.path.join(output_dir, "work.bin"),
                verbose = verbose,
                exit_on_failure = exit_on_failure)
            if not success:
                return (False, "Unable to copy work.bin files")

    # Extract psv pkg files
    for obj in system.GetDirectoryContents(system.GetFilenameDirectory(source_file)):
        if obj.endswith(".pkg"):
            pkg_file = os.path.join(system.GetFilenameDirectory(source_file), obj)
            success = playstation.ExtractPSNPKG(
                pkg_file = pkg_file,
                extract_dir = output_dir,
                verbose = verbose,
                exit_on_failure = exit_on_failure)
            if not success:
                return (False, "Unable to extract psv pkg files")

    # Touch index file
    success = system.TouchFile(
        src = os.path.join(output_dir, config.raw_files_index),
        verbose = verbose,
        exit_on_failure = exit_on_failure)
    if not success:
        return (False, "Unable to create raw index")

    # Return output
    return (True, os.path.join(output_dir, config.raw_files_index))

###########################################################

# Transform game file
def TransformGameFile(
    game_info,
    source_file,
    output_dir,
    keep_setup_files = False,
    verbose = False,
    exit_on_failure = False):

    # Get game info
    game_category = game_info.get_category()
    game_subcategory = game_info.get_subcategory()

    # Output dir doesn't exist
    if not os.path.isdir(output_dir):
        return (False, "Output directory doesn't exist")

    # Create temporary directory
    tmp_dir_success, tmp_dir_result = system.CreateTemporaryDirectory(verbose = verbose)
    if not tmp_dir_success:
        return (False, tmp_dir_result)

    # Transform result
    transform_success = False
    transform_result = ""

    # Computer
    if game_category == config.game_category_computer:
        transform_success, transform_result = TransformComputerPrograms(
            game_info = game_info,
            source_file = source_file,
            output_dir = tmp_dir_result,
            keep_setup_files = keep_setup_files,
            verbose = verbose,
            exit_on_failure = exit_on_failure)
        if not transform_success:
            return (False, transform_result)

    # Microsoft Xbox/Xbox 360
    elif game_subcategory in [config.game_subcategory_microsoft_xbox, config.game_subcategory_microsoft_xbox_360]:
        iso_success, iso_result = TransformDiscImage(
            game_info = game_info,
            source_file = source_file,
            output_dir = tmp_dir_result,
            verbose = verbose,
            exit_on_failure = exit_on_failure)
        if not iso_success:
            return (False, iso_result)
        transform_success, transform_result = TransformXboxDiscImage(
            game_info = game_info,
            source_file = iso_result,
            output_dir = tmp_dir_result,
            verbose = verbose,
            exit_on_failure = exit_on_failure)
        if not transform_success:
            return (False, transform_result)

    # Sony PlayStation 3
    elif game_subcategory == config.game_subcategory_sony_playstation_3:
        iso_success, iso_result = TransformDiscImage(
            game_info = game_info,
            source_file = source_file,
            output_dir = os.path.join(tmp_dir_result, "iso"),
            verbose = verbose,
            exit_on_failure = exit_on_failure)
        if not iso_success:
            return (False, iso_result)
        transform_success, transform_result = TransformPS3DiscImage(
            game_info = game_info,
            source_file = iso_result,
            output_dir = os.path.join(tmp_dir_result, "output"),
            verbose = verbose,
            exit_on_failure = exit_on_failure)
        if not transform_success:
            return (False, transform_result)

    # Sony PlayStation Network - PlayStation 3
    elif game_subcategory == config.game_subcategory_sony_playstation_network_ps3:
        transform_success, transform_result = TransformPS3NetworkPackage(
            game_info = game_info,
            source_file = source_file,
            output_dir = tmp_dir_result,
            verbose = verbose,
            exit_on_failure = exit_on_failure)
        if not transform_success:
            return (False, transform_result)

    # Sony PlayStation Network - PlayStation Vita
    elif game_subcategory == config.game_subcategory_sony_playstation_network_psv:
        transform_success, transform_result = TransformPSVNetworkPackage(
            game_info = game_info,
            source_file = source_file,
            output_dir = tmp_dir_result,
            verbose = verbose,
            exit_on_failure = exit_on_failure)
        if not transform_success:
            return (False, transform_result)

    # No transformation was able to be done, so default to the original file
    if not os.path.exists(transform_result):
        return (True, source_file)

    # Move transformed output out of temporary directory
    success = system.MoveContents(
        src = system.GetFilenameDirectory(transform_result),
        dest = output_dir,
        verbose = verbose,
        exit_on_failure = exit_on_failure)
    if not success:
        return (False, "Unable to move transformed output")

    # Get final result
    final_result_path = os.path.join(output_dir, system.GetFilenameFile(transform_result))

    # Delete temporary directory
    system.RemoveDirectory(tmp_dir_result, verbose = verbose)

    # Return final result
    return (True, final_result_path)
