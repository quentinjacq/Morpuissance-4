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
      

    #Initialisation des taille du jeu MORPION
    #On crée la grille de départ, valable pour n'importe quel jeu avec une grille
    grille = [[0 for j in range(3)] for i in range(3)]
    
    #On affiche l'état de la grille
    AfficherGrille(grille)
        
    
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
        tk.title("Tic Tac Toe")
        
        print(var1.get())
        print(var2.get())
        
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
        
        
        
        
        def disableIAbutton():        
            buttonIA.configure(state=DISABLED)
        
        
        def AffichepasbuttononUsed(button):
            if (button['text']=='X' or button['text']=='O'):
                button['disabledforeground']='white'
            else:
                button['disabledforeground']='gray'

        def finaldisableAllButton():        
            button1.configure(state=DISABLED)
            AffichepasbuttononUsed(button1)
            button2.configure(state=DISABLED)
            AffichepasbuttononUsed(button2)
            button3.configure(state=DISABLED)
            AffichepasbuttononUsed(button3)
            button4.configure(state=DISABLED)
            AffichepasbuttononUsed(button4)
            button5.configure(state=DISABLED)
            AffichepasbuttononUsed(button5)
            button6.configure(state=DISABLED)
            AffichepasbuttononUsed(button6)
            button7.configure(state=DISABLED)
            AffichepasbuttononUsed(button7)
            button8.configure(state=DISABLED)
            AffichepasbuttononUsed(button8)
            button9.configure(state=DISABLED)
            AffichepasbuttononUsed(button9)

         
            
            
        def EnableIAButton():        
            buttonIA.configure(state=NORMAL)
            
            
        def BoutonUsedstayused(button):
            if (button['text']=='X' or button['text']=='O'):
                button.configure(state=DISABLED)
                button['disabledforeground']='white'
                
        def EnableAllButton():        
            button1.configure(state=NORMAL)
            BoutonUsedstayused(button1)
            button2.configure(state=NORMAL)
            BoutonUsedstayused(button2)
            button3.configure(state=NORMAL)
            BoutonUsedstayused(button3)
            button4.configure(state=NORMAL)
            BoutonUsedstayused(button4)
            button5.configure(state=NORMAL)
            BoutonUsedstayused(button5)
            button6.configure(state=NORMAL)
            BoutonUsedstayused(button6)
            button7.configure(state=NORMAL)
            BoutonUsedstayused(button7)
            button8.configure(state=NORMAL)
            BoutonUsedstayused(button8)
            button9.configure(state=NORMAL)
            BoutonUsedstayused(button9)
            
            
        def disableButton(buttons):
            buttons.configure(state=DISABLED)
    
        def ModifieButton(coord, tourjoueur):
            if(coord[0]==0):
                numerobutton=coord[1]+1
            elif(coord[0]==1):
                numerobutton=coord[1]+4
            else:
                numerobutton=coord[1]+7
            print(numerobutton)
            
            if (numerobutton == 1):
                if (tourjoueur==True):
                    button1['text']='X'
                    button1['fg']='white'
                    button1['disabledforeground']='white'
                else:
                    button1['text']='O'
                    button1['fg']='white'
                    button1['disabledforeground']='white'
            elif (numerobutton == 2):
                if (tourjoueur==True):
                    button2['text']='X'
                    button2['fg']='white'
                    button2['disabledforeground']='white'
                else:
                    button2['text']='O'
                    button2['fg']='white'
                    button2['disabledforeground']='white'
            elif (numerobutton == 3):
                if (tourjoueur==True):
                    button3['text']='X'
                    button3['fg']='white'
                    button3['disabledforeground']='white'
                else:
                    button3['text']='O'
                    button3['fg']='white'
                    button3['disabledforeground']='white'
            elif (numerobutton == 4):
                if (tourjoueur==True):
                    button4['text']='X'
                    button4['fg']='white'
                    button4['disabledforeground']='white'
                else:
                    button4['text']='O'
                    button4['fg']='white'
                    button4['disabledforeground']='white'
            elif (numerobutton == 5):
                if (tourjoueur==True):
                    button5['text']='X'
                    button5['fg']='white'
                    button5['disabledforeground']='white'
                else:
                    button5['text']='O'
                    button5['fg']='white'
                    button5['disabledforeground']='white'                   
            elif (numerobutton == 6):
                if (tourjoueur==True):
                    button6['text']='X'
                    button6['fg']='white'
                    button6['disabledforeground']='white'
                else:
                    button6['text']='O'
                    button6['fg']='white'
                    button6['disabledforeground']='white'                    
            elif (numerobutton == 7):
                if (tourjoueur==True):
                    button7['text']='X'
                    button7['fg']='white'
                    button7['disabledforeground']='white'
                else:
                    button7['text']='O'
                    button7['fg']='white'
                    button7['disabledforeground']='white'
            elif (numerobutton == 8):
                if (tourjoueur==True):
                    button8['text']='X'
                    button8['fg']='white'
                    button8['disabledforeground']='white'
                else:
                    button8['text']='O'
                    button8['fg']='white'
                    button8['disabledforeground']='white'
            elif (numerobutton == 9):
                if (tourjoueur==True):
                    button9['text']='X'
                    button9['fg']='white'
                    button9['disabledforeground']='white'
                else:
                    button9['text']='O'
                    button9['fg']='white'
                    button9['disabledforeground']='white'
    
        def btnClickIA(buttons):
            global tourjoueur, modeJeu, estuneIA, grille, Joueurs
            if(Joueurs[0].estuneIA == True and tourjoueur==True):
                grille, coord = Joueurs[0].Joue(grille, modeJeu)
                
                
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
            if grille[int(buttons['text'][0])][int(buttons['text'][1])] ==0 and tourjoueur==True and Joueurs[0].estuneIA == False: 
                grille[int(buttons['text'][0])][int(buttons['text'][1])]=1
                AfficherGrille(grille)
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
        #Allbuttons=[]
        
        buttonIA = Button(tk, text='IA', font='Times 20 bold', bg='gray', fg='black', activeforeground='gray',activebackground='gray', disabledforeground='black', command=lambda: btnClickIA(btnClickIA))
        buttonIA.grid(row=4, column=0)
        
      
        button1 = Button(tk, text='00', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray', disabledforeground='white', height=4, width=8, command=lambda: btnClick(button1))
        button1.grid(row=5, column=0)
        
        button2 = Button(tk, text='01', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray',disabledforeground='white', height=4, width=8, command=lambda: btnClick(button2))
        button2.grid(row=5, column=1)
        
        button3 = Button(tk, text='02', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray',disabledforeground='white', height=4, width=8, command=lambda: btnClick(button3))
        button3.grid(row=5, column=2)
        
        button4 = Button(tk, text='10', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray',disabledforeground='white', height=4, width=8, command=lambda: btnClick(button4))
        button4.grid(row=6, column=0)
        
        button5 = Button(tk, text='11', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray',disabledforeground='white', height=4, width=8, command=lambda: btnClick(button5))
        button5.grid(row=6, column=1)
        
        button6 = Button(tk, text='12', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray',disabledforeground='white', height=4, width=8, command=lambda: btnClick(button6))
        button6.grid(row=6, column=2)
        
        button7 = Button(tk, text='20', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray',disabledforeground='white', height=4, width=8, command=lambda: btnClick(button7))
        button7.grid(row=7, column=0)
        
        button8 = Button(tk, text='21', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray',disabledforeground='white', height=4, width=8, command=lambda: btnClick(button8))
        button8.grid(row=7, column=1)
        
        button9 = Button(tk, text='22', font='Times 20 bold', bg='gray', fg='gray', activeforeground='gray',activebackground='gray',disabledforeground='white', height=4, width=8, command=lambda: btnClick(button9))
        button9.grid(row=7, column=2)        
        
        
        if(Joueurs[0].estuneIA == True):
            finaldisableAllButton()
        elif(Joueurs[0].estuneIA == False):
            disableIAbutton()
 
        tk.mainloop()
    
    
    
    
    tk2.mainloop()
        
    
    