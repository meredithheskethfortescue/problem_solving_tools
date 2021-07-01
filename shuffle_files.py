#!/usr/bin/env python3
"""Achieve shuffle by setting a randomized prefix to *.mp3 files

Some old or just simple built mp3-player have no shuffle functionality and play music alphanumerically.
This script achieves a shuffle by adding a randomized prefix to the filenames in a given directory.
"""

import os
import re
from tqdm import tqdm

import numpy as np

np.random.seed(7)


def scan_for_mp3(dir_src: str) -> [str]:
    """Scan directory for *.mp3 files
    :param dir_src: source directory
    :return: list of basenames
    """
    return [f for f in os.listdir(dir_src) if f.endswith('.mp3')]


def slice_existing_prefixes(basenames_src: [str]) -> [str]:
    """Slice the hex prefix from a filename if existing"""

    def slice_prefix(f: str):
        """Slice prefix if existing"""
        if re.match(r"^[0-9a-f]{4}_.*\.mp3$", f):
            return f[5:]  # prefix has 4 hex digits and a following `_` -> 5 digits
        else:
            return f

    return [slice_prefix(f) for f in basenames_src]


def hex_prefixes(n: int, precision: int = 4) -> [str]:
    # create hex values
    hex_strings = [f'{v:#0{precision + 2}x}' for v in list(range(n))]
    # slice leading `0x` identifier
    return [v[2:] for v in hex_strings]


def main():
    # catch input path
    dir_src = input("Inputpath:\n")

    # scan for *.mp3 files and wait for confirmation
    basenames_src = scan_for_mp3(dir_src)

    print("\nFound *.mp3 files:", *basenames_src, sep="\n")
    confirm = input("Are you sure to rename these files? y/[n]\n")
    print()
    if confirm is not 'y':
        print("Abort.\n")
        exit()

    # slice existing prefixes from source basenames
    basenames_src_no_prefix = slice_existing_prefixes(basenames_src)

    # build random prefixes
    prefixes = hex_prefixes(len(basenames_src))
    np.random.shuffle(prefixes)

    # create new basenames
    basenames_dst = [os.path.join(dir_src, prefix + '_' + basename)
                     for prefix, basename in zip(prefixes, basenames_src_no_prefix)]

    # rename files
    for src, dst in tqdm(zip(basenames_src, basenames_dst), desc="Renaming files", total=len(basenames_dst)):
        os.rename(os.path.join(dir_src, src),
                  os.path.join(dir_src, dst))

    print("\nRenaming finished.\n")


if __name__ == '__main__':
    main()
    # touch '0af7_Interpret - has-written-a-song.mp3' '14be_Foo - Bar.mp3' '1337_Alice - Bob.mp3' 'A Song has no Prefix.mp3' '1337_broken prefix.mp3' 'More Gibberish - Stuff'
