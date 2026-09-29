from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def read_file(filepath):
    data = []
    with open(filepath, 'r') as file:
        for line in file:
            # Split the line into two parts and convert to float
            parts = line.strip().split()
            if len(parts) == 2:
                x, y = map(float, parts)
                data.append([x, y])
    return data

def output_function(coeffs):
    out = []
    n = len(coeffs) - 1
    for i, c in enumerate(coeffs):
        out.append(format(c, "f") + "x^{" + format(n - i, "f") + "}")
    return "+".join(out)

def select_important_points(data, max_points=10):
    """
    Selects the most significant points for interpolation and checks if y-values are ascending.
    
    Parameters:
        data: list of [x, y]
        max_points: number of points to return (default 11)

    Returns:
        (reduced_points, is_ascending)
        - reduced_points: List of [x, y] points (no duplicate x-values, max length = max_points)
        - is_ascending: True if y-values are strictly increasing, False otherwise
    """
    # Combine duplicate x-values by averaging their y-values
    x_groups = defaultdict(list)
    for x, y in data:
        x_groups[x].append(y)

    merged_data = [[x, sum(ys) / len(ys)] for x, ys in x_groups.items()]
    merged_data.sort(key=lambda p: p[0])

    if len(merged_data) <= max_points:
        reduced = merged_data
    else:
        # Always keep first and last
        important_points = [merged_data[0], merged_data[-1]]

        # Compute delta-y between adjacent points
        deltas = []
        for i in range(1, len(merged_data) - 1):
            delta_y = abs(merged_data[i][1] - merged_data[i - 1][1])
            deltas.append((delta_y, i))

        # Select top (max_points - 2) indices by delta-y
        deltas.sort(reverse=True, key=lambda x: x[0])
        top_indices = sorted(idx for _, idx in deltas[:max_points - 2])

        for idx in top_indices:
            important_points.append(merged_data[idx])

        reduced = sorted(important_points, key=lambda p: p[0])

    # Check if y-values are strictly ascending
    y_vals = [p[1] for p in reduced]
    is_ascending = all(y_vals[i] < y_vals[i+1] for i in range(len(y_vals) - 1))

    return reduced, is_ascending

def plot_polynomial(coeffs, data=None, x_min=None, x_max=None, num=200):
    """
    Plots a polynomial defined by `coeffs` and optionally overlays the original data.

    Parameters:
    -----------
    coeffs : array-like
        Polynomial coefficients [a0, a1, ..., an] for a0*x^n + a1*x^(n-1) + ... + an.
        (Same format as returned by np.polyfit or np.linalg.solve with np.vander.)
    data : list of [x, y], optional
        Original points to scatter-plot.
    x_min, x_max : float, optional
        Range over which to plot the polynomial. If None, auto-computed from data or [-10, 10].
    num : int
        Number of points to sample when plotting the curve.
    """
    # Determine plotting range
    if data:
        xs = np.array([p[0] for p in data])
        x_min = xs.min() if x_min is None else x_min
        x_max = xs.max() if x_max is None else x_max
    else:
        x_min = -10 if x_min is None else x_min
        x_max =  10 if x_max is None else x_max

    # Sample points
    x_plot = np.linspace(x_min, x_max, num)
    # Evaluate polynomial
    y_plot = np.polyval(coeffs, x_plot)

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(x_plot, y_plot, label='Fitted polynomial', linewidth=2)

    if data:
        y_data = [p[1] for p in data]
        plt.scatter(xs, y_data, color='red', zorder=5, label='Original data')

    plt.title("Polynomial Fit")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()

