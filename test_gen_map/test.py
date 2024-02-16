import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# Function to generate random points with a minimum number of points
def generate_random_points(num_points, min_points=0):
    attempts = 0
    while attempts < 10:
        points = np.random.rand(num_points, 2)
        unique_points = np.unique(points, axis=0)
        if len(unique_points) >= min_points:
            return unique_points
        attempts += 1
    return None

# Function to perform Lloyd's Relaxation Algorithm
def lloyds_relaxation(points, iterations=10):
    for _ in range(iterations):
        try:
            if len(points) < 4:
                print("Not enough unique points to construct initial simplex.")
                return points, None, None, None
            vor = Voronoi(points)
        except Exception as e:
            print(f"Voronoi computation failed: {e}")
            return points, None, None, None

        valid_regions = [region for region in vor.regions if len(region) > 0 and -1 not in region]
        if not valid_regions:
            print("Voronoi regions are not valid.")
            return points, None, None, None

        centroids = []
        for region in valid_regions:
            polygon = np.array([vor.vertices[i] for i in region])
            centroid = np.mean(polygon, axis=0)
            centroids.append(centroid)
        
        points = np.array(centroids)

    return points, vor.vertices, vor.regions, vor.ridge_vertices

# Generate random points with a minimum of 2 points
points = generate_random_points(3)

# Plot initial Voronoi diagram
vor = Voronoi(points)
voronoi_plot_2d(vor)
plt.title('Initial Voronoi Diagram')
plt.show()
