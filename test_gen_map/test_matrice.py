import random
import json
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d

def creer_points(taille):
    return [(random.uniform(0, taille), random.uniform(0, taille)) for _ in range(taille)]

def creer_matrice(taille, height, max_count):
    points = creer_points(max_count)
    vor = Voronoi(points)

    matrice_jeu = []
    for i in range(taille):
        ligne = []
        for j in range(taille):
            region_index = voronoi_region_index(i, j, vor)
            ligne.append(region_index + 1)
        matrice_jeu.append(ligne)
    return matrice_jeu

def voronoi_region_index(x, y, vor):
    point = np.array([x, y])
    region_index = vor.point_region[np.argmin([np.linalg.norm(point - vor.vertices[i]) for i in vor.regions[vor.point_region[point]]])]
    return region_index

def creer_level(max_count):
    levels = []
    for height in range(2):
        matrice = creer_matrice(taille, height, max_count)
        level = {"height": height, "map": matrice}
        levels.append(level)
    return levels

def creer_map(max_count):
    maps = []
    for i in range(1):
        level = creer_level(max_count)
        map_data = {"name": "Stage {}".format(i), "levels": level}
        maps.append(map_data)
    return map_data

taille = 10
max_count = 25
json_stock = "./maps/test.json"

with open(json_stock, "w") as f:
    for i in range(1):
        map_data = creer_map(max_count)
        json.dump(map_data, f, indent=1)
        f.write('\n')