def animate_polynomial_fit(data, max_degree):
    """
    Animate polynomial fits from degree 1 to max_degree,
    then display the best-degree polynomial at the end.

    The best degree is selected using adjusted R².
    """

    # Convert data to NumPy arrays
    all_x = np.array([p[0] for p in data])
    all_y = np.array([p[1] for p in data])

    # Set up plot
    fig, ax = plt.subplots()

    scatter = ax.scatter(
        all_x,
        all_y,
        color='red',
        label='Original Data'
    )

    line, = ax.plot(
        [],
        [],
        color='blue',
        label='Polynomial Fit'
    )

    text = ax.text(
        0.05,
        0.95,
        '',
        transform=ax.transAxes,
        verticalalignment='top'
    )

    ax.set_xlim(
        np.min(all_x) - 1,
        np.max(all_x) + 1
    )

    ax.set_ylim(
        np.min(all_y) - 10,
        np.max(all_y) + 10
    )

    ax.set_title("Animated Polynomial Fit")
    ax.legend()
    ax.grid(True)

    # Smooth x values used to draw the polynomial
    x_fit = np.linspace(
        np.min(all_x),
        np.max(all_x),
        300
    )

    # -------------------------------------------------
    # Determine valid degrees
    # -------------------------------------------------

    max_valid_degree = min(max_degree, 6)

    # -------------------------------------------------
    # Calculate the best degree BEFORE animation
    # -------------------------------------------------

    best_degree = 1
    best_score = -np.inf

    for degree in range(1, max_valid_degree + 1):

        try:
            # Fit polynomial
            coeffs = np.polyfit(
                all_x,
                all_y,
                degree
            )

            # Predict original data
            predicted_y = np.polyval(
                coeffs,
                all_x
            )

            # Calculate R²
            ss_res = np.sum(
                (all_y - predicted_y) ** 2
            )

            ss_tot = np.sum(
                (all_y - np.mean(all_y)) ** 2
            )

            if ss_tot > 0:
                r_squared = 1 - (
                    ss_res / ss_tot
                )
            else:
                r_squared = 0

            # Calculate adjusted R²
            n = len(all_y)
            p = degree

            if n > p + 1:
                adjusted_r_squared = 1 - (
                    (1 - r_squared)
                    * (n - 1)
                    / (n - p - 1)
                )
            else:
                adjusted_r_squared = -np.inf

            # Check if this is the best degree
            if adjusted_r_squared > best_score:
                best_score = adjusted_r_squared
                best_degree = degree

            print(
                f"Degree {degree}: "
                f"Adjusted R²={adjusted_r_squared:.6f}"
            )

        except np.linalg.LinAlgError:
            print(
                f"Degree {degree}: failed"
            )

    # -------------------------------------------------
    # Print final result
    # -------------------------------------------------

    print()
    print("================================")
    print(f"Best Degree: {best_degree}")
    print(f"Best Score: {best_score:.6f}")
    print("================================")
    print()

    # -------------------------------------------------
    # Animation update function
    # -------------------------------------------------

    def update(frame):

        # ---------------------------------------------
        # Final frame: show best polynomial
        # ---------------------------------------------

        if frame == "best":

            coeffs = np.polyfit(
                all_x,
                all_y,
                best_degree
            )

            y_fit = np.polyval(
                coeffs,
                x_fit
            )

            predicted_y = np.polyval(
                coeffs,
                all_x
            )

            # Calculate MSE
            mse = np.mean(
                (all_y - predicted_y) ** 2
            )

            # Calculate correlation
            if (
                np.std(all_y) > 0
                and np.std(predicted_y) > 0
            ):
                correlation = np.corrcoef(
                    all_y,
                    predicted_y
                )[0, 1]
            else:
                correlation = 0

            # Calculate direction correlation
            actual_direction = np.diff(all_y)
            predicted_direction = np.diff(predicted_y)

            if (
                len(actual_direction) > 1
                and np.std(actual_direction) > 0
                and np.std(predicted_direction) > 0
            ):
                direction_correlation = np.corrcoef(
                    actual_direction,
                    predicted_direction
                )[0, 1]
            else:
                direction_correlation = 0

            # Draw best polynomial
            line.set_data(
                x_fit,
                y_fit
            )

            # Update graph text
            text.set_text(
                f"BEST FIT\n"
                f"Degree: {best_degree}\n"
                f"MSE: {mse:.4f}\n"
                f"Correlation: {correlation:.4f}\n"
                f"Direction: {direction_correlation:.4f}\n"
                f"Adjusted R²: {best_score:.4f}"
            )

            ax.set_title(
                f"Best Polynomial Fit — Degree {best_degree}"
            )

            return line, text

        # ---------------------------------------------
        # Normal degree frame
        # ---------------------------------------------

        degree = frame

        try:
            # Fit polynomial
            coeffs = np.polyfit(
                all_x,
                all_y,
                degree
            )

            # Calculate smooth polynomial
            y_fit = np.polyval(
                coeffs,
                x_fit
            )

            # Calculate predictions
            predicted_y = np.polyval(
                coeffs,
                all_x
            )

            # MSE
            mse = np.mean(
                (all_y - predicted_y) ** 2
            )

            # Overall correlation
            if (
                np.std(all_y) > 0
                and np.std(predicted_y) > 0
            ):
                correlation = np.corrcoef(
                    all_y,
                    predicted_y
                )[0, 1]
            else:
                correlation = 0

            # Direction correlation
            actual_direction = np.diff(all_y)
            predicted_direction = np.diff(predicted_y)

            if (
                len(actual_direction) > 1
                and np.std(actual_direction) > 0
                and np.std(predicted_direction) > 0
            ):
                direction_correlation = np.corrcoef(
                    actual_direction,
                    predicted_direction
                )[0, 1]
            else:
                direction_correlation = 0

            # R²
            ss_res = np.sum(
                (all_y - predicted_y) ** 2
            )

            ss_tot = np.sum(
                (all_y - np.mean(all_y)) ** 2
            )

            if ss_tot > 0:
                r_squared = 1 - (
                    ss_res / ss_tot
                )
            else:
                r_squared = 0

            # Adjusted R²
            n = len(all_y)
            p = degree

            if n > p + 1:
                adjusted_r_squared = 1 - (
                    (1 - r_squared)
                    * (n - 1)
                    / (n - p - 1)
                )
            else:
                adjusted_r_squared = -np.inf

            # Update graph
            line.set_data(
                x_fit,
                y_fit
            )

            text.set_text(
                f"Degree: {degree}\n"
                f"MSE: {mse:.4f}\n"
                f"Correlation: {correlation:.4f}\n"
                f"Direction: {direction_correlation:.4f}\n"
                f"Adjusted R²: {adjusted_r_squared:.4f}"
            )

            ax.set_title(
                "Animated Polynomial Fit"
            )

            print(
                f"Degree {degree}: "
                f"MSE={mse:.6f}, "
                f"Correlation={correlation:.6f}, "
                f"Direction={direction_correlation:.6f}, "
                f"Adjusted R²={adjusted_r_squared:.6f}"
            )

        except np.linalg.LinAlgError:

            text.set_text(
                f"Degree {degree} failed"
            )

        return line, text

    # -------------------------------------------------
    # Create animation
    #
    # Normal degrees first,
    # then "best" as the final frame.
    # -------------------------------------------------

    frames = list(
        range(1, max_valid_degree + 1)
    )

    frames.append("best")

    ani = FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=500,
        repeat=False
    )

    plt.show()

    return best_degree