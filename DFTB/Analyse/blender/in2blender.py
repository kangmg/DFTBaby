#!/usr/bin/env python3
"""
Legacy parser for trajectory ``.in`` files used by old Blender helpers.

The original Blender-2.49 GUI code was Python-2 specific and fragile.
This Python 3 rewrite keeps the geometry/vector parsing path stable so the
data can be validated or converted in modern environments.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import List

BOHR_TO_ANGSTROM = 0.529177249


@dataclass
class xyz:
    filename: str
    coord: List[List[float]] = field(default_factory=list)
    vectors: List[List[float]] = field(default_factory=list)
    atomtypes: List[str] = field(default_factory=list)

    def readxyz(self) -> None:
        self.coord = []
        self.vectors = []
        self.atomtypes = []

        with open(self.filename, "r", encoding="utf-8") as fh:
            while True:
                line = fh.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue

                nat = int(line)
                block_atomtypes: List[str] = []
                block_coords: List[List[float]] = []
                block_vectors: List[List[float]] = []

                for _ in range(nat):
                    words = fh.readline().split()
                    if len(words) < 4:
                        raise ValueError("Malformed .in coordinate line.")
                    atname = words[0].lower()
                    x, y, z = (BOHR_TO_ANGSTROM * float(v) for v in words[1:4])
                    block_atomtypes.append(atname)
                    block_coords.append([x, y, z])

                for _ in range(nat):
                    words = fh.readline().split()
                    if len(words) < 3:
                        raise ValueError("Malformed .in vector line.")
                    vx, vy, vz = (BOHR_TO_ANGSTROM * float(v) for v in words[:3])
                    block_vectors.append([vx, vy, vz])

                self.atomtypes.extend(block_atomtypes)
                self.coord.extend(block_coords)
                self.vectors.extend(block_vectors)


class cube2blender:
    """Compatibility shim for retired Blender rendering path."""

    def __init__(self, xyz_obj: xyz):
        self.xyz = xyz_obj

    def blenderstructure(self) -> None:
        raise RuntimeError(
            "Blender rendering helpers were retired in Python 3 modernization. "
            "Use parsed coordinates/vectors from this module directly."
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse a legacy .in trajectory block (coords + vectors)."
    )
    parser.add_argument("input_file", help="Path to .in file")
    args = parser.parse_args()

    data = xyz(args.input_file)
    data.readxyz()
    print(
        f"Read .in data: atoms={len(data.atomtypes)}, "
        f"coords={len(data.coord)}, vectors={len(data.vectors)}"
    )


if __name__ == "__main__":
    main()
