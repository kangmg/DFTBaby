import numpy as np
import sys

if len(sys.argv) < 4:
    print("Usage: %s <solvent box .xyz> <partial charges of solv. molecule> <output file>" % sys.argv[0])
    print("  Assigns partial charges to each solvent molecule in solvent box.")
    exit(-1)

xyz_in = sys.argv[1]
charges_in = sys.argv[2]
charges_out = sys.argv[3]

# partial charges for each atom in a solvent molecule
charges = np.loadtxt(charges_in)

# solvent box
fh_in = open(xyz_in, "r")
lines = fh_in.readlines()
fh_in.close()

solvent = lines[2:]

# replace atomic labels in xyz-file with partial charges 
header = lines[:2]
with open(charges_out, "w") as fh_out:
    for hl in header:
        print(hl.strip(), file=fh_out)

    for iat, l in enumerate(solvent):
        iat %= len(charges)
        parts = l.strip().split()
        parts[0] = "%s" % charges[iat]
        lrepl = " ".join(parts)
        print(lrepl, file=fh_out)
    
