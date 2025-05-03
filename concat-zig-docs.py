#!/bin/env python3
import glob
import os

zig_files = glob.glob("raw_data/zig/doc/langref/**/*.zig", recursive=True)
total_input_bytes = 0
file_count = 0
lines = []

for filepath in zig_files:
    file_bytes = os.path.getsize(filepath)
    total_input_bytes += file_bytes
    file_count += 1
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        entry = f"Reference Filename: {filename}\n\n```zig\b{content}\b```\n"
        lines.append(entry)

print(f"Found {file_count} .zig files.")
print(f"Total bytes of .zig source files: {total_input_bytes:,} bytes ({total_input_bytes / 1024:.2f} KB)")

outpath = "raw_data/zig_docs_with_filenames.txt"
with open(outpath, "w", encoding='utf-8') as f:
    for line in lines:
        f.write(line + "\n\n")

final_size = os.path.getsize(outpath)
print(f"Wrote concatenated text to: {outpath}")
print(f"Final output file size: {final_size:,} bytes ({final_size / 1024:.2f} KB)")
