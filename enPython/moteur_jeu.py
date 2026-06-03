import random

class MoteurJeu :
    def __init__(self) :
        self.dictionnaire = []
        self.mot_courant = ""
        self.score = 0
        self.tentatives_totales = 0
        self.bonnes_reponses = 0
        self.mots_restants = 0
        self.temps_restant = 0
        self.temps_max = 150
        self.charger_dictionnaire()
    
    def charger_dictionnaire(self) :
        with open("exemple.lettre" , "r" , encoding="utf-8") as fichier :
            contenu = fichier.read()
            self.dictionnaire = contenu.split()
    
    def generer_mot(self , mode) :
        if mode == "Lettres" :
            return random.choice(self.dictionnaire)
        elif mode == "Chiffres" :
            return str(random.randint(1 , 32767))
        else :
            if random.choice([True , False]) :
                return random.choice(self.dictionnaire)
            return str(random.randint(1 , 32767))
    
    def demarrer_partie(self , difficulte , mode) :
        self.score = 0
        self.tentatives_totales = 10
        self.bonnes_reponses = 0
        self.mots_restants = 10
        
        if "Facile" in difficulte :
            self.temps_max = 150
        elif "Normal" in difficulte :
            self.temps_max = 100
        else :
            self.temps_max = 50
        
        self.temps_restant = self.temps_max
        self.mot_courant = self.generer_mot(mode)
    
    def verifier_mot(self , saisie) :
        if saisie.strip() == self.mot_courant.strip() :
            self.bonnes_reponses += 1
            self.score += 1
            self.mots_restants -= 1
            return True
        return False
    
    def mot_suivant(self , mode) :
        self.mot_courant = self.generer_mot(mode)
    
    def partie_finie(self) :
        return self.mots_restants <= 0
    
    def obtenir_precision(self) :
        if self.tentatives_totales == 0 :
            return 0
        return (self.bonnes_reponses * 100) // self.tentatives_totales
