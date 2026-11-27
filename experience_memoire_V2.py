# version 2 : j'améliore mon code, en créant l'expérience dans une fenêtre avec les mots lus à voix haute

# DÉBUT

import subprocess     # -> je lance la voix
import time           # -> tps de lecture d'un mot
import tkinter as tk  # -> crée une fenêtre

from experience_memoire_V1 import LISTES, Experience, Participant   # (pour utiliser ma version 1)

# mes réglages ->
duree_mot_ms = 1000       # (1 mot par s)
duree_rappel_ms = 10000   # (10 s pour répondre)
pause_ms = 3000           # (3 s -> écran blanc entre les listes)
son = True
voix = "Thomas"


# fonction qui lit le mot à voix haute ->
def dire(mot):
    if son:
        subprocess.run(["say", "-v", voix, mot])

# classe Application -> c'est la fenêtre (écran)
class Application:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.experience = Experience(LISTES)
        self.participant = None
        self.listes = []
        self.index_liste = 0
        self.index_mot = 0
        self.minuteur = None

# design de ma fenêtre ->
        fenetre.title("Expérience de mémoire")
        fenetre.geometry("900x500")
        fenetre.configure(bg="white")

# texte du centre de la fenêtre
        self.texte = tk.Label(fenetre, text="", font=("Arial", 48), bg="white", fg="black")
        self.texte.pack(expand=True)

# le texte de la consigne
        self.consigne = tk.Label(fenetre, text="", font=("Arial", 16), bg="white", fg="black",
                                 wraplength=800)
        self.consigne.pack(pady=10)

# lieu pour écrire (et bouton)
        self.saisie = tk.Entry(fenetre, font=("Arial", 20), width=40)
        self.bouton = tk.Button(fenetre, text="Commencer", font=("Arial", 16),
                                command=self.commencer)

        self.ecran_accueil()

# écran d'accueil ->
    def ecran_accueil(self):
        self.texte.config(text="Bienvenue", font=("Arial", 36))
        self.consigne.config(text=(
            "Vous allez voir et entendre des listes de 5 mots. À la fin de chaque liste, "
            "tapez les mots dans l'ordre, séparés par des espaces, puis appuyez sur Entrée. "
            "Vos réponses sont anonymes. En cliquant sur Commencer, vous acceptez de participer.\n\n"
            "Numéro du participant (ex : P01) :"))
        self.saisie.pack(pady=10)
        self.saisie.focus()
        self.bouton.pack(pady=10)

# bouton commencer ->
    def commencer(self):
        numero = self.saisie.get().strip()
        if numero == "":
            return

        self.participant = Participant(numero)
        self.listes = self.experience.ordre_aleatoire()
        self.bouton.pack_forget()
        self.saisie.pack_forget()
        self.consigne.config(text="")
        self.texte.config(text="", font=("Arial", 48))
        self.fenetre.bind("<Return>", lambda event: self.valider())
        self.fenetre.after(1000, self.liste_suivante)

# pour présenter une nouvelle liste 
    def liste_suivante(self):
        if self.index_liste >= len(self.listes):
            self.fin()
            return 
        self.index_mot = 0
        self.mot_suivant()

# affichez le mot puis le lire puis un nouveau mot 1s plus tard 
    def mot_suivant(self):
        liste = self.listes[self.index_liste]
        if self.index_mot < len(liste.mots) :
            mot = liste.mots[self.index_mot]
            debut = time.time() #heure du départ 
            self.texte.config(text= mot.upper()) # pour afficher le mot 
            self.fenetre.update() #pour que ma fenêtre m'affiche le nom 
            dire(mot) 
            ecoule_ms = int((time.time() - debut) * 1000) # temps de lecture 
            self.index_mot = self.index_mot + 1 
            self.fenetre.after(max(0, duree_mot_ms - ecoule_ms), self.mot_suivant)
        else :
            self.phase_rappel()

# le rappel( donc la case apparaît 10s pour qu'on puissent écrire)
    def phase_rappel(self):
        self.texte.config(text="")
        self.consigne.config(text="Tapez les mots dans l'ordre puis appuyez sur Entrée")
        self.saisie.delete(0, tk.END)  # vide la case
        self.saisie.pack(pady=10)     # la réaffiche
        self.saisie.focus()     #pour le curseur qui valide
        self.minuteur = self.fenetre.after(duree_rappel_ms, self.valider)   # en 10s : ça valide 

# pour enregistrer les réponses ->
    def valider(self):
        if self.minuteur is None:
            return                                   
        self.fenetre.after_cancel(self.minuteur)  # pour annuler le compte à rebours
        self.minuteur = None
        liste = self.listes[self.index_liste]
        self.participant.ajouter_reponse(liste, self.index_liste + 1, self.saisie.get())
        self.saisie.pack_forget()    # cache la case
        self.consigne.config(text="")   # écran blanc
        self.index_liste = self.index_liste + 1  # jça passe à la liste suivante
        self.fenetre.after(pause_ms, self.liste_suivante) # dans une pause de 3 s

# enregistrer dans le cvs ->
    def fin(self):
        self.experience.enregistrer(self.participant)
        self.texte.config(text="Merci !", font=("Arial", 36)) # pour dire merci à la fin 
        self.consigne.config(text="L'expérience est terminée. Vous pouvez fermer la fenêtre.")   


# le lancement = pour exécuter le fichier de code 
if __name__ == "__main__":
    fenetre = tk.Tk()  # crée la fenêtre
    Application(fenetre) # mets mon application dedans
    fenetre.mainloop()  # laisse la fenêtre tourner jusqu'à ce qu'on la ferme

# FIN
