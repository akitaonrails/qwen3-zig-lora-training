#!/bin/env python3
import glob
import os

lines = []

for prob_file in sorted(glob.glob('raw_data/zig-cookbook/book-src/*.md')):
    # Extract the nn-nn from the problem filename (e.g., 01-05-matrix-mul.md -> 01-05)
    base = os.path.basename(prob_file)
    if base == "SUMMARY.md" or base == "database.md" or base == "intro.md":
        continue
    print(base)
    match_part = base.split('-')[0] + '-' + base.split('-')[1]  # e.g., 01-05

    code_file = f"raw_data/zig-cookbook/src/{match_part}.zig"
    if not os.path.exists(code_file):
        print(f"WARN: No solution found for problem {prob_file} (expected {code_file})")
        continue

    with open(prob_file, 'r', encoding='utf-8') as pf:
        problem_text = pf.read().strip()

    with open(code_file, 'r', encoding='utf-8') as cf:
        code_text = cf.read().strip()

    # Compose chat format
    block = (
        f"<|user|>Solve this problem in Zig 0.14.0:\n{problem_text}\n<|endoftext|>\n"
            f"<|assistant|>This is the Zig 0.14.0 way to solve this:\n```zig\n{code_text}\n```\n<|endoftext|>\n"
    )
    lines.append(block)

with open("raw_data/zig_cookbook_chat.txt", "w", encoding="utf-8") as out:
    out.writelines(lines)

print(f"Wrote {len(lines)} problem/solution chat pairs to zig_cookbook_chat.txt")
