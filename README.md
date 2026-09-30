# Fourier Transform Project

A mathematical modeling and data-analysis project originally created during **BYU Math Camp 2025** and later expanded into a more complete Python project.

The project explores ways of representing data mathematically by fitting polynomial functions to sets of coordinate data and evaluating how well different polynomial degrees describe the data.

> **Note:** Despite the project name, the current implementation focuses primarily on polynomial regression and curve fitting. The repository originally grew from work involving Fourier analysis, but the current Python implementation does not perform a Fourier transform.

---

## Features

* Read coordinate data from `.dat` files
* Plot and visualize datasets
* Fit polynomial functions to data
* Automatically test polynomial degrees from 1 through 6
* Compare polynomial fits using multiple statistical measurements
* Select the best polynomial degree using **adjusted R²**
* Animate the progression of polynomial fits
* Calculate:

  * Mean Squared Error (MSE)
  * Correlation
  * Direction correlation
  * R²
  * Adjusted R²
* Output the resulting polynomial equation
* Includes several example datasets and image-derived datasets

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
│       └── source images
│
└── test_data/
    └── example datasets
```

### `main.py`

The main entry point for the project.

It:

1. Selects an input dataset.
2. Loads the coordinate data.
3. Tests polynomial fits of different degrees.
4. Animates the fitting process.
5. Determines the best polynomial degree.
6. Calculates the final polynomial.
7. Prints the resulting equation.

The default input is:

```python
INPUT_FILE = "test_data/projectile_height_vs_time.dat"
```

To use a different dataset, change `INPUT_FILE`.

---

### `funcs.py`

Contains the primary mathematical and visualization functions used by the project.

Important functions include:

#### `read_file(filepath)`

Reads a `.dat` file containing pairs of numerical coordinates.

Example:

```text
0 0
1 4
2 7
3 9
```

is interpreted as:

```python
[
    [0, 0],
    [1, 4],
    [2, 7],
    [3, 9]
]
```

---

#### `output_function(coeffs)`

Converts polynomial coefficients into a readable polynomial expression.

For example, coefficients representing

```text
2x² + 3x + 1
```

are converted into a string representation of the polynomial.

---

#### `select_important_points(data, max_points=10)`

Reduces a dataset to a smaller collection of significant points.

The function:

* Combines duplicate x-values
* Averages their y-values
* Preserves the first and last points
* Identifies points with large changes in y
* Checks whether the resulting y-values are strictly increasing

---

#### `plot_polynomial(...)`

Plots a polynomial and optionally displays the original dataset alongside it.

---

#### `animate_polynomial_fit(data, max_degree)`

The main analysis function.

It tests polynomial degrees and calculates their statistical performance.

The current implementation limits the tested polynomial degree to **6**.

For each degree, it calculates:

### Mean Squared Error

MSE measures the average squared difference between the predicted and actual values.

$$
MSE = \frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2
$$

Lower MSE indicates that the predictions are, on average, closer to the observed data.

### R²

R² measures how much of the variation in the data is explained by the model.

$$
R^2 = 1-\frac{SS_{res}}{SS_{tot}}
$$

### Adjusted R²

Adjusted R² accounts for the number of parameters in the polynomial, helping prevent increasingly complicated polynomials from automatically appearing better simply because they have more degrees of freedom.

$$
\bar{R}^2 =
1-(1-R^2)
\frac{n-1}{n-p-1}
$$

where:

* \(n\) is the number of observations
* \(p\) is the polynomial degree

The project uses **adjusted R² to select the best polynomial degree**.

---

## Example Datasets

The repository includes several datasets for testing mathematical models.

### Physical / Mathematical Data

Located in `test_data/`:

* `projectile_height_vs_time.dat`
* `ball_height_vs_time.dat`
* `rocket_launch_altitude_vs_time.dat`
* `cooling_coffee_temperature_vs_time.dat`
* `water_temperature_vs_time.dat`
* `plant_growth_height_vs_time.dat`
* `spring_applied_force_vs_displacement.dat`
* `arch_bridge_shape.dat`

These datasets allow the program to be applied to different types of mathematical and physical relationships.

---

## Image Data

The `paths/` directory contains coordinate data generated from images.

Example images include:

* BYU Cougars logo
* Among Us
* Charizard
* Christus
* Pikachu
* Yoshi
* A star
* Thumbs up
* Circle of Peace
* Priddis

The corresponding `.dat` files contain coordinate information representing these shapes.

This allows mathematical curve-fitting techniques to be experimented with on visual data as well as traditional scientific datasets.

---

## Installation

### Requirements

The project requires Python and the following libraries:

* NumPy
* Matplotlib

Install the dependencies with:

```bash
pip install numpy matplotlib
```

---

## Running the Project

From the project directory, run:

```bash
python main.py
```

The program will load the selected dataset and begin analyzing polynomial fits.

The visualization will show the polynomial fits progressing through different degrees before displaying the selected best-fit polynomial.

After the animation, the program prints the resulting polynomial equation.

---

## Using Your Own Data

Create a `.dat` file containing x/y coordinate pairs:

```text
0 1
1 3
2 7
3 13
4 21
```

Then change:

```python
INPUT_FILE = "test_data/projectile_height_vs_time.dat"
```

to the path of your dataset:

```python
INPUT_FILE = "my_data/my_function.dat"
```

Run:

```bash
python main.py
```

The program will automatically fit polynomial models to the data.

---

## Mathematical Goal

A central goal of the project is to investigate how complicated a mathematical model needs to be to accurately describe a dataset.

Given a collection of points

$$
(x_1,y_1),(x_2,y_2),\ldots,(x_n,y_n)
$$

the program searches for a polynomial

$$
f(x)=a_nx^n+a_{n-1}x^{n-1}+\cdots+a_1x+a_0
$$

that provides a useful approximation of the data.

Instead of simply choosing the polynomial with the smallest error, the project uses **adjusted R²** to account for model complexity.

This makes it possible to investigate the tradeoff between:

* Accuracy
* Complexity
* Overfitting
* General mathematical representation

---

## Background

This project began as work during **BYU Math Camp 2025** and was subsequently expanded into a larger programming and mathematical modeling project.

The project combines concepts from:

* Calculus
* Linear algebra
* Statistics
* Numerical methods
* Polynomial regression
* Data visualization
* Mathematical modeling

The original motivation involved exploring how complicated mathematical functions can be constructed from data. The project has since evolved to experiment with different methods of representing and analyzing mathematical relationships.

---

## Future Development

Possible future directions include:

* Implementing an actual Discrete Fourier Transform (DFT)
* Adding Fast Fourier Transform (FFT) support
* Comparing polynomial and Fourier representations
* Visualizing Fourier coefficients
* Reconstructing images using Fourier series
* Adding frequency-domain visualizations
* Improving automatic model selection
* Supporting additional mathematical functions
* Adding interactive dataset selection
* Improving image-to-coordinate conversion
* Comparing multiple model types automatically

---

## Credits

**Created by Evan Hill**

This is a personal programming and mathematics project, with the original concept developing from a BYU math camp project in 2025.
