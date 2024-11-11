import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial import KDTree

# Parameters for distribution and animation
num_points = 1000  # Total number of points
num_clusters = 100  # Number of focal zones for initial distribution
initial_score = 10  # Starting score for the signal propagation
min_neighbors = 5  # Minimum number of neighbors to start with
max_neighbors = 15  # Maximum number of neighbors as signal weakens
frames = 50  # Number of frames in the animation
fps = 10  # Frames per second for saving the animation
output_file = 'signaling_map_animation.mp4'  # Output file name for the animation

# Arrays to store coordinates
x = np.array([])
y = np.array([])

# Generate non-uniform points by creating clusters
for _ in range(num_clusters):
    center_x = np.random.uniform(-100, 100)
    center_y = np.random.uniform(-100, 100)
    scale_x = np.random.uniform(0.2, 5)
    scale_y = np.random.uniform(0.2, 5)
    points_per_cluster = num_points // num_clusters
    cluster_x = np.random.normal(center_x, scale_x, points_per_cluster)
    cluster_y = np.random.normal(center_y, scale_y, points_per_cluster)
    x = np.concatenate((x, cluster_x))
    y = np.concatenate((y, cluster_y))

# Combine x and y coordinates into a point array
points = np.column_stack((x, y))
tree = KDTree(points)  # KDTree for efficient neighbor searching

# Initialize the signal score
signal_score = initial_score

# Randomly choose an anchor point to start signaling
anchor_idx = np.random.choice(num_points)
anchor_point = points[anchor_idx]
neighbor_points = [anchor_point]

# Set up the plot
fig, ax = plt.subplots(figsize=(8, 8))
scat = ax.scatter(x, y, marker='o', s=5, c='blue', alpha=0.6)  # Plot points
ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)

# List to store lines (edges) for the connections and their current alphas
lines = []


# Function to calculate the number of neighbors based on the signal score
def calculate_neighbors(score):
    # Use a quadratic function to drastically increase neighbors as strength decreases
    return int(min_neighbors + (max_neighbors - min_neighbors) * ((initial_score - score) / initial_score) ** 2)


# Function to calculate a faster-decaying alpha based on the signal score
def calculate_alpha(score):
    # Use a cubic decay to reduce alpha more quickly as score decreases
    return (score / initial_score) ** 0.0


# Function to update the frame
def update(frame):
    global signal_score, neighbor_points

    current_point = neighbor_points.pop(0) if neighbor_points else anchor_point

    # Calculate the number of neighbors based on the current signal score
    num_neighbors = calculate_neighbors(signal_score)

    # Find `num_neighbors` closest neighbors
    distances, indices = tree.query(current_point, k=num_neighbors + 1)
    closest_neighbors = indices[1:num_neighbors + 1]  # skip self (first result)

    # Draw lines between the current point and each neighbor, with a faster-decaying alpha
    for neighbor_idx in closest_neighbors:
        neighbor = points[neighbor_idx]
        line_alpha = calculate_alpha(signal_score)  # Apply cubic decay to alpha
        line, = ax.plot([current_point[0], neighbor[0]], [current_point[1], neighbor[1]], 'r-', alpha=line_alpha)
        lines.append(line)

        # Queue neighbors of the current point for next iteration
        if signal_score > 1:
            neighbor_points.append(neighbor)

    # Reduce the signal score each frame
    signal_score = max(signal_score - 1, 0)

    # Return the line objects to update
    return lines


# Create animation
ani = animation.FuncAnimation(fig, update, frames=frames, blit=True)
ani.save(output_file, writer='ffmpeg', fps=fps)
plt.show()
