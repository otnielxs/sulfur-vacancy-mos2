import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import re

# ==========================================
# USER SETTINGS
# ==========================================

bands_file = "MoS2_H2O_bs"

k_ticks = [0, 20, 40, 60]
k_labels = ["Γ", "M", "K", "Γ"]

emin = -8
emax = 8

# ==========================================
# READ BAND FILE
# ==========================================

with open(bands_file) as f:
    lines = f.readlines()

bands = []
current_k = []

vbm = -1e9

for line in lines:

    if re.match(r'^\s*#\s*Point', line):

        if current_k:
            bands.append(current_k)

        current_k = []
        continue

    if line.strip().startswith("#"):
        continue

    cols = line.split()

    if len(cols) < 3:
        continue

    try:

        band = int(cols[0])

        energy = float(cols[1])

        occ = float(cols[2])

        current_k.append(energy)

        if occ > 0.0:
            vbm = max(vbm, energy)

    except ValueError:
        pass

if current_k:
    bands.append(current_k)

bands = np.array(bands)

# Shift to VBM = 0
bands = bands - vbm

nk, nb = bands.shape

# ==========================================
# BUILD DOS FROM EIGENVALUES
# ==========================================

all_eigs = bands.flatten()

Egrid = np.linspace(emin, emax, 3000)

dos = np.zeros_like(Egrid)

sigma = 0.08

for e in all_eigs:
    dos += np.exp(-(Egrid-e)**2/(2*sigma**2))

dos /= np.sqrt(2*np.pi)*sigma

dos = gaussian_filter1d(dos, sigma=3)

# ==========================================
# PLOT
# ==========================================

fig, (ax_band, ax_dos) = plt.subplots(
    1,
    2,
    figsize=(8,5),
    sharey=True,
    gridspec_kw={
        "width_ratios":[2.0,1.0],
        "wspace":0.02
    }
)

# -------- BAND --------

x = np.arange(nk)

for ib in range(nb):

    ax_band.plot(
        x,
        bands[:,ib],
        color="gold",
        lw=1.0
    )

ax_band.axhline(
    0,
    color="black",
    ls="--"
)

for k in k_ticks:

    ax_band.axvline(
        k,
        color="gray",
        lw=0.5
    )

ax_band.set_xlim(0, nk-1)

ax_band.set_ylim(emin, emax)

ax_band.set_xticks(k_ticks)

ax_band.set_xticklabels(k_labels)

ax_band.set_ylabel("E - VBM (eV)")

# -------- DOS --------

ax_dos.plot(
    dos,
    Egrid,
    color="gold"
)

ax_dos.fill_betweenx(
    Egrid,
    0,
    dos,
    color="gold",
    alpha=0.3
)

ax_dos.axhline(
    0,
    color="black",
    ls="--"
)

ax_dos.set_xlabel("DOS")

ax_dos.tick_params(
    axis='y',
    left=False,
    labelleft=False
)

plt.tight_layout()

plt.savefig(
    "band_dos.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
