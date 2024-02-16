import random
import json

def creer_matrice(taille, height):
    matrice_jeu = []
    for _ in range(taille):
        ligne = []
        for _ in range(taille):
            if height == 0:
                random_block = random.randint(1, 3)
            elif height == 1:
                random_block = random.randint(4, 5)
            else:
                random_block = random.randint(1, 8)
            ligne.append(random_block)
        matrice_jeu.append(ligne)
    return matrice_jeu

def creer_level():
    levels = []
    for height in range(2):
        matrice = creer_matrice(taille, height)
        level = {"height": height, "map": matrice}
        levels.append(level)
    return levels

def creer_map():
    maps = []
    for i in range(1):
        level = creer_level()
        map_data = {"name": "Stage {}".format(i), "levels": level}
        maps.append(map_data)
    return maps

taille = 6
json_stock = "./test_gen_map/test.json"

with open(json_stock, "w") as f:
    for i in range(1):
        map_data = creer_map()
        json.dump(map_data, f, indent=1)
        f.write('\n')
