import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# Function to generate random points with a minimum number of points
def generate_random_points(num_points, min_points=4):
    while True:
        points = np.random.rand(num_points, 2)
        unique_points = np.unique(points, axis=0)
        if len(unique_points) >= min_points:
            return unique_points

# Function to perform Lloyd's Relaxation Algorithm
def lloyds_relaxation(points, iterations=10):
    for _ in range(iterations):
        try:
            if len(points) < 4:
                print("Not enough unique points to construct initial simplex.")
                return points
            vor = Voronoi(points)
        except Exception as e:
            print(f"Voronoi computation failed: {e}")
            return points

        valid_regions = [region for region in vor.regions if len(region) > 0 and -1 not in region]
        if not valid_regions:
            print("Voronoi regions are not valid.")
            return points

        centroids = []
        for region in valid_regions:
            polygon = np.array([vor.vertices[i] for i in region])
            centroid = np.mean(polygon, axis=0)
            centroids.append(centroid)
        
        points = np.array(centroids)

    return points

# Generate random points with a minimum of 4 points
points = generate_random_points(20, min_points=4)

# Plot initial Voronoi diagram
vor = Voronoi(points)
voronoi_plot_2d(vor)
plt.title('Initial Voronoi Diagram')
plt.show()

# Apply Lloyd's Relaxation Algorithm
new_points = lloyds_relaxation(points, iterations=10)

# Plot Voronoi diagram after relaxation
vor_relaxed = Voronoi(new_points)
voronoi_plot_2d(vor_relaxed)
plt.title("Voronoi Diagram after Lloyd's Relaxation")
plt.show()
