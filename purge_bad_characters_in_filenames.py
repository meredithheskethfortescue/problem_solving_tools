#!/usr/bin/env python3
"""Purge some specific literals from filenames

For some dumb reasons like naming *.pdf files after their title, I ended up having several files containing special
characters like `\n` or `,` in their filenames. (Due to copy paste I didn't realized having those in the filename
because the file-explorer was hiding them.)
While ext4 seems to be fine with that, ntfs as well as fat32 have a problem with it.
Now this script shall fix my shameful past.
"""

import os
from tqdm import tqdm

# list from where to start?
path = input("Directory that will be searched in recursively:\n")

# list all files recursively
list_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames]

# those will be purged
bad_chars = ("\n", "\r", ",", ";", ":")

count_issues = 0

# cycle through found files
for path_src in tqdm(list_files):
    # make a copy
    path_dst = path_src
    found_issues = []

    # cycle through bad chars
    for bad_char in bad_chars:
        if bad_char in path_src:
            # if a wild bad char appeared, replace it with an empty string
            found_issues.append(bad_char)
            path_dst = path_src.replace(bad_char, "")

    # if a bad char appeared, those should be different now
    if path_dst != path_src:
        # tell the user what's happening
        print(f"Renaming: `{os.path.basename(path_dst)}` (Due to {found_issues})")
        # rename file
        os.rename(path_src, path_dst)
        count_issues += 1

print(f"\nRenamed {count_issues} files.")
