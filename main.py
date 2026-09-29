"""
Imports:
"""

import numpy as np
import matplotlib.pyplot as plt
import pathlib

from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from matplotlib.collections import LineCollection
from IPython.display import HTML
from IPython.display import display

import matplotlib
matplotlib.rcParams['animation.embed_limit'] = 100000

print("Imports Successful!")


"""
Project Setup:
"""

# GLOBAL VARIABLES
class config:
    BASE_DIR = pathlib.Path(__file__).resolve().parent
    INPUT_FILE = BASE_DIR / "paths" / "circle_peace.dat"
    CANVAS_SIZE = 10
    ANIMATION_LOOP_TIME = 1
    FRAMES_PER_SECOND = 240
    FRAMES = int(ANIMATION_LOOP_TIME * FRAMES_PER_SECOND)
    TIME_PER_FRAME = int(1000 / FRAMES_PER_SECOND)
    MAX_CIRCLES_RENDERED = 50
    MAX_EPICYCLES = 200

# Loads Data
def load_data(filename):
  try:
    return np.loadtxt(filename)
  except OSError as e:
    print(f"Error loading {filename}: {e}")
    return np.empty((0, 2))


"""
 Mathematical Functions:
"""

# Calculates Average
def meanptp(arr):
  return np.mean(np.array([np.max(arr), np.min(arr)]))

# Converts Data to Complex Values
def data_to_complexes(data):
  complexData = []
  for point in data:
    complexData.append(point[0] + (point[1] * 1j))
  return np.array(complexData)

# Recenters and scales points base on canvas size
def recenter_complex_path(complex_points, canvas_size, padding = 20):
  canvas = canvas_size - padding
  reals = complex_points.real
  imags = complex_points.imag

  translate = (meanptp(reals) + (meanptp(imags) * 1j))
  complex_points -= translate
  
  reals = complex_points.real
  imags = complex_points.imag

  if (np.max(imags) > np.max(reals)):
    scalar = (canvas/2)/np.max(imags) + ((canvas/2)/np.max(imags) * 1j)
  else:
    scalar = (canvas/2)/np.max(reals) + ((canvas/2)/np.max(reals) * 1j)

  
  reals *= scalar.real
  imags *= scalar.imag
  complex_points = reals + imags * 1j

  return complex_points

# Fast Fourier Transform
def fft(data):
  return np.fft.fft(data) / len(data)


"""
Animation Math Functions:
"""

# Sorts ftt frequencies
def get_sorted_freqs_and_coeffs(fft_coeffs):
    N = len(fft_coeffs)
    freqs = np.fft.fftfreq(N, d=1/N)
    # we want the frequencies to be sorted as 0, 1, -1, 2, -2, ...
    indices = sorted(range(N), key=lambda i: (abs(freqs[i]), freqs[i] >= 0))
    return freqs[indices], fft_coeffs[indices]

# Sets up the plot
def setup_plot(canvas_size):
    limit = 2/3 * canvas_size
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_xlabel("Real Axis")
    ax.set_ylabel("Imaginary Axis")
    ax.set_aspect('equal', adjustable='box')
    return fig, ax

# Generates time values
def generate_t_vals(N, frames):
  return np.linspace(0, 1.1, max(N, frames))

# Generates a matrix with rows (t) and columns (k), each cell representing (e^(-2*pi*i*k*t*(1/N)))
def generate_exp_matrix(t_vals, freqs):
  n = len(freqs)
  output = np.outer(t_vals, freqs) * (-2j * np.pi)
  return np.exp(output)

# Compute all required information
def precompute_animation_data(fft_coeffs, frames, max_epicycles):
  # (COMPUTE `N` AND `t_vals` HERE)
  n = len(fft_coeffs)
  t_vals = generate_t_vals(n, frames)

  freqs, coeffs = get_sorted_freqs_and_coeffs(fft_coeffs)

  freqs, coeffs = freqs[:max_epicycles], coeffs[:max_epicycles]

  # (COMPUTE `exp_matrix` AND `path_points` HERE)
  exp_matrix = generate_exp_matrix(t_vals, freqs)
  path_points = exp_matrix @ coeffs

  # We will return t_vals, exp_matrix, coeffs, path_points for further use
  return t_vals, exp_matrix, coeffs, path_points, freqs
   

