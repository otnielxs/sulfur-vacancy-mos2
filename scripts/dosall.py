import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

HA_TO_EV = 27.2114

files = {
    "Pristine": "MoS2_Pristine-1.dos",
    "Vacancy": "MoS2_Vaccancy-1.dos",
    "Vac+O2":  "MoS2_O2-1.dos",
    "Vac+H2O": "MoS2_H2O-1.dos",
}

plt.figure(figsize=(8,5))

for label, fname in files.items():

    E = []
    DOS = []
    OCC = []

    with open(fname) as f:

        for line in f:

            cols = line.split()

            if len(cols) < 3:
                continue

            try:
                e = float(cols[0])
                d = float(cols[1])
                occ = float(cols[2])

                E.append(e)
                DOS.append(d)
                OCC.append(occ)

            except ValueError:
                continue

    E = np.array(E)
    DOS = np.array(DOS)
    OCC = np.array(OCC)

    # Cari HOMO
    occupied = E[OCC > 0]

    if len(occupied) == 0:
        EF = 0.0
    else:
        EF = occupied.max()

    # Shift terhadap HOMO/Fermi
    E = (E - EF) * HA_TO_EV

    # Fokus sekitar gap
    mask = (E > -5) & (E < 5)

    E = E[mask]
    DOS = DOS[mask]

    # Smooth DOS
    DOS = gaussian_filter1d(DOS, sigma=2)

    plt.plot(
        E,
        DOS,
        linewidth=2,
        label=label
    )

plt.axvline(
    0,
    color='black',
    linestyle='--',
    linewidth=1
)

plt.xlabel(r"$E-E_F$ (eV)")
plt.ylabel("DOS")

plt.xlim(-5,5)

plt.legend()

plt.tight_layout()

plt.savefig(
    "compare_dos.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
