import random
import json

def creer_matrice(taille):
    matrice_jeu = []
    liste_random = []
    for _ in range(taille):
        ligne = []
        for _ in range(taille):
            random_block = random.randint(1,8)
            liste_random.append(random_block)
            ligne.append(random_block)
        matrice_jeu.append(ligne)
    return matrice_jeu

def creer_level():
    levels = []
    for height in range(2):
        matrice = creer_matrice(taille)
        level = {"height": height, "map": matrice}
        levels.append(level)
    return levels

def creer_map():
    maps = []
    for i in range(1):
        level = creer_level()
        map = {"name": "Stage {}".format(i), "levels": level}
        maps.append(map)
    return map
    
    
    
taille = 6
# level = creer_level()
# print(level)
# niveaux = creer_map()
# print(niveaux)

json_stock = "./maps/test.json"

with open(json_stock,"w") as f:
    for i in range(1):
        map_data = creer_map()
        json.dump(map_data, f, indent=1)
        f.write('\n')