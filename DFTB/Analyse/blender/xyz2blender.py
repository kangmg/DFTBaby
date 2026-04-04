#!/usr/bin/env python3
"""
Legacy XYZ parser for old Blender workflows.

This file previously mixed Blender-2.49 GUI code with Python-2 syntax.
The modernized version keeps robust XYZ parsing and a compatibility shim
for callers that still instantiate ``cube2blender``.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import List


@dataclass
class xyz:
    filename: str
    coord: List[List[float]] = field(default_factory=list)
    atomtypes: List[str] = field(default_factory=list)

    def readxyz(self) -> None:
        self.coord = []
        self.atomtypes = []

        with open(self.filename, "r", encoding="utf-8") as fh:
            while True:
                line = fh.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue

                try:
                    nat = int(line.split()[0])
                except ValueError as exc:
                    raise ValueError(
                        f"Invalid atom count line in xyz file '{self.filename}': {line!r}"
                    ) from exc

                _title = fh.readline()
                if _title == "":
                    raise ValueError(f"Unexpected EOF in xyz file '{self.filename}'.")

                for _ in range(nat):
                    words = fh.readline().split()
                    if len(words) < 4:
                        raise ValueError("Malformed xyz coordinate line.")
                    atname = words[0].lower()
                    x, y, z = (float(v) for v in words[1:4])
                    self.atomtypes.append(atname)
                    self.coord.append([x, y, z])


class cube2blender:
    """Compatibility shim for retired Blender rendering path."""

    def __init__(self, xyz_obj: xyz):
        self.xyz = xyz_obj

    def blenderstructure(self) -> None:
        raise RuntimeError(
            "Blender rendering helpers were retired in Python 3 modernization. "
            "Use parsed XYZ coordinates from this module directly."
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse legacy XYZ files.")
    parser.add_argument("xyz_file", help="Path to .xyz file")
    args = parser.parse_args()

    data = xyz(args.xyz_file)
    data.readxyz()
    print(f"Read xyz: atoms={len(data.atomtypes)}, coordinates={len(data.coord)}")


if __name__ == "__main__":
    main()
