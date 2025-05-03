#!/bin/env python3
import glob
import os

root_path = "raw_data/zig/lib/std"

data = ["/* Zig Standard Lib (lib/std) source code collected for SFT/ref */"]
for filepath in sorted(glob.glob(f'{root_path}/**/*.zig', recursive=True)):
    # Get path relative to root (nicer markers)
    relpath = os.path.relpath(filepath, start=root_path)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    data.append(f"<|system|>\nThis is the source code from the Zig 0.14.0 Standard Library. source filename: std/{relpath}\n<|endoftext|>\n<|code|>\n{content}\n<|endoftext|>\n")

with open('raw_data/zig_stdlib_concat.txt', 'w', encoding='utf-8') as out:
    out.write('\n'.join(data))

print(f"Wrote {len(data)} .zig files into zig_stdlib_concat.txt")
