# -> version 1 : les 10 listes --> ordre aléatoire --> résultats enregistrés dans un fichier CSV

# DÉBUT 

import csv # => écrire mes résultats
import os # => crée un dossier 
import random # => ça mélange l'orde de mes listes
import time # => pause(1s par mot)
import unicodedata # => enlève les accents 
from datetime import datetime # => date de passage 

duree_mot = 1 
pause_listes = 3 
fichier_resultats = "donnees/resultats.csv"


# fonction qui enlève les erreurs d'écritures(accent)
# (->pas une erreur de mémoire donc pas comptabilisé)

def norme(mot) :
    mot = mot.lower().strip().replace("œ", "oe")
    mot = unicodedata.normalize("NFD" , mot)
    return "".join(c for c in mot if unicodedata.category(c) != "Mn")

# fonction qui calcule le score des mots si ils sont à la bonne place
def calculer_score(reponse, liste_correcte) :
    mots = reponse.split()
    score = 0 
    for i, mot in enumerate(mots[:len(liste_correcte)]):
        if norme(mot) == norme(liste_correcte[i]): 
            score = score + 1
    return score

 # ma classe qui contient 3 infos : son code (S1...), sont type et ses 5 mots 
class ListeMots : 
    def __init__(self, code, type_liste, mots) :
        self.code = code 
        self.type_liste = type_liste
        self.mots = mots 

# classe du participant (son numéro et ses réponses) 
class Participant :
    def __init__(self, numero):
        self.numero = numero
        self.reponses = [] 

    def ajouter_reponse(self, liste, ordre, reponse):
        self.reponses.append({
            "participant": self.numero,
            "ordre": ordre,                 
            "liste": liste.code,
            "type": liste.type_liste,
            "reponse": reponse,
            "score": calculer_score(reponse, liste.mots),
         })

    def total(self, type_liste):
        return sum(r["score"] for r in self.reponses if r["type"] == type_liste)



# Mes 10 listes de mots ->
LISTES = [
    ListeMots("S1", "similaire", ["chat", "rat", "plat", "bras", "drap"]),
    ListeMots("S2", "similaire", ["pain", "bain", "main", "train", "grain"]),
    ListeMots("S3", "similaire", ["poule", "boule", "moule", "foule", "roule"]),
    ListeMots("S4", "similaire", ["verre", "terre", "mère", "père", "serre"]),
    ListeMots("S5", "similaire", ["bouche", "couche", "mouche", "douche", "touche"]),
    ListeMots("D1", "different", ["livre", "chaise", "pont", "nez", "fleur"]),
    ListeMots("D2", "different", ["sac", "huit", "doigt", "mer", "feu"]),
    ListeMots("D3", "different", ["clé", "rond", "jus", "banc", "voix"]),
    ListeMots("D4", "different", ["mur", "roi", "sel", "bus", "lait"]),
    ListeMots("D5", "different", ["prix", "cœur", "faim", "dos", "pied"]),
]

# déroulement de l'expérience :
class Experience: 
    def __init__(self, listes):
        self.listes = listes 

# je mélange l'ordre des listes 
# chaque participants aura une succesion différente
    def ordre_aleatoire(self):
        ordre = self.listes[:] 
        random.shuffle(ordre)
        return ordre 

# affiche les 5 mots -> 1 par seconde 
    def presenter_liste(self,liste) :
        for mot in liste.mots :
            print("\n" * 30 + mot.upper())
            time.sleep(duree_mot)
        print("\n" * 30)

# déroulement de l'expérience 
    def lancer(self, participant) :
        input("Vous aller lire des listes de 5 mots. Après chaque liste, tapez les mots "
              "dans l'ordre, séparés par des espaces.\nAppuyez sur Entrée pour commencer.")

        for ordre,liste in enumerate(self.ordre_aleatoire(), start = 1):
            self.presenter_liste(liste)
            reponse = input("Vos mots : ")
            participant.ajouter_reponse(liste,ordre,reponse)
            time.sleep(pause_listes)
        print("Merci pour votre participation !!")

# Ajouter les reponses des participants à la fin 
    def enregistrer(self, participant, fichier=fichier_resultats):
        os.makedirs(os.path.dirname(fichier), exist_ok=True)  
        nouveau = not os.path.exists(fichier)                 
        
        with open(fichier, "a", newline="", encoding="utf-8") as f:  
            colonnes = ["participant", "ordre", "liste", "type", "reponse", "score", "date"]
            writer = csv.DictWriter(f, fieldnames=colonnes)
            if nouveau:
                writer.writeheader()  
            for r in participant.reponses:
                writer.writerow({**r, "date": datetime.now().strftime("%Y-%m-%d")})

# lancement -> 
if __name__ == "__main__":
    numero = input("Numéro du participant (ex. P01) : ")
    p = Participant(numero)        
    exp = Experience(LISTES)       
    exp.lancer(p)                  
    exp.enregistrer(p)             
    print(f"Score listes similaires : {p.total('similaire')} / 25")
    print(f"Score listes différentes : {p.total('different')} / 25")

# FIN