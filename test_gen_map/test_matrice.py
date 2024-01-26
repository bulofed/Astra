import random

def creer_matrice(taille):
    matrice_jeu = []
    for _ in range(taille):
        ligne = []
        for _ in range(taille):
            random_block = random.randint(1,8)
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
    for i in range(4):
        level = creer_level()
        map = {"name": "Stage {}".format(i), "levels": level}
        maps.append(map)
    return maps
    
    
    
taille = 6
level = creer_level()
print(level)
# niveaux = creer_map()
# print(niveaux)