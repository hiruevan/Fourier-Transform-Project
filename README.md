# Fourier Transform Project

A Python project that explores **Fourier transforms, complex numbers, epicycles, and mathematical curve reconstruction**.

The main program takes a set of 2D points, interprets them as complex numbers, computes their Fourier transform, and uses the resulting Fourier coefficients to reconstruct the original shape using rotating vectors (epicycles).

The project also contains a separate **polynomial optimizer** for experimenting with polynomial regression and determining an appropriate polynomial degree using adjusted R².

---

## Features

### Fourier Transform Visualizer

The main program:

1. Loads a collection of 2D coordinate points.
2. Converts each point into a complex number.
3. Recenters and scales the path.
4. Computes the Discrete Fourier Transform using NumPy.
5. Sorts the resulting frequencies for epicycle visualization.
6. Reconstructs the path using rotating complex vectors.
7. Animates the epicycles drawing the original shape.
8. Saves the resulting animation as an HTML file.
9. Generates a Fourier-series representation of the function.

### Polynomial Optimizer

The `polynomial optimizer` directory contains a separate tool that:

* Loads `(x, y)` data from `.dat` files.
* Tests polynomial degrees from 1 through 6.
* Calculates:

  * Mean squared error (MSE)
  * Correlation
  * Direction correlation
  * R²
  * Adjusted R²
* Selects the polynomial degree with the highest adjusted R².
* Animates the polynomial fits as the degree increases.
* Outputs the resulting polynomial.

---

## Project Structure

```text
Fourier-Transform-Project/
│
├── main.py
├── funcs.py
├── function.txt
├── README.md
│
├── paths/
│   ├── *.dat
│   │
│   └── images/
│       ├── *.png
│       ├── *.jpg
│       └── *.svg
│
└── polynomial optimizer/
    ├── main.py
    ├── funcs.py
    │
    └── test_data/
        ├── arch_bridge_shape.dat
        ├── ball_height_vs_time.dat
        ├── cooling_coffee_temperature_vs_time.dat
        ├── plant_growth_height_vs_time.dat
        ├── projectile_height_vs_time.dat
        ├── rocket_launch_altitude_vs_time.dat
        ├── spring_applied_force_vs_displacement.dat
        └── water_temperature_vs_time.dat
```

---

# Requirements

The project uses Python and the following libraries:

