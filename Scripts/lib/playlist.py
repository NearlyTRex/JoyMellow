# Imports
import os, os.path
import sys

# Local imports
import config
import command
import programs
import system
import environment

# Read playlist file
def ReadPlaylist(input_file, verbose = False, exit_on_failure = False):
    try:
        if verbose:
            system.Log("Reading playlist file %s" % input_file)
        playlist_contents = []
        with open(input_file, "r", encoding="utf8") as f:
            playlist_contents = []
            for line in f.readlines():
                playlist_contents.append(line.strip())
        return playlist_contents
    except Exception as e:
        if exit_on_failure:
            system.LogError("Unable to read playlist file %s" % input_file)
            system.LogError(e)
            sys.exit(1)
        return []

# Write playlist file
def WritePlaylist(output_file, playlist_contents = [], verbose = False, exit_on_failure = False):
    try:
        if verbose:
            system.Log("Writing playlist file %s" % output_file)
        with open(output_file, "w", encoding="utf8") as f:
            for entry in playlist_contents:
                f.write(entry + "\n")
        return True
    except Exception as e:
        if exit_on_failure:
            system.LogError("Unable to write playlist file %s" % output_file)
            system.LogError(e)
            sys.exit(1)
        return False

# Generate playlist file
def GeneratePlaylist(source_dir, output_file, extensions = [], recursive = False, only_keep_ends = False, verbose = False, exit_on_failure = False):

    # Generate playlist contents
    playlist_contents = []
    if recursive:
        for file in system.BuildFileListByExtensions(
            root = source_dir,
            extensions = extensions):
            if only_keep_ends:
                playlist_contents.append(system.GetFilenameFile(file))
            else:
                playlist_contents.append(file)
    else:
        for obj in system.GetDirectoryContents(source_dir):
            obj_path = os.path.join(source_dir, obj)
            if os.path.isfile(obj_path):
                for extension in extensions:
                    if obj_path.endswith(extension):
                        if only_keep_ends:
                            playlist_contents.append(obj)
                        else:
                            playlist_contents.append(obj_path)

    # Write playlist
    return WritePlaylist(
        output_file = output_file,
        playlist_contents = playlist_contents,
        verbose = verbose,
        exit_on_failure = exit_on_failure)

# Generate tree playlist file
def GenerateTreePlaylist(source_dir, output_file, extensions = [], verbose = False, exit_on_failure = False):
    return GeneratePlaylist(
        source_dir = source_dir,
        output_file = output_file,
        extensions = extensions,
        recursive = True,
        verbose = verbose,
        exit_on_failure = exit_on_failure)

# Generate local playlists
def GenerateLocalPlaylists(source_dir, extensions = [], verbose = False, exit_on_failure = False):

    # Check each directory for the requested files
    for input_dir in system.BuildDirectoryList(source_dir):
        print(input_dir)
        if system.DoesDirectoryContainFilesByExtensions(
            path = input_dir,
            extensions = extensions,
            recursive = False):

            # Generate local playlist
            success = GeneratePlaylist(
                source_dir = input_dir,
                output_file = os.path.join(input_dir, system.GetDirectoryName(input_dir) + ".m3u"),
                extensions = extensions,
                recursive = False,
                only_keep_ends = True,
                verbose = verbose,
                exit_on_failure = exit_on_failure)
            if not success:
                return False

    # Must be successful
    return True
