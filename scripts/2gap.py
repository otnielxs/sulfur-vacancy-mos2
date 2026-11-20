files = {
    "Pristine" : "MoS2_bs",
    "Vacancy"  : "MoS2_v_bs",
    "Vac+H2O"  : "MoS2_H2O_bs",
    "Vac+O2"   : "MoS2_O2_bs",
}

for system, fname in files.items():

    print("\n" + "="*80)
    print(system)
    print("="*80)

    current_point = None

    vbm_energy = -1e9
    vbm_info = None

    cbm_energy =  1e9
    cbm_info = None

    with open(fname) as f:

        for line in f:

            if line.startswith("#  Point"):

                cols = line.split()

                try:
                    current_point = int(cols[2])
                except:
                    pass

                continue

            cols = line.split()

            if len(cols) < 3:
                continue

            try:
                band   = int(cols[0])
                energy = float(cols[1])
                occ    = float(cols[2])

            except:
                continue

            # VBM
            if occ > 1e-6 and energy > vbm_energy:

                vbm_energy = energy

                vbm_info = (
                    current_point,
                    band,
                    energy,
                    occ
                )

            # CBM
            if occ < 1e-6 and energy < cbm_energy:

                cbm_energy = energy

                cbm_info = (
                    current_point,
                    band,
                    energy,
                    occ
                )

    gap = cbm_energy - vbm_energy

    print("\nVBM")
    print(
        f"k-point    : {vbm_info[0]}\n"
        f"band       : {vbm_info[1]}\n"
        f"energy(eV) : {vbm_info[2]:.6f}\n"
        f"occupancy  : {vbm_info[3]}"
    )

    print("\nCBM")
    print(
        f"k-point    : {cbm_info[0]}\n"
        f"band       : {cbm_info[1]}\n"
        f"energy(eV) : {cbm_info[2]:.6f}\n"
        f"occupancy  : {cbm_info[3]}"
    )

    print("\nBand Gap")
    print(f"{gap:.6f} eV")
