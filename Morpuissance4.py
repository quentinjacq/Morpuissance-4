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
        
    
    def Joue(self,grille, modeJeu):
        if(self.estuneIA==True):
            actionfinal = self.MiniMaxDecision(grille, modeJeu)
            grillenv=copy.deepcopy(grille)
            grillenv[:]=list(self.Result(grillenv, actionfinal))
            return self.Result(grillenv, actionfinal)
        
        else:
            actionJoueurReel = [[],[]]
            print("C'est le tour du Joueur %i" %self.numJoueur) 
            listeactions = self.Action(grille, modeJeu)
            print('La/les case(s) ', end ="")
            for i in range (len(listeactions)):
                for j in range(len(listeactions[i])):
                    print('(%i,%i), ' %(i,j), end ="")
            print(' est/sont jouable.')
            if modeJeu==1:
                entreevalable = False
                while(entreevalable == False):
                    CoordX=(eval(input('Quelle est la coordonnée en X ?')))
                    CoordY=(eval(input('Quelle est la coordonnée en Y ?')))
                    if(grille[CoordX][CoordY]==0):
                        entreevalable = True
                    else:
                        print("Tu peux pas jouer la")
                
                grille = self.Result(grille, [CoordX,CoordY])
            else :               
                CoordX=(eval(input('Dans quelle colonne voulez vous mettre votre pion ?')))
                for i in range (len(listeactions)):
                    if (listeactions[i][1]==CoordX):
                        CoordY =listeactions[i][0]
                actionJoueurReel=[CoordX,CoordY]
                grille = self.Result(grille, actionJoueurReel)
        return grille
            
    

    
    def MiniMaxDecision(self, grille, modeJeu):
        scoreMax = -10
        actionspossibles = self.Action(grille, modeJeu)
        for i in range(len(actionspossibles)):
            print("Coord : ", end='')
            print(actionspossibles[i])
            grillenv=copy.deepcopy(grille)
            grillenv[:]=list(self.Result(grillenv, actionspossibles[i]))
            score = self.MinValue(grillenv, modeJeu)
            print(score)
            
            if (score>scoreMax):
                scoreMax = score
                choix = i
        return (actionspossibles[choix])
    
    def MinValue(self,grille, modeJeu):
        gagnant = self.TerminalTest(grille, modeJeu)
        if(gagnant >=0):
            print("coucou")
            return self.Utility(gagnant)
        else:
            scoreMin = 10
            actionspossibles = self.Action(grille, modeJeu)
            for i in range(len(actionspossibles)):
                grillenv=copy.deepcopy(grille)
                grillenv[:]=list(self.Result(grillenv, actionspossibles[i], 2))
                score = self.MaxValue(grillenv, modeJeu)
                if (score<scoreMin):
                    scoreMin = score
            return (scoreMin)
    
    def MaxValue(self,grille, modeJeu):
        gagnant = self.TerminalTest(grille, modeJeu)
        if(gagnant >=0):
            print("coucou2")
            return self.Utility(gagnant)
        else:
            scoreMax = -10
            actionspossibles = self.Action(grille, modeJeu)
            for i in range(len(actionspossibles)):
                grillenv=copy.deepcopy(grille)
                grillenv[:]=list(self.Result(grillenv, actionspossibles[i]))
                score = self.MinValue(grillenv, modeJeu)
                if (score>scoreMax):
                    scoreMax = score
            return (scoreMax)
        
        

    
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

            
    def Result(self, grille, action, numJoueur=1):#Va appliquer l'action à la grille (action est une liste avec les deux coordonnés puis la valeur)
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
                if(grille[i][j]==1 and grille[i][j+1]==1 and grille[i][j+2]==1):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    if(modeJeu == 2):
                        if(grille[i][j+3]==1):
                            gagnant = 1
                    else:
                        gagnant = 1
                elif(grille[i][j]==2 and grille[i][j+1]==2 and grille[i][j+2]==2):
                    if(modeJeu == 2):
                        if(grille[i][j+3]==2):
                            gagnant = 2
                    else:
                        gagnant = 2
         
        #Check si gagner par colonne
        for i in range(len(grille)-nombrepourgagner+1):
            for j in range(len(grille[i])):#On parcourt toutes les cases
                if(grille[i][j]==1 and grille[i+1][j]==1 and grille[i+2][j]==1):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    if(modeJeu == 2):
                        if(grille[i+3][j]==1):
                            gagnant = 1
                    else:
                        gagnant = 1
                elif(grille[i][j]==2 and grille[i+1][j]==2 and grille[i+2][j]==2):
                    if(modeJeu == 2):
                        if(grille[i+3][j]==2):
                            gagnant = 2
                    else:
                        gagnant = 2
                        
        #Check si gagnant par diagonale descendante
        for i in range(len(grille)-nombrepourgagner+1):
            for j in range(len(grille[i])-nombrepourgagner+1):#On parcourt toutes les cases
                if(grille[i][j]==1 and grille[i+1][j+1]==1 and grille[i+2][j+2]==1):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    if(modeJeu == 2):
                        if(grille[i+3][j+3]==1):
                            gagnant = 1
                    else:
                        gagnant = 1
                elif(grille[i][j]==2 and grille[i+1][j+1]==2 and grille[i+2][j+2]==2):
                    if(modeJeu == 2):
                        if(grille[i+3][j+3]==2):
                            gagnant = 2
                    else:
                        gagnant = 2
        
        #Check si gagnant par diagonale montante
        for i in range(nombrepourgagner-1,len(grille)):
            for j in range(len(grille[i])-nombrepourgagner+1):#On parcourt toutes les cases
                if(grille[i][j]==1 and grille[i-1][j+1]==1 and grille[i-2][j+2]==1):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    if(modeJeu == 2):
                        if(grille[i-3][j+3]==1):
                            gagnant = 1
                    else:
                        gagnant = 1
                elif(grille[i][j]==2 and grille[i-1][j+1]==2 and grille[i-2][j+2]==2):
                    if(modeJeu == 2):
                        if(grille[i-3][j+3]==2):
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
            print(str(grille[i][j])+" | ",end='')
        print("\n -----------")



if __name__== '__main__':
    """print("A quel mode voulez vous jouer ?")
    print (" 1. Tic Tac Toe")
    print (" 2. Connect 4")
    modeJeu = eval(input())"""
    
    modeJeu = 1
    
    #Initialisation des taille du jeu MORPION
    taillegrillex = 3
    taillegrilley = 3
    
    #On crée la grille de départ, valable pour n'importe quel jeu avec une grille
    grille = [[0 for j in range(taillegrilley)] for i in range(taillegrillex)]
    
    

    #On affiche l'état de la grille
    AfficherGrille(grille)
    J1 = Joueur('IA',True,1)
    J2 = Joueur('Cyprien le naze', False, 2)
    
    while(J1.TerminalTest(grille, 1) < 0):
        grille = J1.Joue(grille, modeJeu)
        AfficherGrille(grille)
        
        grille = J2.Joue(grille, modeJeu)
        AfficherGrille(grille)
     
    if(J1.TerminalTest(grille, 1) == 0):
        print("Egalité")
    else:
        print("Joueur %i a gagné !" %J1.TerminalTest(grille, 1))
    