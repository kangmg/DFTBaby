#!/usr/bin/env python3
"""
Legacy Blender helper for Gaussian cube files.

The original script relied on Blender 2.49 APIs and Python 2 syntax.
This modernized module keeps robust cube parsing and VTK export so it is
usable in standard Python 3 environments and Colab-like setups.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass, field
from typing import List, Sequence, Tuple


def _read_grid_line(tokens: Sequence[str]) -> Tuple[int, Tuple[float, float, float]]:
    if len(tokens) < 4:
        raise ValueError("Malformed cube grid line.")
    return int(tokens[0]), (float(tokens[1]), float(tokens[2]), float(tokens[3]))


@dataclass
class cube:
    filename: str
    header: str = ""
    natom: int = 0
    origin: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    nx: int = 0
    ny: int = 0
    nz: int = 0
    ivec: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    jvec: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    kvec: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    atomtypes: List[str] = field(default_factory=list)
    coord: List[List[float]] = field(default_factory=list)
    data1d: List[float] = field(default_factory=list)

    def readCube(self) -> None:
        with open(self.filename, "r", encoding="utf-8") as fh:
            header1 = fh.readline().rstrip("\n")
            header2 = fh.readline().rstrip("\n")
            self.header = f"{header1}\n{header2}"

            nat_line = fh.readline().split()
            if len(nat_line) < 4:
                raise ValueError("Malformed cube header: missing atom count/origin.")
            self.natom = abs(int(nat_line[0]))
            self.origin = (float(nat_line[1]), float(nat_line[2]), float(nat_line[3]))

            self.nx, self.ivec = _read_grid_line(fh.readline().split())
            self.ny, self.jvec = _read_grid_line(fh.readline().split())
            self.nz, self.kvec = _read_grid_line(fh.readline().split())

            self.atomtypes = []
            self.coord = []
            for _ in range(self.natom):
                words = fh.readline().split()
                if len(words) < 5:
                    raise ValueError("Malformed cube atom line.")
                self.atomtypes.append(words[0])
                self.coord.append([float(words[2]), float(words[3]), float(words[4])])

            self.data1d = []
            for line in fh:
                if line.strip():
                    self.data1d.extend(float(x) for x in line.split())

        expected = self.nx * self.ny * self.nz
        if len(self.data1d) < expected:
            raise ValueError(
                f"Cube data truncated: expected {expected} values, got {len(self.data1d)}."
            )
        if len(self.data1d) > expected:
            self.data1d = self.data1d[:expected]

    @property
    def dx(self) -> float:
        return math.sqrt(sum(v * v for v in self.ivec))

    @property
    def dy(self) -> float:
        return math.sqrt(sum(v * v for v in self.jvec))

    @property
    def dz(self) -> float:
        return math.sqrt(sum(v * v for v in self.kvec))

    @property
    def data3d(self) -> List[List[List[float]]]:
        data = [[[0.0 for _ in range(self.nx)] for _ in range(self.ny)] for _ in range(self.nz)]
        ind = 0
        for i in range(self.nx):
            for j in range(self.ny):
                for k in range(self.nz):
                    data[k][j][i] = self.data1d[ind]
                    ind += 1
        return data

    def cube2vtk(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as vtkfile:
            vtkfile.write("# vtk DataFile Version 2.0\n")
            vtkfile.write("vtk representation of a gaussian cube file\n")
            vtkfile.write("ASCII\n\n")
            vtkfile.write("DATASET STRUCTURED_POINTS\n")
            vtkfile.write(f"DIMENSIONS {self.nx} {self.ny} {self.nz}\n")
            vtkfile.write(f"ORIGIN {self.origin[0]} {self.origin[1]} {self.origin[2]}\n\n")
            vtkfile.write(f"SPACING {self.dx} {self.dy} {self.dz}\n")
            vtkfile.write(f"POINT_DATA {self.nx * self.ny * self.nz}\n")
            vtkfile.write("SCALARS scalars float\n")
            vtkfile.write("LOOKUP_TABLE default\n")
            for value in self.data1d:
                vtkfile.write(f"{value}\n")


class cube2blender:
    """
    Legacy compatibility shim.

    Rendering code that depended on Blender 2.49 is intentionally not
    executed in regular Python environments.
    """

    def __init__(self, cube_obj: cube):
        self.cube = cube_obj

    def blenderstructure(self) -> None:
        raise RuntimeError(
            "Blender rendering helpers were retired in Python 3 modernization. "
            "Use this module for cube parsing/VTK export only."
        )

    def isosurface(self, cubeobject: cube, isovalue: float) -> None:
        _ = (cubeobject, isovalue)
        raise RuntimeError(
            "Blender rendering helpers were retired in Python 3 modernization."
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse a Gaussian cube file and optionally export VTK."
    )
    parser.add_argument("cube_file", help="Path to .cube file")
    parser.add_argument("--vtk", help="Optional output .vtk path")
    args = parser.parse_args()

    cube_obj = cube(args.cube_file)
    cube_obj.readCube()

    print(
        f"Read cube: natom={cube_obj.natom}, grid={cube_obj.nx}x{cube_obj.ny}x{cube_obj.nz}"
    )
    if args.vtk:
        cube_obj.cube2vtk(args.vtk)
        print(f"Wrote VTK: {args.vtk}")


if __name__ == "__main__":
    main()
