import re
import numpy as np

files = {
    "Pristine": "MoS2_bs",
    "Vacancy": "MoS2_v_bs",
    "Vac+H2O": "MoS2_H2O_bs",
    "Vac+O2":  "MoS2_O2_bs",
}

print(f"{'System':15s} {'VBM(eV)':>12} {'CBM(eV)':>12} {'Gap(eV)':>12}")
print("-"*55)

for name, fname in files.items():

    vbm = -1e9
    cbm =  1e9

    with open(fname) as f:

        for line in f:

            cols = line.split()

            if len(cols) < 3:
                continue

            try:
                band = int(cols[0])
                energy = float(cols[1])
                occ = float(cols[2])

            except:
                continue

            if occ > 1e-6:
                vbm = max(vbm, energy)

            else:
                cbm = min(cbm, energy)

    gap = cbm - vbm

    print(
        f"{name:15s} "
        f"{vbm:12.4f} "
        f"{cbm:12.4f} "
        f"{gap:12.4f}"
    )
