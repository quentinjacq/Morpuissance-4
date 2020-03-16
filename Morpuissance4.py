#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 09:08:49 2020

@author: MOsmoz_
"""

import tkinter
#tkinter._test()


class Joueur:
    def __init__(self,pseudo, estuneIA):
        self.pseudo=pseudo
        self.estuneIA=estuneIA
    
    def Joue(grille):
        if(estuneIA==True):
            JeuIA(grille)
        else:
            JeuIA(grille)
            
            
            
            
    
    def JeuJoueurReel(grille):
        zfzefzef
    
    def JeuIA(grille):
        
        
        
        
    
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
    
    def TerminalTest(grille):#Test si c'est la fin du jeu
        nombrepourgagner = 3
        termine = True#Retourne faux si je leu n'est pas fini, True si le jeu est fini
        for i in range(len(grille)):
            for j in range(len(grille[i])):#On parcourt toutes les cases
                if(grille[i][j]==0):#Si une case est égalse à zéro, cela n'est pas fini
                    termine = False
        
        
        pionplacement = [[],[]]#Liste qui contient en premier, une liste des coord du pion 1, et en 2eme une liste des coord du pion 2
        for i in range(len(grille)):
            for j in range(len(grille[i])):#On parcourt toutes les cases
                if(grille[i][j]==1):#Si une case est égalse à 1, on ajoute la coord au joueur 1
                    pionplacement[0].append(j)
                elif(grille[i][j]==2):#Si une case est égalse à 2,one ajoute la coord au joueur 2
                    pionplacement[1].append(j)
            
            for k in range(2):#On fait le test pour les deux joueurs
                n=1
                while(n<len(pionplacement[k])-1):
                    m=0
                    suitecontinue=True
                    while(suitecontinue==True and n<len(pionplacement[k])-1):
                        if (pionplacement[k][n]==pionplacement[k][n-1]+1):
                            m++
                        else:
                            suitecontinue = False
                        n++
                        if (m>=nombrepourgagner):
                            termine = True
            
                            
                        
                        
        
        
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
    AfficherGrille(grille,taillegrillex, taillegrilley)