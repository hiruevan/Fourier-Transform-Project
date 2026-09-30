import numpy as np
import funcs as c

# config
INPUT_FILE = "test_data/projectile_height_vs_time.dat"

# Load coordinate points
data = c.read_file(INPUT_FILE)

print("Animating and finding best fit...")

best = c.animate_polynomial_fit(
    data,
    len(data)
)

# -------------------------------------------------
# Calculate corresponding polynomial
# using the SAME method used to select the degree
# -------------------------------------------------

x = np.array([p[0] for p in data])
k = np.array([p[1] for p in data])

coeffs = np.polyfit(
    x,
    k,
    best
)

print("\nComplete! Here is the polynomial:")
print(c.output_function(coeffs))