"""
Animation:
"""
# Precompute function
def precomute_function(fft_coeffs):
  t_vals, exp_matrix, coeffs, path_pts, freqs = precompute_animation_data(fft_coeffs, config.FRAMES, config.MAX_EPICYCLES)
  radii = np.abs(coeffs)

  out = output_function(freqs, coeffs)
  with open("function.txt", "w") as file:
    file.write(out)
  print("Function calculated!")
  return t_vals, exp_matrix, coeffs, path_pts, radii

# Runs the animation
def run_animation(fft_coeffs):
  # Precompute data
  t_vals, exp_matrix, coeffs, path_pts, radii = precomute_function(fft_coeffs)

  print("Creating animation...")

  # Setup screen
  fig, ax = setup_plot(config.CANVAS_SIZE)

  # Create vector lines
  trace_line, = ax.plot([], [], lw=2, color='blue', zorder=2)
  vectors = LineCollection([], colors='r', linewidths=1, zorder=3)
  ax.add_collection(vectors)
  vector_segment_arr = np.zeros((len(coeffs), 2, 2))

  # Create cricles
  circles = [Circle((0, 0), 0, edgecolor='gray', facecolor='none', linestyle='dotted', zorder=1) for _ in coeffs[:config.MAX_CIRCLES_RENDERED]]
  for c in circles:
    ax.add_patch(c)

  # Initializer
  def init():
    trace_line.set_data([], [])
    vectors.set_segments([])
    for c in circles:
      c.center = (0, 0)
      c.radius = 0
    return [trace_line, vectors] + circles

  # Update Function
  def update(frame):
    idx = int(len(t_vals) * frame / config.FRAMES) + 1

    vecs = coeffs * exp_matrix[idx]
    tips = np.empty_like(vecs)
    np.cumsum(vecs, out=tips)
    origins = np.concatenate(([0 + 0j], tips[:-1]))

    # Update trace line
    trace_line.set_data(path_pts.real[:idx], path_pts.imag[:idx])

    # Update vectors
    vector_segment_arr[:, 0, 0] = origins.real
    vector_segment_arr[:, 0, 1] = origins.imag
    vector_segment_arr[:, 1, 0] = tips.real
    vector_segment_arr[:, 1, 1] = tips.imag
    vectors.set_segments(vector_segment_arr)

    # Update circles
    for i in range(min(config.MAX_CIRCLES_RENDERED, len(circles))):
      o = origins[i]
      circles[i].center = (o.real, o.imag)
      circles[i].radius = radii[i]

    return [trace_line, vectors] + circles

  # Run animation
  ani = FuncAnimation(
    fig, update, frames=config.FRAMES,
    init_func=init, blit=True, interval=config.TIME_PER_FRAME
  )
  plt.close(fig)
  with open("animation.html", "w") as file:
    file.write(HTML(ani.to_jshtml()).data)


def output_function(freqs, coeffs):
  output = ""
  arr = []
  for c, f in zip(coeffs, freqs):
    arr.append("(" + format(c, 'f').replace("j", "i") + ")e^{" + format(f, 'f') + "i2\\pi t}")
  output = "+".join(arr)
  return output


"""
Main Program
"""

if __name__ == "__main__":
  raw_data = load_data(config.INPUT_FILE)
  complex_path = recenter_complex_path(data_to_complexes(raw_data), config.CANVAS_SIZE)
  fft_path = fft(complex_path)
  print("Setup Successful! Loading animation...")
  # precomute_function(fft_path)
  run_animation(fft_path)
  print("Finished!")