# -*- coding: utf-8 -*-

"""dirtydir.

Usage:
  dirtydir ls [--only-dirty] [--only-clean] [--verbose]
  dirtydir lock <subdirectory>
  dirtydir lock --all
  dirtydir (-h | --help)
  dirtydir --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --verbose     Produce verbose output.

"""
from docopt import docopt
import json
import os
import hashlib
import sys

from dirtydir import __version__

__author__ = "Stefan Hudelmaier"
__copyright__ = "Stefan Hudelmaier"
__license__ = "apache"

CHUNK_SIZE = 4096
PERSISTENCE_FILENAME = '.dirtydir.json'


def md5(filename):
    result = hashlib.md5()
    with open(filename, "rb") as input_file:
        for chunk in iter(lambda: input_file.read(CHUNK_SIZE), b""):
            result.update(chunk)
    return result.hexdigest()


def calculate_hash(folder):
    result = hashlib.md5()
    for root, dirs, files in os.walk(folder):
        for name in files:
            filename = os.path.join(root, name)
            s = filename + "_" + md5(filename)
            result.update(s.encode('utf-8'))

    return result.hexdigest()


def read_persisted_hashes():
    if os.path.exists(PERSISTENCE_FILENAME):
        with open(PERSISTENCE_FILENAME) as persistent_file:
            return json.loads(persistent_file.read())

    return {}


def persist_hashes(hashes):
    with open(PERSISTENCE_FILENAME, "w") as out:
        out.write(json.dumps(hashes, sort_keys=True, indent=2, separators=(',', ': ')))


def list_all_subfolders():
    return [f.name for f in os.scandir(".") if f.is_dir() and not f.name.startswith(".")]


def list_subfolders(verbose):

    subfolders = list_all_subfolders()

    changed_subfolders = []
    unchanged_subfolders = []

    hashes = read_persisted_hashes()

    for subfolder in subfolders:
        hash_value = hashes.get(subfolder)

        calculated_hash = calculate_hash(subfolder)

        if verbose:
            print("subfolder: %s: persisted: %s, current: %s" % (subfolder, hash_value, calculated_hash), file=sys.stderr)

        if hash_value == calculated_hash:
            unchanged_subfolders.append(subfolder)
        else:
            changed_subfolders.append(subfolder)

    return changed_subfolders, unchanged_subfolders


def lock_subfolder(subfolder):
    hashes = read_persisted_hashes()

    hashes[subfolder] = calculate_hash(subfolder)
    persist_hashes(hashes)


def main():
    arguments = docopt(__doc__, version=__version__)

    if arguments['--only-clean'] and arguments['--only-dirty']:
        print("--only-clean and --only-dirty flags are mutually exclusive", file=sys.stderr)
        sys.exit(1)

    if arguments['--only-dirty']:
        output_changed = True
    elif arguments['--only-clean']:
        output_changed = False
    else:
        # The default is to output changed directories
        output_changed = True

    if arguments["ls"]:
        changed_subfolders, unchanged_subfolders = list_subfolders(arguments['--verbose'])
        list_to_output = changed_subfolders if output_changed else unchanged_subfolders

        for subfolder in list_to_output:
            print(subfolder)
    elif arguments["lock"]:
        if arguments['--all']:
            for subfolder in list_all_subfolders():
                lock_subfolder(subfolder)
        else:
            lock_subfolder(arguments['<subdirectory>'])


if __name__ == "__main__":
    main()
