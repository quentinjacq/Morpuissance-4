#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 09:08:49 2020

@author: MOsmoz_
"""

from tkinter import *
import tkinter.messagebox
import copy
from random import choice

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
            return self.Result(grillenv, actionfinal, self.numJoueur), actionfinal
        
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
        return grille, actionfinal
            
    

    
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
        score,  actionspossibles, prof= self.MaxValue(grillenv, modeJeu, -50, 50, 1)
        return (actionspossibles)
        
    
    def MinValue(self,grille, modeJeu, a, b, prof):
        gagnant = self.TerminalTest(grille, modeJeu)
        if(gagnant >=0):
            return self.Utility(gagnant), [0,0], prof
        else:
            scoreMin = 10
            profmin = 10
            actionspossibles = self.Action(grille, modeJeu)
            for i in range(len(actionspossibles)):
                grillenv=copy.deepcopy(grille)
                if prof ==2:
                    print("   "*prof, end="")
                    print("Coord : ")
                    print("   "*prof, end="")
                    print(actionspossibles[i])
                grillenv[:]=list(self.Result(grillenv, actionspossibles[i], ((self.numJoueur%2)+1)))
                score, action, profcoupwin = self.MaxValue(grillenv, modeJeu, a, b, prof+1)
                
                if (score<scoreMin or (score==scoreMin and profcoupwin<profmin)):
                    profmin = profcoupwin
                    scoreMin = score
                    choix = i
                if prof ==2:
                    print("   "*prof, end="")
                    print("score final " + str(scoreMin))
                if(scoreMin<a):
                    if prof ==2:
                        print("                     Choisi au final" + str(scoreMin))
                    return scoreMin, actionspossibles[i], prof
                if (scoreMin<b):
                    b = scoreMin
            if prof ==2:
                print("                     Choisi au final" + str(scoreMin))
            return (scoreMin, actionspossibles[choix], prof)
    
    def MaxValue(self,grille, modeJeu, a, b, prof):
        gagnant = self.TerminalTest(grille, modeJeu)
        if(gagnant >=0):
            return self.Utility(gagnant), [0,0], prof
        else:
            scoreMax = -10
            profmin = 10
            actionspossibles = self.Action(grille, modeJeu)
            for i in range(len(actionspossibles)):
                grillenv=copy.deepcopy(grille)
                grillenv[:]=list(self.Result(grillenv, actionspossibles[i], self.numJoueur))
                if prof==1:
                    print("Coord : ")
                    print(actionspossibles[i])
                    random = choice([1,2])
                    print("random : ")
                    print(random)
                score, action, profcoupwin = self.MinValue(grillenv, modeJeu, a, b, prof+1)
                if (score>scoreMax or (score==scoreMax and profcoupwin<profmin)or (score != -1 and score==scoreMax and profcoupwin == profmin and prof == 1 and random==1)):
                    profmin = profcoupwin
                    scoreMax = score
                    choix = i
                    if prof ==1:
                        print("                                 Je vais choisir lui")
                    
                #if prof==1:
                    #print("Score choisi : ")
                    #print(scoreMax)
                    #print("Coord choisi : ")
                    #print(actionspossibles[choix])
                if(scoreMax>b):
                    if prof ==2:
                        print("                     Choisi au final" + str(scoreMin))
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
        
    def Utility(self,gagnant):#On récupère le gagnant grâce à Terminal
        if(gagnant==0):#Cette valeur est retournée si il y a égalitée
            valeur = 0
        elif(gagnant==self.numJoueur):
            valeur = 1
        elif(gagnant==((self.numJoueur%2)+1)):
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
    
    tk2 =Tk()
    p1 = StringVar()
    p2 = StringVar()
    tourjoueur = True
    Joueurs = []
    n=0
    gagnant = -1    
    estuneIA = False
    modeJeu=1
    
    
    player1_name = Entry(tk2, textvariable=p1, bd=5)
    player1_name.grid(row=1, column=1, columnspan=8)
    player2_name = Entry(tk2, textvariable=p2, bd=5)
    player2_name.grid(row=2, column=1, columnspan=8)
    
    
    

    buttons = StringVar()

    label = Label( tk2, text="Player 1:", font='Times 20 bold', bg='white', fg='black', height=1, width=8)
    label.grid(row=1, column=0)
    
    label = Label( tk2, text="Player 2:", font='Times 20 bold', bg='white', fg='black', height=1, width=8)
    label.grid(row=2, column=0) 
  
    
    var1 = IntVar()
    checkIA1 = Checkbutton(tk2, text="Player 1 is an IA", variable=var1)
    checkIA1.grid(row=3, column=0)
    var1.get()

    var2 = IntVar()
    checkIA2 = Checkbutton(tk2, text="Player 2 is an IA", variable=var2)
    checkIA2.grid(row=3, column=1)
    var2.get()
    
    
    variable = StringVar(tk2)
    variable.set("Tic Tac Toe") # default value  
    w = OptionMenu(tk2, variable, "Tic Tac Toe", "Connect 4")
    w.grid(row=4, column=0)
    
    
    
    
    button_quitter = Button(tk2, text='Play', font='Times 20 bold', command = lambda: jeu())
    button_quitter.grid(row=5, column=1)
    

    
    def jeu():
        global grille, estuneIA
        button_quitter.configure(state=DISABLED)
        
        checkIA1.configure(state=DISABLED)
        var2.get()
        checkIA2.configure(state=DISABLED)
        p1.get()
        player1_name.configure(state=DISABLED)
        p2.get()
        player2_name.configure(state=DISABLED)
        variable.get()
        w.configure(state=DISABLED)
        
        tk = Tk()
        tk.title("Tic Tac Toe/ Connect 4")
        
        
        if (var1.get()==0):
            J1=Joueur(p1.get(),estuneIA,1)
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
            
            
        print(taillegrillex)
        print(modeJeu) 
            
        #Initialisation des taille du jeu MORPION
        #On crée la grille de départ, valable pour n'importe quel jeu avec une grille
        grille = [[0 for j in range(taillegrillex)] for i in range(taillegrilley)]
        
        #On affiche l'état de la grille
        AfficherGrille(grille)
            
            

            
        
        def disableIAbutton():        
            buttonIA.configure(state=DISABLED)
        
        
        def AffichepasbuttononUsed(button):
            if (button['text']=='X' or button['text']=='O'):
                button['disabledforeground']='white'
            else:
                button['disabledforeground']='gray'

        def finaldisableAllButton():  
            for i in range (len(Allbuttons)):
                Allbuttons[i].configure(state=DISABLED)
                AffichepasbuttononUsed(Allbuttons[i])
            
         
            
            
        def EnableIAButton():        
            buttonIA.configure(state=NORMAL)
            
            
        def BoutonUsedstayused(button):
            if (button['text']=='X' or button['text']=='O'):
                button.configure(state=DISABLED)
                button['disabledforeground']='white'
                
        def EnableAllButton():        
            for i in range (len(Allbuttons)):
                Allbuttons[i].configure(state=NORMAL)
                BoutonUsedstayused(Allbuttons[i])
            
            
        def disableButton(buttons):
            buttons.configure(state=DISABLED)
    
        def ModifieButton(coord, tourjoueur):
            if(coord[0]==0):
                numerobutton=coord[1]+1
            elif(coord[0]==1):
                numerobutton=coord[1]+4
            else:
                numerobutton=coord[1]+7
            
            Allbuttons[numerobutton-1]['text']='X' if (tourjoueur== True) else 'O'
            Allbuttons[numerobutton-1]['fg']='white'
            Allbuttons[numerobutton-1]['disabledforeground']='white'
    
        def btnClickIA(buttons):
            global tourjoueur, modeJeu, estuneIA, grille, Joueurs
            if(Joueurs[0].estuneIA == True and tourjoueur==True):
                grille, coord = Joueurs[0].Joue(grille, modeJeu)
                print ("terminal test ia")
                print(J1.TerminalTest(grille, modeJeu))
                
                ModifieButton(coord, tourjoueur)
                tourjoueur = False
                AfficherGrille(grille)
                
                if (Joueurs[1].estuneIA == False):
                    EnableAllButton()
                    disableIAbutton()
                    
                if (J1.TerminalTest(grille, modeJeu)==1):
                    tkinter.messagebox.showinfo("Tic-Tac-Toe", "Le Joueur "+ J1.pseudo + " gagne.") 
                    finaldisableAllButton()
                elif (J1.TerminalTest(grille, modeJeu)==0):
                    tkinter.messagebox.showinfo("Tic-Tac-Toe", 'Il y a une égalité.')
    
            elif(Joueurs[1].estuneIA == True and tourjoueur==False):
                grille, coord = Joueurs[1].Joue(grille, modeJeu)
                print ("terminal test ia2")
                print(J2.TerminalTest(grille, modeJeu))
                
                ModifieButton(coord, tourjoueur)
                tourjoueur = True
                AfficherGrille(grille)
                
                if (Joueurs[0].estuneIA == False):
                    EnableAllButton()
                    disableIAbutton()
                
                if (J2.TerminalTest(grille, modeJeu)==2):
                    tkinter.messagebox.showinfo("Tic-Tac-Toe", "Le Joueur "+ J2.pseudo + " gagne.")
                    finaldisableAllButton()
                elif (J2.TerminalTest(grille, modeJeu)==0):
                    tkinter.messagebox.showinfo("Tic-Tac-Toe", 'Il y a une égalité.')
    
    
        def btnClick(buttons):
            global tourjoueur, modeJeu, estuneIA, grille
            
            if grille[int(buttons['text'][0])][int(buttons['text'][1])]==0 and tourjoueur==True and Joueurs[0].estuneIA == False: 
                grille[int(buttons['text'][0])][int(buttons['text'][1])]=1
                AfficherGrille(grille)
                print ("terminal test joeuru")
                print(J1.TerminalTest(grille, 1))
                
                
                if (Joueurs[1].estuneIA == True):
                    finaldisableAllButton()
                    EnableIAButton()
                    
                    
                buttons['text']='X'
                buttons['fg']='white'
                tourjoueur = False
                buttons['disabledforeground']='white'
                disableButton(buttons)
                
                if (J1.TerminalTest(grille, modeJeu)==1):
                    tkinter.messagebox.showinfo("Tic-Tac-Toe", "Le Joueur "+ J1.pseudo + " gagne.") 
                    finaldisableAllButton()
                elif (J1.TerminalTest(grille, modeJeu)==0):
                    tkinter.messagebox.showinfo("Tic-Tac-Toe", 'Il y a une égalité.')
                     
            elif (grille[int(buttons['text'][0])][int(buttons['text'][1])] == 0 and tourjoueur == False and Joueurs[1].estuneIA == False):
                grille[int(buttons['text'][0])][int(buttons['text'][1])] = 2  
                AfficherGrille(grille)
                print ("terminal test joeuru")
                print(J2.TerminalTest(grille, 1))
                tourjoueur = True
                
                if (Joueurs[0].estuneIA == True):
                    finaldisableAllButton()
                    EnableIAButton()
                
                buttons['text']='O'
                buttons['fg']='black'
                buttons['disabledforeground']='white'
                disableButton(buttons)
                
                if (J2.TerminalTest(grille, modeJeu)==2):
                    tkinter.messagebox.showinfo("Tic-Tac-Toe", "Le Joueur "+ J2.pseudo + " gagne.")
                    finaldisableAllButton()
                elif (J2.TerminalTest(grille, modeJeu)==0):
                    tkinter.messagebox.showinfo("Tic-Tac-Toe", 'Il y a une égalité.')
            

        
        buttons = StringVar()
        textbutton = StringVar()

        buttonIA = Button(tk, text='IA', font='Times 20 bold', bg='gray', fg='black', activeforeground='gray',activebackground='gray', disabledforeground='black', command=lambda: btnClickIA(btnClickIA))
        buttonIA.grid(row=4, column=0)
        
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

           
            print(len(Allbuttons))
            
            
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