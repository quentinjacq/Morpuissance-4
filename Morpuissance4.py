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
            listeactions = self.Action(grille)
            for i in range (len(listeactions)):
                for j in range(len(listeactions[i])):
                    print('La/les case(s) %i,%i' %(i,j), end ="")
            print(' est/sont jouable.') 
            CoordX=(eval(input('Quelle est la coordonnée en X ?')))
            CoordY=(eval(input('Quelle est la coordonnée en Y ?')))
            actionJoueurReel=[CoordX,CoordY][self.numJoueur]
            grille = self.Result(grille,actionJoueurReel)
            
    
    #def JeuIA(grille):
        
        
        
        
    
    def Action(grille):#Va lister les actions que l'IA peut réaliser
        actionspossible = [] #On intancie une liste vide qui va stocker les coordonnées de la grille dont la valeur est égale à 0
        for i in range(len(grille)):
            for j in range(len(grille[i])):#On parcourt toutes les cases
                if(grille[i][j]==0):#On ajoute au tableau si c'est égal à zéro
                    actionspossible.append([i,j])
        return actionspossible
            
    def Result(grille, action):#Va appliquer l'action à la grille (action est une liste avec les deux coordonnés puis la valeur)
        grille[action[0]][action[1]]=action[2]
        return grille
    
    def TerminalTest(grille):#Test si c'est la fin du jeu, et qui a gagné
        nombrepourgagner = 3
        gagnant = -1#Retourne -1 si la table est complete sans gagnant, 0 si le jeu continue, 1 si le joueur 1 a gagné, 2 si le joueur 2 a gagné
        for i in range(len(grille)):
            for j in range(len(grille[i])):#On parcourt toutes les cases
                if(grille[i][j]==0):#Si une case est égalse à zéro, cela n'est pas fini
                    gagnant = 0
        
        
        pionplacementligne = [[],[]]#Liste qui contient en premier, une liste des coord du pion 1, et en 2eme une liste des coord du pion 2
        pionplacementcolonne = [[],[]]
        for i in range(len(grille)):
            for j in range(len(grille[i])):#On parcourt toutes les cases
                if(grille[i][j]==1):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    pionplacementligne[0].append(j)
                    pionplacementcolonne[0].append(j)
                elif(grille[i][j]==2):#Si une case est égalse à 2,one ajoute la coord au joueur 2
                    pionplacementligne[1].append(j)
                    pionplacementcolonne[1].append(j)
            
            for k in range(2):#On fait le test pour les deux joueurs
                n=1
                while(n<len(pionplacementligne[k])-1):
                    m=0
                    suitecontinue=True
                    while(suitecontinue==True and n<len(pionplacementligne[k])-1):
                        if (pionplacementligne[k][n]==pionplacementligne[k][n-1]+1):
                            m=m+1
                        else:
                            suitecontinue = False
                        n=n+1
                        if (m>=nombrepourgagner):
                            gagnant = k + 1 #Le joueur k+1 a gagné, +1 car le tableau est 0 puis 1, donc pour joueur 1 est 2 on incrémente de 1
             
            for k in range(2):#On fait le test pour les deux joueurs
                n=1
                while(n<len(pionplacementcolonne[k])-1):
                    m=0
                    suitecontinue=True
                    while(suitecontinue==True and n<len(pionplacementcolonne[k])-1):
                        if (pionplacementcolonne[k][n]==pionplacementcolonne[k][n-1]+1):
                            m=m+1
                        else:
                            suitecontinue = False
                        n=n+1
                        if (m>=nombrepourgagner):
                            gagnant = k + 1 #Le joueur k+1 a gagné, +1 car le tableau est 0 puis 1, donc pour joueur 1 est 2 on incrémente de 1
            
                            
                        
                        
        
        
        #Ou mettre le for pour les deux joueur test (tableau)
        
        
        
            
def AfficherGrille(grille):#Simple méthode pour afficher esthétiquement la grille
    print("\n -----------")
    for i in range(len(grille)):
        print("| ",end='')
        for j in range(len(grille[i])):
            print(str(grille[i][j])+" | ",end='')
        print("\n -----------")



if __name__== '__main__':
    
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
    
    