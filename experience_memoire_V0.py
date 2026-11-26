# Expérience de rappel sériel pour voir l'effet de similarité phonologique
# -> version 0 avec 2 listes pour tester

# DÉBUT

import time

print("Vous allez voir et entendre des listes de 5 mots. À la fin de chaque liste, écrivez les mots dans l’ordre où vous les avez vus.")

# Mes listes de mots ->
LISTES = [
    ["chat", "rat", "plat", "bras", "drap"],      # liste similaire (S1)
    ["livre", "chaise", "pont", "nez", "fleur"],  # liste différente (D1)
]

# Pour le contexte voir mon dossier : "En quoi l'effet de similarité phonologique 
# constitue-t-il une preuve que l'information est encodée 
# sous forme phonologique en mémoire de travail ?" (projet de L2)

# Fonction qui calcule le score ->
# (compte les mots rappelés à la bonne place)
def calculer_score(reponse, liste_correcte):
    mots = reponse.lower().split()
    score = 0

    for i, mot in enumerate(mots[:5]):
        if mot == liste_correcte[i]:   # même mot à la même position ?
            score = score + 1
    return score

# Déroulement de l'expérience ->
for liste in LISTES:
    for mot in liste:
        print("\n" * 30 + mot.upper())
        time.sleep(1)
    print("\n" * 30)

    reponse = input("Tape les mots dans l'ordre : ")
    print(f"Score : {calculer_score(reponse, liste)} / 5")

    time.sleep(3)

# FIN

