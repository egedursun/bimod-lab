import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from scipy.spatial import (
    KDTree
)

num_points = 1000
num_clusters = 100
initial_score = 10

min_neighbors = 5
max_neighbors = 15

frames = 50
fps = 10

output_file = 'signaling_map_animation.mp4'

x = np.array([])
y = np.array([])

for _ in range(num_clusters):
    center_x = np.random.uniform(-100, 100)
    center_y = np.random.uniform(-100, 100)
    scale_x = np.random.uniform(0.2, 5)
    scale_y = np.random.uniform(0.2, 5)

    points_per_cluster = num_points // num_clusters

    cluster_x = np.random.normal(
        center_x,
        scale_x,
        points_per_cluster
    )

    cluster_y = np.random.normal(
        center_y,
        scale_y,
        points_per_cluster
    )

    x = np.concatenate(
        (x, cluster_x)
    )

    y = np.concatenate(
        (y, cluster_y)
    )

points = np.column_stack(
    (x, y)
)

tree = KDTree(points)

signal_score = initial_score

anchor_idx = np.random.choice(num_points)
anchor_point = points[anchor_idx]
neighbor_points = [anchor_point]

fig, ax = plt.subplots(
    figsize=(8, 8)
)

scat = ax.scatter(
    x,
    y,
    marker='o',
    s=5,
    c='blue',
    alpha=0.6
)

ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)

lines = []


def calculate_neighbors(score):
    return int(
        min_neighbors + (
            max_neighbors - min_neighbors
        ) * (
            (initial_score - score) / initial_score
        ) ** 2
    )


def calculate_alpha(score):
    return (score / initial_score) ** 0.0


def update(frame):
    global signal_score, neighbor_points

    current_point = (
        neighbor_points.pop(0)
    ) if neighbor_points else anchor_point

    num_neighbors = calculate_neighbors(signal_score)

    distances, indices = tree.query(
        current_point,
        k=num_neighbors + 1
    )

    closest_neighbors = indices[1:num_neighbors + 1]

    for neighbor_idx in closest_neighbors:
        neighbor = points[neighbor_idx]

        line_alpha = calculate_alpha(
            signal_score
        )

        line, = ax.plot(
            [
                current_point[0],
                neighbor[0]
            ],
            [
                current_point[1],
                neighbor[1]
            ],
            'r-',
            alpha=line_alpha
        )
        lines.append(line)

        if signal_score > 1:
            neighbor_points.append(neighbor)

    signal_score = max(signal_score - 1, 0)

    return lines


ani = animation.FuncAnimation(
    fig,
    update,
    frames=frames,
    blit=True
)

ani.save(
    output_file,
    writer='ffmpeg',
    fps=fps
)

plt.show()
