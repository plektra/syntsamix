# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Check the two-tier decision log (decision 154).

Every decision number must appear once in INDEX.md, once in a short area file
(docs/decisions/<area>.md) and once in the record file of the same area
(docs/decisions/record/<area>.md), and the index row must name that area.

Usage: python3 tools/check_decisions.py   (exit status 1 on any problem)
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

DECISIONS = Path(__file__).resolve().parent.parent / "docs" / "decisions"
ENTRY = re.compile(r"^(\d+)\. ", re.MULTILINE)
ROW = re.compile(r"^\| (\d+) \|.*\[[^\]]*\]\(([\w-]+)\.md\)", re.MULTILINE)


def entries(folder):
    """Map decision number -> list of area names that hold an entry for it."""
    found = defaultdict(list)
    for path in sorted(folder.glob("*.md")):
        if path.name == "INDEX.md":
            continue
        for number in ENTRY.findall(path.read_text()):
            found[int(number)].append(path.stem)
    return found


def main():
    problems = []
    index = defaultdict(list)
    for number, area in ROW.findall((DECISIONS / "INDEX.md").read_text()):
        index[int(number)].append(area)
    short = entries(DECISIONS)
    record = entries(DECISIONS / "record")

    for number in sorted(set(index) | set(short) | set(record)):
        tiers = {"INDEX.md": index[number], "short file": short[number], "record": record[number]}
        for tier, areas in tiers.items():
            if len(areas) != 1:
                problems.append(f"{number}: {len(areas)} entries in {tier} {areas or ''}".rstrip())
        areas = {a for found in tiers.values() for a in found}
        if len(areas) > 1:
            problems.append(f"{number}: areas disagree {tiers}")

    missing = [n for n in range(1, max(index) + 1) if n not in index]
    if missing:
        problems.append(f"numbers missing from INDEX.md: {missing}")

    for line in problems:
        print(line)
    print(f"{len(index)} decisions, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
