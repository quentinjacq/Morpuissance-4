#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 09:08:49 2020

@author: MOsmoz_
"""

import tkinter
#tkinter._test()


class Joueur:
    def __init__(self,pseudo, estuneIA, numJoueur):
        self.pseudo=pseudo
        self.estuneIA=estuneIA
        self.numJoueur=numJoueur
        
    
    def Joue(self,grille):
        if(self.estuneIA==True):
            #JeuIA(grille)
            print('')
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
                CoordX=(eval(input('Quelle est la coordonnée en X ?')))
                CoordY=(eval(input('Quelle est la coordonnée en Y ?')))
                actionJoueurReel=[CoordX,CoordY,self.numJoueur]
                grille = self.Result(grille, actionJoueurReel)
            else :               
                CoordX=(eval(input('Dans quelle colonne voulez vous mettre votre pion ?')))
                for i in range (len(listeactions)):
                    if (listeactions[i][1]==CoordX):
                        CoordY =listeactions[i][0]
                actionJoueurReel=[CoordX,CoordY,self.numJoueur]
                grille = self.Result(grille, actionJoueurReel)
            
    
    #def JeuIA(grille):
        

        
    
    def Action(self,grille, modeJeu): #Va lister les actions que l'IA peut réaliser
        actionspossible = [] #On intancie une liste vide qui va stocker les coordonnées de la grille dont la valeur est égale à 0
        if (modeJeu==1):
            for i in range(len(grille)):
                for j in range(len(grille[i])):#On parcourt toutes les cases
                    if(grille[i][j]==0):#On ajoute au tableau si c'est égal à zéro
                        actionspossible.append([i,j])
        else:
            for j in range(len(grille[i])):
                for i in range(len(grille)):#On parcourt toutes les cases
                    if (grille[i][j]==0):
                        actionspossible.append(i,j)
        return actionspossible

            
    def Result(self, grille, action):#Va appliquer l'action à la grille (action est une liste avec les deux coordonnés puis la valeur)
        grille[action[0]][action[1]]=action[2]
        return grille
    
    def TerminalTest(grille, modeJeu):#Test si c'est la fin du jeu, et qui a gagné
        
        
        nombrepourgagner = 3 
        
        gagnant = -1#Retourne -1 si la table est complete sans gagnant, 0 si le jeu continue, 1 si le joueur 1 a gagné, 2 si le joueur 2 a gagné
        for i in range(len(grille)):
            for j in range(len(grille[i])):#On parcourt toutes les cases
                if(grille[i][j]==0):#Si une case est égalse à zéro, cela n'est pas fini
                    gagnant = 0
        
        #Check si gagner par lignes
        for i in range(len(grille)-1):
            for j in range(len(grille[i])-nombrepourgagner-1):#On parcourt toutes les cases
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
         
        
        
        return gagnant
        #Ou mettre le for pour les deux joueur test (tableau)
        
        
        
            
def AfficherGrille(grille):#Simple méthode pour afficher esthétiquement la grille
    print("\n -----------")
    for i in range(len(grille)):
        print("| ",end='')
        for j in range(len(grille[i])):
            print(str(grille[i][j])+" | ",end='')
        print("\n -----------")



if __name__== '__main__':
    print("A quel mode voulez vous jouer ?")
    print (" 1. Tic Tac Toe")
    print (" 2. Connect 4")
    modeJeu = eval(input())
    
    #Initialisation des taille du jeu MORPION
    taillegrillex = 3
    taillegrilley = 3
    
    #On crée la grille de départ, valable pour n'importe quel jeu avec une grille
    grille = [[0 for j in range(taillegrilley)] for i in range(taillegrillex)]
    
    #On affiche l'état de la grille
    AfficherGrille(grille)
    J1 = Joueur('moi',False,1)
    J1.Joue(grille)
    AfficherGrille(grille)
    J1.Joue(grille)
    AfficherGrille(grille)
    J1.Joue(grille)
    AfficherGrille(grille)

    