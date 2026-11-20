import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import re
mpl.rcParams.update({
    "font.family": "DejaVu Serif",
    "font.size": 12,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "axes.linewidth": 1.2,
    "lines.linewidth": 1.2,
})

# ====================================================
# CP2K values
# ====================================================

HA_TO_EV = 27.2114

EF = 0

emin = -5
emax = 5

bands_file = "MoS2_bs"
dos_file = "MoS2_Vaccancy-1.dos"

k_ticks = [0, 20, 40, 60]
k_labels = ["Γ", "M", "K", "Γ"]

# ====================================================
# Read DOS
# ====================================================

dos_energy = []
dos_value = []

with open(dos_file) as f:

    for line in f:

        if line.startswith("#"):
            continue

        cols = line.split()

        if len(cols) < 2:
            continue

        try:
            e = float(cols[0]) * HA_TO_EV
            d = float(cols[1])

            dos_energy.append(e - EF)
            dos_value.append(d)

        except ValueError:
            continue

dos_energy = np.array(dos_energy)
dos_value = np.array(dos_value)


# ====================================================
# Read Band Structure (CP2K)
# Select the LAST dataset in mos2_bs
# ====================================================

import re

# Read entire file
with open(bands_file) as f:
    lines = f.readlines()

# Find all dataset headers
set_indices = []

for i, line in enumerate(lines):
    if re.match(r'^\s*#\s*Set\s+\d+', line):
        set_indices.append(i)

if not set_indices:
    raise ValueError("Dataset header not found!")

print("Number of datasets found:", len(set_indices))

# Select last dataset
start = set_indices[-1]

print("Using dataset starting at line:", start + 1)

selected_lines = lines[start:]

# Read expected number of k-points and bands
header = selected_lines[0]

match = re.search(
    r'(\d+)\s+k-points,\s+(\d+)\s+bands',
    header
)

if not match:
    raise ValueError("Cannot read dataset header!")

expected_nk = int(match.group(1))
expected_nb = int(match.group(2))

print("Expected k-points:", expected_nk)
print("Expected bands   :", expected_nb)

# Parse k-point blocks
bands = []
current_k = []

for line in selected_lines:

    # Detect new k-point
    point_match = re.match(
        r'^\s*#\s*Point\s+(\d+)',
        line
    )

    if point_match:

        if current_k:
            bands.append(current_k)

        current_k = []
        continue

    # Skip comments and headers
    if line.strip().startswith("#"):
        continue

    cols = line.split()

    if len(cols) < 3:
        continue

    try:
        band_index = int(cols[0])
        energy = float(cols[1])

        current_k.append(energy - EF)

    except ValueError:
        continue

# Save final k-point
if current_k:
    bands.append(current_k)

# Validate data
band_lengths = [len(k) for k in bands]

print("Actual k-points  :", len(bands))
print("Bands per k-point:", sorted(set(band_lengths)))

if len(bands) != expected_nk:
    raise ValueError("K-point count does not match header!")

if any(n != expected_nb for n in band_lengths):
    raise ValueError("Band count does not match header!")

bands = np.array(bands)

nk, nb = bands.shape

print("Final k-points   :", nk)
print("Final bands      :", nb)


# ====================================================
# Plot
# ====================================================

fig, (ax_band, ax_dos) = plt.subplots(
    1,
    2,
    figsize=(8,5.5),
    sharey=True,
    gridspec_kw={
        "width_ratios":[1.8,1.0],
        "wspace":0
    }
)

x = np.arange(nk)

for ib in range(nb):
    ax_band.plot(
        x,
        bands[:,ib],
        color="#1f77b4",
        linewidth=1.0
    )

ax_band.axhline(
    0,
    linestyle="--",
    color="black",
    linewidth=0.8
)

for k in k_ticks:
    ax_band.axvline(
        k,
        color="gray",
        linewidth=0.6
    )

ax_band.set_xlim(
    k_ticks[0],
    k_ticks[-1]
)

ax_band.set_ylim(
    emin,
    emax
)

ax_band.set_xticks(k_ticks)
ax_band.set_xticklabels(k_labels)

ax_band.set_ylabel(r"$E-E_F$ (eV)")

# ---------------- DOS ----------------

ax_dos.plot(
    dos_value,
    dos_energy,
    color="#1f77b4"
)

ax_dos.fill_betweenx(
    dos_energy,
    0,
    dos_value,
    color="#1f77b4",
    alpha=0.35
)

ax_dos.axhline(
    0,
    linestyle="--",
    color="black",
    linewidth=0.8
)

ax_dos.set_xlim(
    0,
    dos_value.max()*1.1
)

ax_dos.set_xlabel("DOS")

ax_dos.tick_params(
    axis="y",
    left=False,
    labelleft=False
)

ax_dos.spines["left"].set_visible(False)

plt.tight_layout()

plt.savefig(
    "mos2_band_dos.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
