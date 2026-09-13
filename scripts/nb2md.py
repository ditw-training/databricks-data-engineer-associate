#!/usr/bin/env python3
"""Minimal .ipynb -> markdown converter (fallback when jupyter is unavailable).

Markdown cells pass through; code cells become fenced blocks. Outputs are dropped,
which is what we want for print: the PDFs document the code, not one run of it.
"""
import json
import sys


def main(path):
    nb = json.load(open(path, encoding="utf-8"))
    out = []
    for cell in nb["cells"]:
        src = "".join(cell["source"]).rstrip()
        if not src:
            continue
        if cell["cell_type"] == "markdown":
            out.append(src)
        else:
            lang = "sql" if src.lstrip().startswith("%sql") else "python"
            out.append(f"```{lang}\n{src}\n```")
    sys.stdout.write("\n\n".join(out) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
