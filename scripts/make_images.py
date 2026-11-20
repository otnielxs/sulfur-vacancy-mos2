from ase.io import read, write
from ase.mep import NEB

initial = read("initial_fixed.xyz")
final   = read("final_fixed.xyz")

images = [initial]

for i in range(3):
    images.append(initial.copy())

images.append(final)

neb = NEB(images)
neb.interpolate()

for i, img in enumerate(images):
    write(f"image{i+1}.xyz", img)