* [NumPy](https://numpy.org/)
* [Matplotlib](https://matplotlib.org/)
* [IPython](https://ipython.org/)

Install the dependencies with:

```bash
pip install numpy matplotlib ipython
```

Python 3.9+ is recommended.

---

# Fourier Transform Visualizer

## Running the Project

From the root project directory:

```bash
python main.py
```

The default input file is:

```text
paths/circle_peace.dat
```

The program will process the path and create an animation using Fourier epicycles.

The generated animation is saved as:

```text
animation.html
```

A Fourier representation of the reconstructed function is also written to:

```text
function.txt
```

---

## Changing the Input Image

The input path is selected in `main.py` through the configuration:

```python
class config:
    INPUT_FILE = BASE_DIR / "paths" / "circle_peace.dat"
```

To use another path, change the filename.

For example:

```python
INPUT_FILE = BASE_DIR / "paths" / "pikachu.dat"
```

The repository includes several example paths:

* `BYU_Cougars_logo.dat`
* `among_us.dat`
* `charizard.dat`
* `christus.dat`
* `circle_peace.dat`
* `pikachu.dat`
* `priddis.dat`
* `star.dat`
* `thumbs_up.dat`
* `yoshi.dat`

The corresponding source images are located in:

```text
paths/images/
```

---

# How the Fourier Transform Works

A two-dimensional point

```text
(x, y)
```

can be represented as a complex number:

```text
z = x + yi
```

The entire path can therefore be represented as a sequence of complex numbers:

```text
z₀, z₁, z₂, ..., zₙ
```

The project applies the Discrete Fourier Transform to this sequence.

Conceptually, the transform decomposes the path into rotating complex components:

```text
z(t) = Σ cₖ e^(2πikt)
```

where:

* `cₖ` is a complex Fourier coefficient.
* `k` is a frequency.
* `t` is time.
* `e^(2πikt)` represents a rotating vector.

Each coefficient therefore corresponds to a rotating vector with:

* **Magnitude** → the radius of the epicycle.
* **Angle** → the initial rotation of the epicycle.
* **Frequency** → how quickly the vector rotates.

Adding all of these vectors together reconstructs the original path.

---

# Epicycle Animation

The animation visualizes the Fourier decomposition directly.

Each Fourier coefficient becomes a rotating vector. The vectors are chained together:

```text
Origin
  │
  ├── Vector 1
  │       │
  │       ├── Vector 2
  │       │       │
  │       │       └── Vector 3
  │       │
  │       └── ...
```

The endpoint of the final vector traces the reconstructed shape.

The program also displays circles representing the radius of the rotating vectors.

The number of vectors displayed is controlled by:

```python
MAX_EPICYCLES = 200
```

The number of circles rendered simultaneously can be controlled with:

```python
MAX_CIRCLES_RENDERED = 50
```

Increasing the number of epicycles generally improves the reconstruction, but also increases the amount of computation and visualization.

---

# Fourier Transform Implementation

The Fourier transform is calculated with:

```python
def fft(data):
    return np.fft.fft(data) / len(data)
```

The division by the number of points normalizes the Fourier coefficients.

The frequencies are then reordered so that the animation processes them approximately in the order:

```text
0, 1, -1, 2, -2, 3, -3, ...
```

This makes the most visually significant low-frequency components appear first.

---

# Path Processing

Before the Fourier transform is calculated, the coordinates are converted to complex numbers and normalized.

The path is:

1. Converted from `(x, y)` coordinates to complex values.
2. Translated toward the origin.
3. Scaled to fit the animation canvas.

This allows input paths with different sizes and coordinate systems to be displayed consistently.

---

# Polynomial Optimizer

The `polynomial optimizer` directory is an independent experiment involving polynomial regression.

Run it with:

```bash
cd "polynomial optimizer"
python main.py
```

The default dataset is:

```text
test_data/projectile_height_vs_time.dat
```

The program tests polynomial degrees from 1 through 6.

---

## Polynomial Degree Selection

For each degree, the program calculates R²:

```text
R² = 1 - SS_res / SS_tot
```

It then calculates adjusted R²:

```text
Adjusted R² =
1 - (1 - R²)(n - 1)/(n - p - 1)
```

where:

* `n` = number of observations
* `p` = number of predictors/parameters represented by the polynomial degree

Adjusted R² is used instead of ordinary R² because ordinary R² generally increases as additional polynomial terms are added. Adjusted R² accounts for the additional model complexity.

The degree with the highest adjusted R² is selected.

---

## Polynomial Test Data

Several datasets are included for experimentation:

| Dataset                                    | Example Application            |
| ------------------------------------------ | ------------------------------ |
| `arch_bridge_shape.dat`                    | Structural/architectural curve |
| `ball_height_vs_time.dat`                  | Projectile motion              |
| `cooling_coffee_temperature_vs_time.dat`   | Cooling behavior               |
| `plant_growth_height_vs_time.dat`          | Growth over time               |
| `projectile_height_vs_time.dat`            | Projectile motion              |
| `rocket_launch_altitude_vs_time.dat`       | Launch trajectory              |
| `spring_applied_force_vs_displacement.dat` | Spring behavior                |
| `water_temperature_vs_time.dat`            | Temperature over time          |

To test another dataset, change:

```python
INPUT_FILE = "test_data/projectile_height_vs_time.dat"
```

in:

```text
polynomial optimizer/main.py
```

---

# Data Format

The `.dat` files contain two numerical columns:

```text
x y
```

For example:

```text
0.0 0.0
1.0 4.5
2.0 8.2
3.0 10.1
```

The Fourier-transform datasets represent 2D paths.

The polynomial-optimizer datasets represent ordinary `(x, y)` measurements.

---

# Output

The Fourier transform program produces:

### `animation.html`

A self-contained HTML representation of the Matplotlib animation.

It shows the Fourier epicycles reconstructing the input path.

### `function.txt`

A Fourier-series representation of the reconstructed path.

It contains terms of the general form:

```text
(c)e^(ki2πt)
```

where `c` is a complex coefficient and `k` is the corresponding frequency.

---

# Configuration

The main Fourier animation can be adjusted through the `config` class in `main.py`:

```python
class config:
    CANVAS_SIZE = 10
    ANIMATION_LOOP_TIME = 1
    FRAMES_PER_SECOND = 240
    MAX_CIRCLES_RENDERED = 50
    MAX_EPICYCLES = 200
```

### `CANVAS_SIZE`

Controls the size of the coordinate system.

### `ANIMATION_LOOP_TIME`

Controls the intended animation duration in seconds.

### `FRAMES_PER_SECOND`

Controls animation resolution.

Higher values produce smoother animations but require more computation.

### `MAX_CIRCLES_RENDERED`

Controls how many epicycle circles are displayed.

### `MAX_EPICYCLES`

Controls how many Fourier coefficients are used to reconstruct the path.

---

# Mathematical Purpose

This project demonstrates how a seemingly complicated shape can be represented as a combination of simple periodic functions.

The central idea is:

> A complex path can be decomposed into many rotating vectors, and the sum of those vectors can reconstruct the original path.

This provides a visual demonstration of the Fourier transform and shows the relationship between:

* Complex numbers
* Periodic functions
* Frequency
* Fourier coefficients
* Vector rotation
* Signal reconstruction
* Data approximation

The polynomial optimizer provides a related exploration of mathematical modeling by demonstrating how increasingly complex polynomial functions can approximate measured data.

---

# Credits and Inspiration

**Created by Evan Hill**

The project was created as an exploration of computational mathematics, Fourier analysis, data visualization, and mathematical curve reconstruction. It was inspired by a BYU math camp project in 2025.

---
