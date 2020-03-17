#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 09:08:49 2020

@author: MOsmoz_
"""

import tkinter
#tkinter._test()
import copy


class Joueur:
    def __init__(self,pseudo, estuneIA, numJoueur):
        self.pseudo=pseudo
        self.estuneIA=estuneIA
        self.numJoueur=numJoueur
        
    def getitem(self, coord):
        if (coord=='pseudo'):
            return self.pseudo
    
    def Joue(self,grille, modeJeu):
        print("Au tour de " + str(self.pseudo)) 
        if(self.estuneIA==True):
            actionfinal = self.AlphaBetaSearch(grille, modeJeu)
            grillenv=copy.deepcopy(grille)
            #grillenv[:]=list(self.Result(grillenv, actionfinal, self.numJoueur))
            print(self.numJoueur)
            return self.Result(grillenv, actionfinal, self.numJoueur)
        
        else:
            actionJoueurReel = [[],[]]
            listeactions = self.Action(grille, modeJeu)
            if modeJeu==1:
                entreevalable = False
                while(entreevalable == False):
                    CoordX=(eval(input('En quelle coord X voulez-vous jouer ?')))
                    CoordY=(eval(input('En quelle coord Y voulez-vous jouer ?')))
                    if(grille[CoordX][CoordY]==0):
                        entreevalable = True
                    else:
                        print("Tu peux pas jouer la")
                
                grille = self.Result(grille, [CoordX,CoordY], self.numJoueur)
            else :               
                CoordX=(eval(input('Dans quelle colonne voulez vous mettre votre pion ?')))
                for i in range (len(listeactions)):
                    if (listeactions[i][1]==CoordX):
                        CoordY =listeactions[i][0]
                actionJoueurReel=[CoordX,CoordY]
                grille = self.Result(grille, actionJoueurReel, self.numJoueur)
        return grille
            
    

    
    def MiniMaxDecision(self, grille, modeJeu):
        scoreMax = -10
        actionspossibles = self.Action(grille, modeJeu)
        for i in range(len(actionspossibles)):
            grillenv=copy.deepcopy(grille)
            grillenv[:]=list(self.Result(grillenv, actionspossibles[i]), self.numJoueur)
            score = self.MinValue(grillenv, modeJeu)
            if (score>scoreMax):
                scoreMax = score
                choix = i
        return (actionspossibles[choix])
    
    
    def AlphaBetaSearch(self, grille, modeJeu):
        grillenv=copy.deepcopy(grille)
        score,  actionspossibles= self.MaxValue(grillenv, modeJeu, -10, 10)
        return (actionspossibles)
        
    
    def MinValue(self,grille, modeJeu, a, b):
        gagnant = self.TerminalTest(grille, modeJeu)
        if(gagnant >=0):
            return self.Utility(gagnant), [0,0]
        else:
            scoreMin = 10
            actionspossibles = self.Action(grille, modeJeu)
            for i in range(len(actionspossibles)):
                grillenv=copy.deepcopy(grille)
                grillenv[:]=list(self.Result(grillenv, actionspossibles[i], ((self.numJoueur%2)+1)))
                score, action = self.MaxValue(grillenv, modeJeu, a, b)
                if (score<scoreMin):
                    scoreMin = score
                    choix = i
                if(scoreMin<=a):
                    return scoreMin, actionspossibles[i]
                if (scoreMin<b):
                    b = scoreMin
            return (scoreMin, actionspossibles[choix])
    
    def MaxValue(self,grille, modeJeu, a, b):
        gagnant = self.TerminalTest(grille, modeJeu)
        if(gagnant >=0):
            return self.Utility(gagnant), [0,0]
        else:
            scoreMax = -10
            actionspossibles = self.Action(grille, modeJeu)
            for i in range(len(actionspossibles)):
                grillenv=copy.deepcopy(grille)
                grillenv[:]=list(self.Result(grillenv, actionspossibles[i], self.numJoueur))
                score, action = self.MinValue(grillenv, modeJeu, a, b)
                if (score>scoreMax):
                    scoreMax = score
                    choix = i
                if(scoreMax>=b):
                    return scoreMax, actionspossibles[i]
                if(scoreMax> a):
                    a = scoreMax
            return (scoreMax, actionspossibles[choix])
        
        

    
    def Action(self,grille, modeJeu): #Va lister les actions que l'IA peut réaliser
        actionspossibles = [] #On intancie une liste vide qui va stocker les coordonnées de la grille dont la valeur est égale à 0
        if (modeJeu==1):
            for i in range(len(grille)):
                for j in range(len(grille[i])):#On parcourt toutes les cases
                    if(grille[i][j]==0):#On ajoute au tableau si c'est égal à zéro
                        actionspossibles.append([i,j])
        else:
            for j in range(len(grille[0])):
                for i in range(len(grille)):#On parcourt toutes les cases
                    if (grille[i][j]!=0):
                        actionspossibles.append(i-1,j)
                    elif(i == len(grille)-1):
                        actionspossibles.append(i,j)
                        
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
                            gagnant = 1
                    else:
                        gagnant = 1
                elif(grille[i][j]==((self.numJoueur%2)+1) and grille[i][j+1]==((self.numJoueur%2)+1) and grille[i][j+2]==((self.numJoueur%2)+1)):
                    if(modeJeu == 2):
                        if(grille[i][j+3]==((self.numJoueur%2)+1)):
                            gagnant = 2
                    else:
                        gagnant = 2
         
        #Check si gagner par colonne
        for i in range(len(grille)-nombrepourgagner+1):
            for j in range(len(grille[i])):#On parcourt toutes les cases
                if(grille[i][j]==self.numJoueur and grille[i+1][j]==self.numJoueur and grille[i+2][j]==self.numJoueur):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    if(modeJeu == 2):
                        if(grille[i+3][j]==self.numJoueur):
                            gagnant = 1
                    else:
                        gagnant = 1
                elif(grille[i][j]==((self.numJoueur%2)+1) and grille[i+1][j]==((self.numJoueur%2)+1) and grille[i+2][j]==((self.numJoueur%2)+1)):
                    if(modeJeu == 2):
                        if(grille[i+3][j]==((self.numJoueur%2)+1)):
                            gagnant = 2
                    else:
                        gagnant = 2
                        
        #Check si gagnant par diagonale descendante
        for i in range(len(grille)-nombrepourgagner+1):
            for j in range(len(grille[i])-nombrepourgagner+1):#On parcourt toutes les cases
                if(grille[i][j]==self.numJoueur and grille[i+1][j+1]==self.numJoueur and grille[i+2][j+2]==self.numJoueur):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    if(modeJeu == 2):
                        if(grille[i+3][j+3]==self.numJoueur):
                            gagnant = 1
                    else:
                        gagnant = 1
                elif(grille[i][j]==((self.numJoueur%2)+1) and grille[i+1][j+1]==((self.numJoueur%2)+1) and grille[i+2][j+2]==((self.numJoueur%2)+1)):
                    if(modeJeu == 2):
                        if(grille[i+3][j+3]==((self.numJoueur%2)+1)):
                            gagnant = 2
                    else:
                        gagnant = 2
        
        #Check si gagnant par diagonale montante
        for i in range(nombrepourgagner-1,len(grille)):
            for j in range(len(grille[i])-nombrepourgagner+1):#On parcourt toutes les cases
                if(grille[i][j]==self.numJoueur and grille[i-1][j+1]==self.numJoueur and grille[i-2][j+2]==self.numJoueur):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    if(modeJeu == 2):
                        if(grille[i-3][j+3]==self.numJoueur):
                            gagnant = 1
                    else:
                        gagnant = 1
                elif(grille[i][j]==((self.numJoueur%2)+1) and grille[i-1][j+1]==((self.numJoueur%2)+1) and grille[i-2][j+2]==((self.numJoueur%2)+1)):
                    if(modeJeu == 2):
                        if(grille[i-3][j+3]==((self.numJoueur%2)+1)):
                            gagnant = 2
                    else:
                        gagnant = 2
        
        return gagnant
        
    def Utility(self,gagnant):#On récupère le gagnant grâce à Terminal
        if(gagnant==0):#Cette valeur est retournée si il y a égalitée
            valeur = 0
        elif(gagnant==1):
            valeur = 1
        elif(gagnant==2):
            valeur = -1
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
    modeJeuvalide=False
    while(modeJeuvalide==False):
        
        print("\nBienvue dans Morpuissance 4 !\nA quel mode voulez-vous jouer ?")
        print (" 1. Morpion")
        print (" 2. Puissance 4")
        modeJeu = eval(input("Saisissez le numéro correspondant : "))
        if (modeJeu != 1 and modeJeu != 2):
            print("Erreur : Saisie non prise en compte")
        else:
            modeJeuvalide = True
    
    
    #Initialisation des taille du jeu MORPION
    if(modeJeu==1):
        taillegrillex = 3
        taillegrilley = 3
    else:
        taillegrillex = 6
        taillegrilley = 7
    
    #On crée la grille de départ, valable pour n'importe quel jeu avec une grille
    grille = [[0 for j in range(taillegrilley)] for i in range(taillegrillex)]
   
    
    #On affiche l'état de la grille
    
    Joueurs = []
    
    for i in range(1,3):
        pseudo = input("Saisissez le pseudo du Joueur %i : " %i)
        IAvalide=False
        while(IAvalide==False):
            print("\nEst-il un IA ?")
            print (" 1. Oui")
            print (" 2. Non")
            IAint = eval(input("Saisissez le numéro correspondant : "))
            if (IAint != 1 and IAint != 2):
                print("Erreur : Saisie non prise en compte")
            else:
                IAvalide = True
                if(IAint==1):
                    IA = True
                else:
                    IA = False
        Joueurs.append(Joueur(pseudo,IA,i))
        
    print(Joueurs[0].pseudo)
    print(Joueurs[1].pseudo)
    AfficherGrille(grille)
    n=0
    gagnant = -1
    while(gagnant < 0):
        print("--------------")
        grille = Joueurs[n].Joue(grille, modeJeu)
        AfficherGrille(grille)
        n = n+1
        n = n%2
        gagnant = Joueurs[n].TerminalTest(grille, modeJeu)
        
    if(gagnant == 0):
        print("Egalité")
    else:
        print(gagnant)
        print(str(Joueurs[gagnant-1].pseudo) + " a gagné !")
    #cyprinul