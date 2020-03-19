#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 09:08:49 2020

@author: MOsmoz_
"""

from tkinter import * #Bibliothèque du GUI
import tkinter.messagebox #Permet d'afficher le résultat
import copy #Pour copier les grilles afin de les modifier dans différentes profondeur sans changer l'originale
from random import choice #Permet d'insérer de l'aléatoire dans le choix de l'IA

class Joueur:
    def __init__(self,pseudo, estuneIA, numJoueur):#Initialisation des joueurs avec leur numéro, leur pseudo, et estuneIA est True si c'est une IA et false sinon
        self.pseudo=pseudo
        self.estuneIA=estuneIA
        self.numJoueur=numJoueur
        
    def getitem(self, coord):#Permet de récupérer les infos dans le Main
        if (coord=='pseudo'):
            return self.pseudo
        elif (coord=='estuneIA'):
            return self.estuneIA
        elif (coord=='numJoueur'):
            return self.numJoueur
    
    def Joue(self,grille, modeJeu, niveau):#Début du tour de l'IA, appelé AlphaBetaSearch dans le TD
        grillenv=copy.deepcopy(grille)#On crée une nouvelle matrice pour ne pas modifier l'originale dans nos test à venir dans le min max
        score,  actionfinal, prof= self.MaxValue(grillenv, modeJeu, -5000, 5000, 1, niveau)#score et prof ne sont pas utilie ici mais le sont lorsque Min et Max s'appellent entre eux
        return self.Result(grille, actionfinal, self.numJoueur), actionfinal#On retourne la grille modifiée avec l'action finale

    def MinValue(self,grille, modeJeu, a, b, prof, niveau):#On considère ici que c'est l'adversaire qui joue, donc qu'il va choisir l'action la plus néfaste pour nous (qui à un score/utility la plus faible)
        gagnant = self.TerminalTest(grille, modeJeu)#On test si c'est la fin du jeu (gagnany = -1 : contine / = 0 égalité finie / = numJoueur C'est le joueur actuel qui gagne / = (numJoueur%2)+1 C'est l'adversaire qui gagne)
        if(gagnant >=0):
            return self.Utility(gagnant), [0,0], prof #Retourne une valeur selon le gagnant : 0 si égalité, 1 si joueur actuel gagne, -1 si il perd
        elif(prof >= niveau):#Si on arrive a une profondeur de 2 au Puissance 4,on établit dès maintenant une estimation de qui est en train de gagner (car sinon il y a trop de récureences)
            return self.Etatjeu(grille, modeJeu), [0,0], prof
        else:
            scoreMin = 5000#valeur arbitraire qui va être changée dès la première occurence (+infin dans l'énoncé)
            profmin = -100#Idem
            actionspossibles = self.Action(grille, modeJeu)#On liste les actions pouvant être jouée
            for i in range(len(actionspossibles)):#pour chacun de ces actions
                grillenv=copy.deepcopy(grille)#On crée une nouvelle grille pour ne pas modifier l'originale
                grillenv[:]=list(self.Result(grillenv, actionspossibles[i], ((self.numJoueur%2)+1)))#On lui applique l'action
                score, action, profcoupwin = self.MaxValue(grillenv, modeJeu, a, b, prof+1, niveau)#On regarde le score de l'action que va choisir max selon notre action
                if (score<scoreMin or (score==scoreMin and profcoupwin>profmin)):#Si ce score est plus petit que le plus néfaste actuellement stockée dans scoreMin, alors il est mieux et on le choisi
                    profmin = profcoupwin
                    scoreMin = score
                    choix = i
                if(scoreMin<a):#Si il est déja plus petit que alpha, pas besoin de continuer sur cette branche (élagage)
                    return scoreMin, actionspossibles[i], prof
                if (scoreMin<b):#Sinon on remplace beta
                    b = scoreMin
            return (scoreMin, actionspossibles[choix], prof)
    
    def MaxValue(self,grille, modeJeu, a, b, prof, niveau):#Idem que MIN VALUE
        gagnant = self.TerminalTest(grille, modeJeu)
        if(gagnant >=0):
            return self.Utility(gagnant), [0,0], prof
        elif(prof >= niveau):#Si on arrive a une profondeur de 2 au Puissance 4,on établit dès maintenant une estimation de qui est en train de gagner (car sinon il y a trop de récureences)
            return self.Etatjeu(grille, modeJeu), [0,0], prof
        else:
            scoreMax = -5000
            profmin = 100
            actionspossibles = self.Action(grille, modeJeu)
            for i in range(len(actionspossibles)):
                grillenv=copy.deepcopy(grille)
                grillenv[:]=list(self.Result(grillenv, actionspossibles[i], self.numJoueur))
                if prof==1: #Au choix final, si il y a plusieurs possibilités équivalentes, on choisir aléatoirement entre celles-ci
                    random = choice([1,2,3,4])
                score, action, profcoupwin = self.MinValue(grillenv, modeJeu, a, b, prof+1, niveau)
                if (score>scoreMax or (score==scoreMax and profcoupwin<profmin)or (score != -1 and score==scoreMax and profcoupwin == profmin and prof == 1 and random==1)):
                    profmin = profcoupwin
                    scoreMax = score
                    choix = i
                if(scoreMax>b):
                    return scoreMax, actionspossibles[i], prof
                if(scoreMax> a):
                    a = scoreMax
            return (scoreMax, actionspossibles[choix], prof)
        
    def Action(self,grille, modeJeu): #Va lister les actions que l'IA peut réaliser
        actionspossibles = [] #On intancie une liste vide qui va stocker les coordonnées de la grille dont la valeur est égale à 0
        
        if (modeJeu==1):
            for i in range(len(grille)):
                for j in range(len(grille[i])):#On parcourt toutes les cases
                    if(grille[i][j]==0):#On ajoute au tableau si c'est égal à zéro
                        actionspossibles.append([i,j])
        else:
            for j in range(len(grille[0])):
                caseremplie = False
                for i in range(len(grille)):#On parcourt toutes les cases
                    if (grille[i][j]!=0 and caseremplie==False):
                        actionspossibles.append([i-1,j])
                        caseremplie = True
                    elif(i == len(grille)-1 and caseremplie==False):
                        actionspossibles.append([i,j])
                        caseremplie = True
                        
        return actionspossibles

            
    def Result(self, grille, action, numJoueur):#Va appliquer l'action à la grille (action est une liste avec les deux coordonnés puis la valeur)
        grillenv=copy.deepcopy(grille)
        grillenv[action[0]][action[1]]= numJoueur
        return grillenv
    
    def TerminalTest(self, grille, modeJeu):#Test si c'est la fin du jeu, et qui a gagné
        
        if (modeJeu == 2):
            nombrepourgagner = 4
        else:
            nombrepourgagner = 3
        
        gagnant = 0#Retourne 0 si la table est complete sans gagnant, -1 si le jeu continue, 1 si le joueur 1 a gagné, 2 si le joueur 2 a gagné
        for i in range(len(grille)):
            for j in range(len(grille[i])):#On parcourt toutes les cases
                if(grille[i][j]==0):#Si une case est égalse à zéro, cela n'est pas fini
                    gagnant = -1
        
        #Check si gagner par lignes
        for i in range(len(grille)):
            for j in range(len(grille[i])-nombrepourgagner+1):#On parcourt toutes les cases
                if(grille[i][j]==self.numJoueur and grille[i][j+1]==self.numJoueur and grille[i][j+2]==self.numJoueur):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    if(modeJeu == 2):
                        if(grille[i][j+3]==self.numJoueur):
                            gagnant = self.numJoueur
                    else:
                        gagnant = self.numJoueur
                elif(grille[i][j]==((self.numJoueur%2)+1) and grille[i][j+1]==((self.numJoueur%2)+1) and grille[i][j+2]==((self.numJoueur%2)+1)):
                    if(modeJeu == 2):
                        if(grille[i][j+3]==((self.numJoueur%2)+1)):
                            gagnant = ((self.numJoueur%2)+1)
                    else:
                        gagnant = ((self.numJoueur%2)+1)
         
        #Check si gagner par colonne
        for i in range(len(grille)-nombrepourgagner+1):
            for j in range(len(grille[i])):#On parcourt toutes les cases
                if(grille[i][j]==self.numJoueur and grille[i+1][j]==self.numJoueur and grille[i+2][j]==self.numJoueur):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    if(modeJeu == 2):
                        if(grille[i+3][j]==self.numJoueur):
                            gagnant = self.numJoueur
                    else:
                        gagnant = self.numJoueur
                elif(grille[i][j]==((self.numJoueur%2)+1) and grille[i+1][j]==((self.numJoueur%2)+1) and grille[i+2][j]==((self.numJoueur%2)+1)):
                    if(modeJeu == 2):
                        if(grille[i+3][j]==((self.numJoueur%2)+1)):
                            gagnant = ((self.numJoueur%2)+1)
                    else:
                        gagnant = ((self.numJoueur%2)+1)
                        
        #Check si gagnant par diagonale descendante
        for i in range(len(grille)-nombrepourgagner+1):
            for j in range(len(grille[i])-nombrepourgagner+1):#On parcourt toutes les cases
                if(grille[i][j]==self.numJoueur and grille[i+1][j+1]==self.numJoueur and grille[i+2][j+2]==self.numJoueur):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    if(modeJeu == 2):
                        if(grille[i+3][j+3]==self.numJoueur):
                            gagnant = self.numJoueur
                    else:
                        gagnant = self.numJoueur
                elif(grille[i][j]==((self.numJoueur%2)+1) and grille[i+1][j+1]==((self.numJoueur%2)+1) and grille[i+2][j+2]==((self.numJoueur%2)+1)):
                    if(modeJeu == 2):
                        if(grille[i+3][j+3]==((self.numJoueur%2)+1)):
                            gagnant = ((self.numJoueur%2)+1)
                    else:
                        gagnant = ((self.numJoueur%2)+1)
        
        #Check si gagnant par diagonale montante
        for i in range(nombrepourgagner-1,len(grille)):
            for j in range(len(grille[i])-nombrepourgagner+1):#On parcourt toutes les cases
                if(grille[i][j]==self.numJoueur and grille[i-1][j+1]==self.numJoueur and grille[i-2][j+2]==self.numJoueur):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    if(modeJeu == 2):
                        if(grille[i-3][j+3]==self.numJoueur):
                            gagnant = self.numJoueur
                    else:
                        gagnant = self.numJoueur
                elif(grille[i][j]==((self.numJoueur%2)+1) and grille[i-1][j+1]==((self.numJoueur%2)+1) and grille[i-2][j+2]==((self.numJoueur%2)+1)):
                    if(modeJeu == 2):
                        if(grille[i-3][j+3]==((self.numJoueur%2)+1)):
                            gagnant = ((self.numJoueur%2)+1)
                    else:
                        gagnant = ((self.numJoueur%2)+1)
        
        return gagnant
    
    def Etatjeu(self, grille, modeJeu):#Test si c'est la fin du jeu, et qui a gagné
        
        if (modeJeu == 2):
            nombrepourgagner = 4
        else:
            nombrepourgagner = 3
        
        score = 0#Retourne 0 si la table est complete sans gagnant, -1 si le jeu continue, 1 si le joueur 1 a gagné, 2 si le joueur 2 a gagné
        selfpion = 0
        pionautre = 0
        
        #Check si gagner par lignes
        for i in range(len(grille)):
            for j in range(len(grille[i])-nombrepourgagner+1):#On parcourt toutes les cases
                if(grille[i][j]==self.numJoueur):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    selfpion = selfpion+1
                    for k in range(1,3):
                        if grille[i][j+k]==self.numJoueur:
                            selfpion = selfpion+1
                        elif grille[i][j+k]==(self.numJoueur%2)+1:
                            pionautre = pionautre + 1
                    if (modeJeu==2):
                        if grille[i][j+3]==self.numJoueur:
                            selfpion = selfpion+1
                        elif grille[i][j+3]==(self.numJoueur%2)+1:
                            pionautre = pionautre + 1
                    
                    if pionautre==0:
                        if(selfpion==1):
                            score = score + 10
                        elif (selfpion==2):
                            score = score + 30
                        elif (selfpion==3 and modeJeu == 2):
                            score = score + 60
                            
                elif(grille[i][j]==(self.numJoueur%2)+1):
                    pionautre = pionautre + 1
                    for k in range(1,3):
                        if grille[i][j+k]==self.numJoueur:
                            selfpion = selfpion+1
                        elif grille[i][j+k]==(self.numJoueur%2)+1:
                            pionautre = pionautre + 1
                    if (modeJeu==2):
                        if grille[i][j+3]==self.numJoueur:
                            selfpion = selfpion+1
                        elif grille[i][j+3]==(self.numJoueur%2)+1:
                            pionautre = pionautre + 1
                    
                    if selfpion==0:
                        if(pionautre==1):
                            score = score - 10
                        elif (pionautre==2):
                            score = score - 30
                        elif (pionautre==3 and modeJeu == 2):
                            score = score - 60


        #Check si gagner par colonne
        for i in range(len(grille)-nombrepourgagner+1):
            for j in range(len(grille[i])):#On parcourt toutes les cases
                if(grille[i][j]==self.numJoueur):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    selfpion = selfpion+1
                    for k in range(1,3):
                        if grille[i+k][j]==self.numJoueur:
                            selfpion = selfpion+1
                        elif grille[i+k][j]==(self.numJoueur%2)+1:
                            pionautre = pionautre + 1
                    if (modeJeu==2):
                        if grille[i+3][j]==self.numJoueur:
                            selfpion = selfpion+1
                        elif grille[i+3][j]==(self.numJoueur%2)+1:
                            pionautre = pionautre + 1
                    
                    if pionautre==0:
                        if(selfpion==1):
                            score = score + 10
                        elif (selfpion==2):
                            score = score + 30
                        elif (selfpion==3 and modeJeu == 2):
                            score = score + 60
                
                elif(grille[i][j]==(self.numJoueur%2)+1):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    pionautre = pionautre + 1
                    for k in range(1,3):
                        if grille[i+k][j]==self.numJoueur:
                            selfpion = selfpion+1
                        elif grille[i+k][j]==(self.numJoueur%2)+1:
                            pionautre = pionautre + 1
                    if (modeJeu==2):
                        if grille[i+3][j]==self.numJoueur:
                            selfpion = selfpion+1
                        elif grille[i+3][j]==(self.numJoueur%2)+1:
                            pionautre = pionautre + 1
                    
                    if selfpion==0:
                        if(pionautre==1):
                            score = score - 10
                        elif (pionautre==2):
                            score = score - 30
                        elif (pionautre==3 and modeJeu == 2):
                            score = score - 60

                        
        #Check si gagnant par diagonale descendante
        for i in range(len(grille)-nombrepourgagner+1):
            for j in range(len(grille[i])-nombrepourgagner+1):#On parcourt toutes les cases
                if(grille[i][j]==self.numJoueur):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    selfpion = selfpion+1
                    for k in range(1,3):
                        if grille[i+k][j+k]==self.numJoueur:
                            selfpion = selfpion+1
                        elif grille[i+k][j+k]==(self.numJoueur%2)+1:
                            pionautre = pionautre + 1
                    if (modeJeu==2):
                        if grille[i+3][j+3]==self.numJoueur:
                            selfpion = selfpion+1
                        elif grille[i+3][j+3]==(self.numJoueur%2)+1:
                            pionautre = pionautre + 1
                    
                    if pionautre==0:
                        if(selfpion==1):
                            score = score + 10
                        elif (selfpion==2):
                            score = score + 30
                        elif (selfpion==3 and modeJeu == 2):
                            score = score + 60
                
                elif(grille[i][j]==(self.numJoueur%2)+1):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    pionautre = pionautre + 1
                    for k in range(1,3):
                        if grille[i+k][j+k]==self.numJoueur:
                            selfpion = selfpion+1
                        elif grille[i+k][j+k]==(self.numJoueur%2)+1:
                            pionautre = pionautre + 1
                    if (modeJeu==2):
                        if grille[i+3][j+3]==self.numJoueur:
                            selfpion = selfpion+1
                        elif grille[i+3][j+3]==(self.numJoueur%2)+1:
                            pionautre = pionautre + 1
                    
                    if selfpion==0:
                        if(pionautre==1):
                            score = score - 10
                        elif (pionautre==2):
                            score = score - 30
                        elif (pionautre==3 and modeJeu == 2):
                            score = score - 60

        
        #Check si gagnant par diagonale montante
        for i in range(nombrepourgagner-1,len(grille)):
            for j in range(len(grille[i])-nombrepourgagner+1):#On parcourt toutes les cases
                if(grille[i][j]==self.numJoueur):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    selfpion = selfpion+1
                    for k in range(1,3):
                        if grille[i-k][j+k]==self.numJoueur:
                            selfpion = selfpion+1
                        elif grille[i-k][j+k]==(self.numJoueur%2)+1:
                            pionautre = pionautre + 1
                    if (modeJeu==2):
                        if grille[i-3][j+3]==self.numJoueur:
                            selfpion = selfpion+1
                        elif grille[i-3][j+3]==(self.numJoueur%2)+1:
                            pionautre = pionautre + 1
                    
                    if pionautre==0:
                        if(selfpion==1):
                            score = score + 10
                        elif (selfpion==2):
                            score = score + 30
                        elif (selfpion==3 and modeJeu == 2):
                            score = score + 60
                
                elif(grille[i][j]==(self.numJoueur%2)+1):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    pionautre = pionautre + 1
                    for k in range(1,3):
                        if grille[i-k][j+k]==self.numJoueur:
                            selfpion = selfpion+1
                        elif grille[i-k][j+k]==(self.numJoueur%2)+1:
                            pionautre = pionautre + 1
                    if (modeJeu==2):
                        if grille[i-3][j+3]==self.numJoueur:
                            selfpion = selfpion+1
                        elif grille[i-3][j+3]==(self.numJoueur%2)+1:
                            pionautre = pionautre + 1
                    
                    if selfpion==0:
                        if(pionautre==1):
                            score = score - 10
                        elif (pionautre==2):
                            score = score - 30
                        elif (pionautre==3 and modeJeu == 2):
                            score = score - 60
        
        return score
        
    def Utility(self,gagnant):#On récupère le gagnant grâce à Terminal
        if(gagnant==0):#Cette valeur est retournée si il y a égalitée
            valeur = 0
        elif(gagnant==self.numJoueur):
            valeur = 5000
        elif(gagnant==((self.numJoueur%2)+1)):
            valeur = -5000
        return valeur
        
            
def AfficherGrille(grille):#Simple méthode pour afficher esthétiquement la grille
    print("\n -----------")
    for i in range(len(grille)):
        print("| ",end='')
        for j in range(len(grille[i])):
            if(grille[i][j] == 1):
                print("X | ",end='')
            elif(grille[i][j] == 2):
                print("O | ",end='')
            else:
                print("  | ",end='')
        print("\n -----------")

if __name__== '__main__':
    
    tk2 =Tk() #on initialise une premiere fenetre qui nous permettra de prendre les infos sur les joueurs, le jeu, la difficulté etc
    p1 = StringVar()#variables pour le pseudo des joueurs
    p2 = StringVar()
    tourjoueur = True# variable qui permet de savoir a qui est le tour
    Joueurs = []# tableau de classe
    n=0
    gagnant = -1    
    estuneIA = False    # booleen qui nous permet de savoir si un joueur un est une IA ou non
    modeJeu=1   # le mode de Jeu
    niveau1=3    # le niveau de diff
    niveau2=3 
    #cette partie crée les boxes dans lesquelles on peut rentrer les pseudos des joueurs
    player1_name = Entry(tk2, textvariable=p1, bd=5)
    player1_name.grid(row=1, column=1, columnspan=8)    # .grid permet de faire l'affichage selon un quadrillage prédéfini par Tkinter
    player2_name = Entry(tk2, textvariable=p2, bd=5)
    player2_name.grid(row=2, column=1, columnspan=8)
    
    
   

    buttons = StringVar() #la variable buttons qui sera utilisé lorsqu'un bouton est utilisé

    #ici on affiche les 2 textes Player 1 et 2 avec des couleurs, polices et dimensions précises.
    label = Label( tk2, text="Player 1:", font='Helvetica 20 bold', bg='white', fg='black', height=1, width=8,)
    label.grid(row=1, column=0)
    
    label = Label( tk2, text="Player 2:", font='Helvetica 20 bold', bg='white', fg='black', height=1, width=8)
    label.grid(row=2, column=0) 
  
    #ici on crée une selection, ou l'on peut choisir si le joueur est une IA, il suffit de cliquer pour cocher la case
    var1 = IntVar()
    checkIA1 = Checkbutton(tk2, text="Player 1 is an AI", variable=var1)
    checkIA1.grid(row=1, column=12)
    var1.get()
    
    #ici on fait la meme chose mais avec le 2eme joueur
    var2 = IntVar()
    checkIA2 = Checkbutton(tk2, text="Player 2 is an AI", variable=var2)
    checkIA2.grid(row=2, column=12)
    var2.get()
    
    # ici on va crée une liste de selection, cad que le joueur peut choisir entre Tic tac toe et Connect 4, la valeur par défaut est Tic tac toe
    variable = StringVar(tk2)
    variable.set("Tic Tac Toe") # default value  
    w = OptionMenu(tk2, variable, "Tic Tac Toe", "Connect 4")
    w.grid(row=4, column=3, columnspan=6)
    
    # pareil ici avec le niveau de difficulté
    variable2 = StringVar(tk2)
    variable2.set("Beginner") # default value  
    w2 = OptionMenu(tk2, variable2, "Beginner", "Medium", "Hardcore")
    w2.grid(row=1, column=13, columnspan=8)
    
    # pareil ici avec le niveau de difficulté
    variable3 = StringVar(tk2)
    variable3.set("Beginner") # default value  
    w3 = OptionMenu(tk2, variable3, "Beginner", "Medium", "Hardcore")
    w3.grid(row=2, column=13, columnspan=8)
    
    
    
    #le boutton lance la grille du jeu choisi, attention le bouton verrouille vos choix
    button_play = Button(tk2, text='Play', font='Times 20 bold', command = lambda: jeu())
    button_play.grid(row=6, column=3, columnspan=6)
    

    #le bouton play lance cette méthode
    def jeu():
        global grille, estuneIA, modeJeu, niveau1, niveau2
        button_play.configure(state=DISABLED)
        #global permet de récupérer les valeurs initialisées précédemment
        #on va mettre tout les butons en DISABLED, on ne peut plus les utiliser
        checkIA1.configure(state=DISABLED)
        var2.get()
        #.get() permet de prendre la valeur de la case, 0 si elle n'est pas cochée, 1 autrement
        checkIA2.configure(state=DISABLED)
        p1.get()
        # on récupere le pseudo du J1
        player1_name.configure(state=DISABLED)
        p2.get()        
        player2_name.configure(state=DISABLED)
        variable.get()
        #on récupère le nom du jeu 
        w.configure(state=DISABLED)
        variable2.get()
        w2.configure(state=DISABLED)
        variable3.get()
        w3.configure(state=DISABLED)
        
     
        #on crée une nouvelle fenetre
        tk = Tk()
        tk.title("Tic Tac Toe/ Connect 4")
        
        
        
        
        #selon le choix de la case cochée ou non, on initialise les joueurs comme étant une IA ou non
        if (var1.get()==0):
            J1=Joueur(p1.get(),estuneIA,1)
            #p1.get() est le pseudo du joueur 1
            Joueurs.append(J1)
        elif(var1.get()==1):
            estuneIA= True
            J1=Joueur(p1.get(),estuneIA,1)    
            Joueurs.append(J1)
            
            
            
        if(var2.get()==0):
            estuneIA= False
            J2=Joueur(p2.get(),estuneIA,2)
            Joueurs.append(J2)
        elif(var2.get()==1):
            estuneIA= True
            J2=Joueur(p2.get(),estuneIA,2)
            Joueurs.append(J2)
       
        
        #on définit le mode de jeu, et la taille de la grille correspondante
        if(variable.get()=='Tic Tac Toe'):
            modeJeu=1
        else:
            modeJeu=2
        
        if(modeJeu==1):
            taillegrillex = 3
            taillegrilley = 3
        else:
            taillegrillex = 7
            taillegrilley = 6
            
        #on définit chacun des niveaux des IAs  
        if(variable2.get()=='Hardcore'):
            if(modeJeu==1):
                niveau1=9
            else:
                niveau1=7
        elif(variable2.get()=='Medium'):
            if(modeJeu==1):
                niveau1=6
            else:
                niveau1=5
                
        if(variable3.get()=='Hardcore'):
            if(modeJeu==1):
                niveau2=9
            else:
                niveau2=7
        elif(variable3.get()=='Medium'):
            if(modeJeu==1):
                niveau2=6
            else:
                niveau2=5
         
            
            
        #Initialisation des taille du jeu MORPION
        #On crée la grille de départ, valable pour n'importe quel jeu avec une grille
        grille = [[0 for j in range(taillegrillex)] for i in range(taillegrilley)]
        
        #On affiche l'état de la grille
        AfficherGrille(grille)
            
            

            
        # on désactive les boutons IA
        def disableIAbutton():        
            buttonIA.configure(state=DISABLED)
        
        # les boutons sur lesquelles on a pas cliquer ne seront pas affichés grace a cette méthode
        def AffichepasbuttononUsed(button):
            if (button['text']=='X' or button['text']=='O'):
                button['disabledforeground']='white'
            else:
                button['disabledforeground']='gray'

        # on désactive tous les boutons
        def finaldisableAllButton():  
            for i in range (len(Allbuttons)):
                Allbuttons[i].configure(state=DISABLED)
                AffichepasbuttononUsed(Allbuttons[i])
            
         
            
        #on réactive tous les boutons IA
        def EnableIAButton():        
            buttonIA.configure(state=NORMAL)
            
        #on fait en sorte que les boutons deja utilisés reste affichés   
        def BoutonUsedstayused(button):
            if (button['text']=='X' or button['text']=='O'):
                button.configure(state=DISABLED)
                button['disabledforeground']='white'
                
        #on réactive tous les boutons         
        def EnableAllButton():        
            for i in range (len(Allbuttons)):
                Allbuttons[i].configure(state=NORMAL)
                BoutonUsedstayused(Allbuttons[i])
            
        #on désactive un bouton   
        def disableButton(buttons):
            buttons.configure(state=DISABLED)
    
        #on modifie la valeur d'u bouton a partir de la grille et de ses coords
        def ModifieOnlyButton(coord, tourjoueur):            
            if(modeJeu==1):
                numerobutton=coord[1]+coord[0]*3 + 1
            elif(modeJeu==2):
                numerobutton=coord[1]+coord[0]*7 + 1
            return numerobutton
    
        #on modifie la valeur d'u bouton a partir de la grille et de ses coords
        #on modifie aussi la valeur de ce bouton
        def ModifieButton(coord, tourjoueur):            
            if(modeJeu==1):
                numerobutton=coord[1]+coord[0]*3 + 1
            elif(modeJeu==2):
                numerobutton=coord[1]+coord[0]*7 + 1
            
            Allbuttons[numerobutton-1]['text']='X' if (tourjoueur== True) else 'O'
            Allbuttons[numerobutton-1]['fg']='white'
            Allbuttons[numerobutton-1]['disabledforeground']='white'
    
        # on definit ici ce qu'il se passe lorsque l'on appuie sur un bouton
        def btnClickIA(buttons):
            global tourjoueur, modeJeu, estuneIA, grille, Joueurs,niveau1, niveau2
            
            #il faut que le joueur est une IA et que ce soit a son tour
            if(Joueurs[0].estuneIA == True and tourjoueur==True):
                #on récupère les coord de la case jouée par l'IA
                grille, coord = Joueurs[0].Joue(grille, modeJeu, niveau1)
                #on modifie nos boutons a l'aide des coords
                ModifieButton(coord, tourjoueur)
                #on change le tour
                tourjoueur = False
                #on réafiche la grille
                AfficherGrille(grille)
                
                #ce qui suit est a faire que quand le J2 est un vrai joueur
                if (Joueurs[1].estuneIA == False):
                    #on désactive les boutons IA pour éviter que l'on puisse la faire jouer tout seule
                    EnableAllButton()
                    #on active les boutons du vrai Joueurs
                    disableIAbutton()
               
    
            elif(Joueurs[1].estuneIA == True and tourjoueur==False):
                #meme case mais pour le joueur 2
                grille, coord = Joueurs[1].Joue(grille, modeJeu, niveau2)
                
                ModifieButton(coord, tourjoueur)
                tourjoueur = True
                AfficherGrille(grille)
                
                if (Joueurs[0].estuneIA == False):
                    EnableAllButton()
                    disableIAbutton()
            
            # ces cas permettent d'afficher un message dans le cas d'une fin de partie
            if (J1.TerminalTest(grille, modeJeu)==1):
                #on désactive tous les boutons
                finaldisableAllButton()
                #on affiche le message dans une fenetre Tkinter avec le nom du gagnant
                tkinter.messagebox.showinfo("Tic-Tac-Toe", J1.pseudo + " wins.") 
                
            elif (J2.TerminalTest(grille, modeJeu)==2):
                finaldisableAllButton()
                tkinter.messagebox.showinfo("Tic-Tac-Toe", J2.pseudo + " wins.")
                
            elif (J2.TerminalTest(grille, modeJeu)==0):
                finaldisableAllButton()
                tkinter.messagebox.showinfo("Tic-Tac-Toe", 'There is a Tie.')
    
    
    
        def btnClick(buttons):
            global tourjoueur, modeJeu, estuneIA, grille
            #le cas d'un bouton si le joueur est humain
            #on récupère la valeur du bouton
            couple =str(buttons['text'])
            #on met ses valeurs sous la forme d'une liste
            listcouppossible = [int(couple[0]),int(couple[1])]
            
            #dans le cas du puissance 4, cette méthode modélise la gravité
            #
            if (tourjoueur==True and modeJeu==2):
                for i in range (len(Joueurs[0].Action(grille, modeJeu))):
                    if (Joueurs[0].Action(grille, modeJeu)[i][1]==listcouppossible[1]):
                        listcouppossible=Joueurs[0].Action(grille, modeJeu)[i]
                        buttons = Allbuttons[ModifieOnlyButton(listcouppossible, tourjoueur)-1]
            elif(tourjoueur==False and modeJeu==2): 
                for i in range (len(Joueurs[1].Action(grille, modeJeu))):
                    if (Joueurs[1].Action(grille, modeJeu)[i][1]==listcouppossible[1]):
                        listcouppossible=Joueurs[1].Action(grille, modeJeu)[i]
                        buttons = Allbuttons[ModifieOnlyButton(listcouppossible, tourjoueur)-1]
                    
            
            
            if(grille[int(buttons['text'][0])][int(buttons['text'][1])]==0):
                
                if(tourjoueur==True and Joueurs[0].estuneIA == False and listcouppossible in Joueurs[0].Action(grille, modeJeu)):
                    grille[int(buttons['text'][0])][int(buttons['text'][1])]=1
                    AfficherGrille(grille)
                    tourjoueur = False
                    
                    buttons['text']='X'
                    buttons['fg']='white'                    
                    buttons['disabledforeground']='white'
                    disableButton(buttons)
                    
                    if (Joueurs[1].estuneIA == True):
                        finaldisableAllButton()
                        EnableIAButton()
                    
            
                elif(tourjoueur==False and Joueurs[1].estuneIA == False and listcouppossible in Joueurs[1].Action(grille, modeJeu)):
                    grille[int(buttons['text'][0])][int(buttons['text'][1])] = 2  
                    AfficherGrille(grille)            
                    tourjoueur = True
                
                    buttons['text']='O'
                    buttons['fg']='white'                    
                    buttons['disabledforeground']='white'
                    disableButton(buttons)
                    
                    if (Joueurs[0].estuneIA == True):
                        finaldisableAllButton()
                        EnableIAButton()
             
            
            
            
            
            if (J2.TerminalTest(grille, modeJeu)==2):
                finaldisableAllButton()
                tkinter.messagebox.showinfo("Tic-Tac-Toe", J2.pseudo + " wins.")
                
            elif (J2.TerminalTest(grille, modeJeu)==0):
                finaldisableAllButton()
                tkinter.messagebox.showinfo("Tic-Tac-Toe", 'There is a Tie.')
                
            elif (J1.TerminalTest(grille, modeJeu)==1):
                finaldisableAllButton()
                tkinter.messagebox.showinfo("Tic-Tac-Toe", J1.pseudo + " wins.")
                
            
 
        
        
        
        
        buttons = StringVar()

        buttonIA = Button(tk, text='IA', font='Times 20 bold', bg='gray', fg='black', activeforeground='gray',activebackground='gray', disabledforeground='black', command=lambda: btnClickIA(btnClickIA))
        buttonIA.grid(row=4, column=2)
        
        label = Label( tk, text="When it is the AI turn, press the button :", font='Helvetica 10 bold', bg='white', fg='black',anchor='w', height=1, width=32,)
        label.grid(row=4, column=0, columnspan=2)
        Allbuttons=[]
        
        
        if (modeJeu==1):
            Allbuttons.append(Button(tk, text='00', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=4, width=8, command=lambda: btnClick(Allbuttons[0])))
            Allbuttons.append(Button(tk, text='01', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=4, width=8, command=lambda: btnClick(Allbuttons[1])))   
            Allbuttons.append(Button(tk, text='02', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=4, width=8, command=lambda: btnClick(Allbuttons[2])))
            Allbuttons.append(Button(tk, text='10', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=4, width=8, command=lambda: btnClick(Allbuttons[3])))
            Allbuttons.append(Button(tk, text='11', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=4, width=8, command=lambda: btnClick(Allbuttons[4])))
            Allbuttons.append(Button(tk, text='12', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=4, width=8, command=lambda: btnClick(Allbuttons[5])))
            Allbuttons.append(Button(tk, text='20', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=4, width=8, command=lambda: btnClick(Allbuttons[6])))
            Allbuttons.append(Button(tk, text='21', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=4, width=8, command=lambda: btnClick(Allbuttons[7])))
            Allbuttons.append(Button(tk, text='22', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=4, width=8, command=lambda: btnClick(Allbuttons[8])))
            
            
            index=0
            for i in range (taillegrillex):   
                for j in range (taillegrilley): 
                   Allbuttons[index].grid(row=i+5, column=j)
                   index = index+1
            
        
        
        
        elif (modeJeu==2):
            Allbuttons.append(Button(tk, text='00', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[0])))
            Allbuttons.append(Button(tk, text='01', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[1])))   
            Allbuttons.append(Button(tk, text='02', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[2])))
            Allbuttons.append(Button(tk, text='03', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[3])))
            Allbuttons.append(Button(tk, text='04', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[4])))
            Allbuttons.append(Button(tk, text='05', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[5])))
            Allbuttons.append(Button(tk, text='06', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[6])))
            Allbuttons.append(Button(tk, text='10', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[7])))
            Allbuttons.append(Button(tk, text='11', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[8])))
            Allbuttons.append(Button(tk, text='12', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[9])))
            Allbuttons.append(Button(tk, text='13', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[10])))
            Allbuttons.append(Button(tk, text='14', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[11])))
            Allbuttons.append(Button(tk, text='15', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[12])))
            Allbuttons.append(Button(tk, text='16', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[13])))
            Allbuttons.append(Button(tk, text='20', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[14])))   
            Allbuttons.append(Button(tk, text='21', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[15])))
            Allbuttons.append(Button(tk, text='22', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[16])))
            Allbuttons.append(Button(tk, text='23', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[17])))
            Allbuttons.append(Button(tk, text='24', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[18])))
            Allbuttons.append(Button(tk, text='25', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[19])))
            Allbuttons.append(Button(tk, text='26', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[20])))
            Allbuttons.append(Button(tk, text='30', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[21])))   
            Allbuttons.append(Button(tk, text='31', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[22])))
            Allbuttons.append(Button(tk, text='32', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[23])))
            Allbuttons.append(Button(tk, text='33', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[24])))
            Allbuttons.append(Button(tk, text='34', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[25])))
            Allbuttons.append(Button(tk, text='35', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[26])))
            Allbuttons.append(Button(tk, text='36', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[27])))
            Allbuttons.append(Button(tk, text='40', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[28])))   
            Allbuttons.append(Button(tk, text='41', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[29])))
            Allbuttons.append(Button(tk, text='42', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[30])))
            Allbuttons.append(Button(tk, text='43', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[31])))
            Allbuttons.append(Button(tk, text='44', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[32])))
            Allbuttons.append(Button(tk, text='45', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[33])))
            Allbuttons.append(Button(tk, text='46', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[34])))
            Allbuttons.append(Button(tk, text='50', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[35])))
            Allbuttons.append(Button(tk, text='51', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[36])))
            Allbuttons.append(Button(tk, text='52', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[37])))
            Allbuttons.append(Button(tk, text='53', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[38])))
            Allbuttons.append(Button(tk, text='54', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[39])))
            Allbuttons.append(Button(tk, text='55', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[40])))
            Allbuttons.append(Button(tk, text='56', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=3, width=8, command=lambda: btnClick(Allbuttons[41])))

           

            
            
            index=0
            for i in range (taillegrilley):   
                for j in range (taillegrillex): 
                   Allbuttons[index].grid(row=i+5, column=j)
                   index = index+1

        
        if(Joueurs[0].estuneIA == True):
            finaldisableAllButton()
        elif(Joueurs[0].estuneIA == False):
            disableIAbutton()
 
        tk.mainloop()
    
    
    
    
    tk2.mainloop()