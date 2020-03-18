#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 09:08:49 2020

@author: MOsmoz_
"""

from tkinter import *
import tkinter.messagebox
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
    '''
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
        '''
        
        
        
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
    
    
    
        def btnClickIA(buttons):
            global tourjoueur, modeJeu, estuneIA, grille, Joueurs
            if(Joueurs[0].estuneIA == True and tourjoueur==True):
                grille = Joueurs[0].Joue(grille, modeJeu)
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
                grille = Joueurs[1].Joue(grille, modeJeu)
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
        
    
    