#!/usr/bin/env python3
"""Chipset names in the ALFA docs must match ALFA's official spec sheets.

AWUS036AXM and AWUS036AXML both carry the MT7921AUN (confirmed on alfa.com.tw, 2026-11-22).
Our own test summary once recorded the AXM as MT7921AU; the USB descriptor is 0e8d:7961 for
both, so the suffix cannot be told apart by testing — the official sheet decides.
Usage (repo root): python3 scripts/check_chipsets.py
"""
import re
import sys
from pathlib import Path

OFFICIAL = {
    "awus036acm": "MT7612U", "awus036achm": "MT7610U", "awus036ach": "RTL8812AU",
    "awus036acs": "RTL8811AU", "awus036eacs": "RTL8821CU", "awus036ax": "RTL8832BU",
    "awus036axer": "RTL8832BU", "awus036axm": "MT7921AUN", "awus036axml": "MT7921AUN",
}
ROW = re.compile(r"^\|\s*(?:Chipset|晶片|芯片)\s*\|\s*([^|]+?)\s*\|", re.M)


def main() -> int:
    bad = 0
    for page in sorted(Path(".").glob("**/01-alfa-network/products/*/index.md")):
        model = page.parent.name
        want = OFFICIAL.get(model)
        if not want:
            continue
        m = ROW.search(page.read_text(encoding="utf-8"))
        if not m:
            print(f"NO CHIPSET ROW  {page}")
            bad += 1
            continue
        got = m.group(1)
        # 允許附註，但必須含官方晶片名，且不得出現「裸 AU」的舊值
        if want not in got or re.search(r"MT7921AU(?!N)", got):
            print(f"WRONG  {page}\n       got {got!r}, expected to contain {want!r}")
            bad += 1
    print(f"{len(OFFICIAL)} models x locales checked, {bad} wrong")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
