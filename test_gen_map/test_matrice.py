import random
import json

def creer_matrice(taille, height, max_count):
    matrice_jeu = []
    count = 0
    for _ in range(taille):
        ligne = []
        for _ in range(taille):
            if height == 0:
                random_block = random.randint(1, 3)
            else:
                if count < max_count:
                    random_block = 5
                    count += 1
                else:
                    random_block = random.randint(1, 4)
            ligne.append(random_block)
        matrice_jeu.append(ligne)
    return matrice_jeu

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
    return maps

taille = 10
max_count = 25
json_stock = "./maps/test.json"

with open(json_stock, "w") as f:
    for i in range(1):
        map_data = creer_map(max_count)
        json.dump(map_data, f, indent=1)
        f.write('\n')
