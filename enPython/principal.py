import tkinter as tk
from tkinter import messagebox
from moteur_jeu import MoteurJeu

class AppJeu :
    def __init__(self , fenetre) :
        self.fenetre = fenetre
        self.fenetre.title("Jeu de Frappe")
        self.fenetre.geometry("500x380")
        self.moteur = MoteurJeu()
        self.jeu_actif = False
        self.minuteur_id = None
        self.creer_interface()
    
    def creer_interface(self) :
        titre = tk.Label(self.fenetre , text="Jeu de Frappe" , font=("Arial" , 20 , "bold"))
        titre.pack(pady=10)
        
        frame_options = tk.Frame(self.fenetre)
        frame_options.pack(pady=10)
        
        tk.Label(frame_options , text="difficulite  :").pack(side=tk.LEFT , padx=5)
        self.difficulte = tk.StringVar(value="Facile (15s)")
        tk.OptionMenu(frame_options , self.difficulte , "Facile (15s)" , "Normal (100s)" , "Difficile (50s)").pack(side=tk.LEFT , padx=5)
        
        tk.Label(frame_options , text="Mode  :").pack(side=tk.LEFT , padx=5)
        self.mode = tk.StringVar(value="Lettres")
        tk.OptionMenu(frame_options , self.mode , "Lettres" , "Chiffres" , "Melange").pack(side=tk.LEFT , padx=5)
        
        self.label_mot = tk.Label(self.fenetre , text="Cliquez sur Demarrer" , font=("Courier" , 28 , "bold") , fg="blue" , pady=15)
        self.label_mot.pack()
        
        self.saisie = tk.Entry(self.fenetre , font=("Courier" , 14) , width=30)
        self.saisie.pack(pady=10)
        self.saisie.config(state=tk.DISABLED)
        self.saisie.bind("<KeyRelease>" , lambda e : self.verifier_saisie())
        
        self.barre = tk.Scale(self.fenetre , from_=0 , to=100 , orient=tk.HORIZONTAL)
        self.barre.pack(pady=10 , fill=tk.X , padx=20)
        
        frame_stats = tk.Frame(self.fenetre)
        frame_stats.pack(pady=10)
        
        self.label_temps = tk.Label(frame_stats , text="Temps  : 0s")
        self.label_temps.pack(side=tk.LEFT , padx=10)
        
        self.label_score = tk.Label(frame_stats , text="Score  : 0/10")
        self.label_score.pack(side=tk.LEFT , padx=10)
        
        self.label_precision = tk.Label(frame_stats , text="Précision  : 0%")
        self.label_precision.pack(side=tk.LEFT , padx=10)
        
        self.bouton_demarrer = tk.Button(self.fenetre , text="Demarrer" , font=("Arial" , 12 , "bold") , bg="#4CAF50" , fg="white" , command=self.demarrer_partie)
        self.bouton_demarrer.pack(pady=10)
    
    def demarrer_partie(self) :
        self.moteur.demarrer_partie(self.difficulte.get() , self.mode.get())
        self.jeu_actif = True
        
        self.saisie.config(state=tk.NORMAL)
        self.saisie.delete(0 , tk.END)
        self.saisie.focus()
        self.bouton_demarrer.config(state=tk.DISABLED)
        
        self.label_mot.config(text=self.moteur.mot_courant)
        self.label_score.config(text="Score  : 0/10")
        self.label_temps.config(text=f"Temps  : {self.moteur.temps_restant}s")
        self.barre.config(state=tk.NORMAL)
        self.barre.set(100)
        self.decremente_temps()
    
    def verifier_saisie(self) :
        if not self.jeu_actif :
            return
        
        saisie_text = self.saisie.get()
        if self.moteur.verifier_mot(saisie_text) :
            self.saisie.delete(0 , tk.END)
            self.label_score.config(text=f"Score  : {self.moteur.score}/10")
            if self.moteur.partie_finie() :
                self.jeu_actif = False
                if self.minuteur_id :
                    self.fenetre.after_cancel(self.minuteur_id)
                self.afficher_resultats()
            else :
                self.moteur.mot_suivant(self.mode.get())
                self.label_mot.config(text=self.moteur.mot_courant)
    
    def decremente_temps(self) :
        if not self.jeu_actif :
            return
        
        self.moteur.temps_restant -= 1
        self.label_temps.config(text=f"Temps  : {self.moteur.temps_restant}s")
        pourcentage = (self.moteur.temps_restant * 100) // self.moteur.temps_max
        self.barre.set(max(0 , pourcentage))
        
        if self.moteur.temps_restant <= 0 :
            self.jeu_actif = False
            self.afficher_resultats()
        else :
            self.minuteur_id = self.fenetre.after(1000 , self.decremente_temps)
    
    def afficher_resultats(self) :
        self.saisie.config(state=tk.DISABLED)
        self.bouton_demarrer.config(state=tk.NORMAL)
        self.barre.config(state=tk.DISABLED)
        precision = self.moteur.obtenir_precision()
        self.label_precision.config(text=f"Précision  : {precision}%")
        messagebox.showinfo("Resultats" , f"Score  : {self.moteur.score}/10\nPrecision  : {precision}%")

root = tk.Tk()
app = AppJeu(root)
root.mainloop()