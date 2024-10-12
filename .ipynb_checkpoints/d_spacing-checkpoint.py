import numpy as np

# Function to calculate d-spacing for cubic system
def cubic_d_spacing(a, h, k, l):
    return a / np.sqrt(h**2 + k**2 + l**2)

# Function to calculate d-spacing for hexagonal system
def hexagonal_d_spacing(a, c, h, k, l):
    return a / np.sqrt((4/3) * (h**2 + h*k + k**2) + (c/a)**2 * l**2)

# Define close-packed planes for cubic and hexagonal structures
# (hkl) for cubic (FCC/BCC close-packed planes)
cubic_close_packed_planes = [
    (1, 1, 1), (2, 0, 0), (2, 2, 0), (3, 1, 1), (2, 2, 2), 
    (4, 0, 0), (3, 3, 1), (4, 2, 0), (3, 3, 3), (5, 1, 1),
    (4, 4, 0), (5, 3, 1), (6, 0, 0), (4, 4, 4), (6, 2, 0),
    (5, 5, 1), (6, 3, 3), (5, 5, 5), (7, 1, 1), (6, 4, 0)
]

# (hkil) for hexagonal close-packed planes
hexagonal_close_packed_planes = [
    (1, 0, -1, 1), (1, 0, -1, 0), (1, 1, -2, 0), (1, 1, -2, 1), (2, 0, -2, 0),
    (2, 0, -2, 1), (2, 1, -3, 0), (2, 1, -3, 1), (3, 0, -3, 0), (3, 0, -3, 1),
    (3, 1, -4, 0), (3, 1, -4, 1), (4, 0, -4, 0), (4, 0, -4, 1), (4, 1, -5, 0),
    (4, 1, -5, 1), (5, 0, -5, 0), (5, 0, -5, 1), (5, 1, -6, 0), (5, 1, -6, 1)
]

# Main function to calculate d-spacings
def calculate_d_spacings(crystal_system, a, c=None):
    d_spacings = []
    if crystal_system == 'cubic':
        for h, k, l in cubic_close_packed_planes:
            d = cubic_d_spacing(a, h, k, l)
            d_spacings.append((h, k, l, d))
    elif crystal_system == 'hexagonal':
        if c is None:
            raise ValueError("For hexagonal system, 'c' parameter is required.")
        for h, k, i, l in hexagonal_close_packed_planes:
            d = hexagonal_d_spacing(a, c, h, k, l)
            d_spacings.append((h, k, i, l, d))
    return d_spacings

# Example usage:
lattice_type = input("Enter crystal system (cubic/hexagonal): ").strip().lower()
a = float(input("Enter lattice parameter a (in Å): "))

if lattice_type == 'hexagonal':
    c = float(input("Enter lattice parameter c (in Å): "))
    d_spacings = calculate_d_spacings(lattice_type, a, c)
else:
    d_spacings = calculate_d_spacings(lattice_type, a)

print("\nCalculated d-spacings for close-packed planes:")
if lattice_type == 'cubic':
    for h, k, l, d in d_spacings:
        print(f"(hkl) = ({h}, {k}, {l}): d = {d:.4f} Å")
elif lattice_type == 'hexagonal':
    for h, k, i, l, d in d_spacings:
        print(f"(hkil) = ({h}, {k}, {i}, {l}): d = {d:.4f} Å")
