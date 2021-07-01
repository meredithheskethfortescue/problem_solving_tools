#!/usr/bin/env python3
"""Purge some specific literals from filenames

For some dumb reasons like naming *.pdf files after their title I ended up having several files containing special
characters like `\n` or `,` in their filenames. (Due to copy paste)
While ext4 seems to be fine with that ntfs or fat32 have a problem with that.
Now this script shall fix my shameful past.
"""

import os
from tqdm import tqdm

path = '.'
list_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames]

bad_chars = ('\n', '\r', ',')

for path_src in tqdm(list_files):
    for bad_char in bad_chars:
        path_dst = path_src
        if bad_char in path_src:
            path_dst = path_src.replace(bad_char, '')

        if path_dst != path_src:
            print(f"Renaming: `{os.path.basename(path_dst)}`")
            os.rename(path_src, path_dst)
