import tkinter as tk
from functools import partial

BACKGROUND_COLOR = "#1f1f2e"
BUTTON_COLOR = "#29293d"
RESTART_COLOR = "#29293d"

MAX_DEPTH = 9
MAX = 1
MIN = -1

class Board:
    def __init__(self, node):
        self.positions = {}
        n = node
        while n.position != '': #while it's not the tree's root#
            self.positions[n.position] = n.parent.objective #get the node's position and the objective of the parent#
            n = n.parent
        for i in range(0, MAX_DEPTH): #filling with the empty positions#
            if not self.positions.get(i):
                self.positions[i] = 0

    def checkWinner(self):
        for i in range(0, 3):
            #checking if MAX wins#
            if (self.positions.get(i*3) == MAX) & (self.positions.get((i*3)+1) == MAX) & (self.positions.get((i*3)+2) == MAX): #checking lines#
                return MAX;
            if (self.positions.get(i) == MAX) & (self.positions.get(i+3) == MAX) & (self.positions.get(i+6) == MAX): #checking columns#
                return MAX;

            #checking if MIN wins#
            if (self.positions.get(i*3) == MIN) & (self.positions.get((i*3)+1) == MIN) & (self.positions.get((i*3)+2) == MIN): #checking lines#
                return MIN
            if (self.positions.get(i) == MIN) & (self.positions.get(i+3) == MIN) & (self.positions.get(i+6)== MIN): #checking columns#
                return MIN

        # checking if MAX wins#
        if (self.positions.get(0) == MAX) & (self.positions.get(4) == MAX) & (self.positions.get(8) == MAX): #checking diagonal 1#
            return MAX;
        if (self.positions.get(2) == MAX) & (self.positions.get(4) == MAX) & (self.positions.get(6) == MAX): #checking diagonal 2#
            return MAX;

        # checking if MIN wins#
        if (self.positions.get(0) == MIN) & (self.positions.get(4) == MIN) & (self.positions.get(8) == MIN):  # checking diagonal 1#
            return MIN;
        if (self.positions.get(2) == MIN) & (self.positions.get(4) == MIN) & (self.positions.get(6) == MIN):  # checking diagonal 2#
            return MIN;

        return 0 #draw#

    def print(self):
        for i in [0, 3, 6]:
            for j in range(0,3):
                if self.positions.get(i+j) == MAX:
                    print('X ', end='')
                elif self.positions.get(i+j) == MIN:
                    print('O ', end='')
                else:
                    print('  ', end='')
            print('')
        print('\n\n')


class Node:
    def __init__(self, parent, level, position, objective):
        self.parent = parent #parent node#
        self.level = level #level of the node in the tree#
        self.position = position #position of the move on the board#
        self.objective = objective #the objective, MIN = -1, MAX = 1#
        self.evaluation = '' #value returned after the checking#
        self.children = [] #list of children#

    def createChildren(self, occupiedPositions):
        if self.level > 4:  #if 5 moves were made, we can start looking for a winner#
            board = Board(self)
            result = board.checkWinner()
            if result != 0:  #if we have a winner, we don't need to continue#
               self.evaluation = result #set the evaluation for the leaf#
               return    #the node will bea leaf#

        if self.level == MAX_DEPTH: #the node is a leaf#
            board = Board(self)
            self.evaluation = board.checkWinner() #set the evaluation for the leaf#
            return

        occupied = list(occupiedPositions) #add the parent position to the list of occupied positions#
        occupied.append(self.position)
        for i in range(0, MAX_DEPTH):
            if i not in occupied:
                node = Node(self, self.level+1, i,  self.objective*-1) #child has an opposite objective#
                node.createChildren(occupied)
                self.children.append(node)

    def evaluate(self):
        if not self.children: #if its a leaf#
            return self.evaluation #it was already evaluated at the creation of children#

        values = []
        for child in self.children: #evaluate all the children#
                values.append(child.evaluate())
        if self.objective == MAX:
            self.evaluation = max(values)
        else:
            self.evaluation = min(values)
        return self.evaluation

    def print(self):
        print("Current Node: level: ", self.level, " position: ", self.position)
        for child in self.children:
            print("Children: ", child.evaluation, end=", ")
        print("\n")
        for child in self.children:
            child.print()

class Tree:
    def __init__(self):
        self.root = Node(None, 0, '', MAX) #objective max

    def buildTree(self):
        self.root.createChildren([])

    def minMaxSearch(self):
        self.root.evaluate()

    def print(self):
        self.root.print()


class TicTacToe:
    def __init__(self, tree):
        self.tree = tree
        self.board = Board(tree.root)
        self.currentNode = tree.root
        self.gameover = 0
        self.buttons = {}
        self.label1 = None
        self.label2 = None
        self.turn = 'player'

        #init graphic intereface#
        self.init = tk.Tk()
        self.init.title("Jogo da Velha")
        self.window = tk.Frame(self.init) #create the window#
        self.window.pack()
        self.drawInterface()
        self.init.mainloop() #mantain the interface on a loop#

    def makeMove(self, child):
        self.board.positions[child.position] = MIN
        self.buttons[child.position]["text"] = "O"
        self.buttons[child.position]["fg"] = "#990099"
        self.turn = "player"
        self.currentNode = child
        return

    def chooseMove(self): #PC is MIN
        for child in self.currentNode.children:
            if child.evaluation == MIN: #try the winning situations first#
                self.makeMove(child)
                return
        for child in self.currentNode.children:
            if child.evaluation == 0: #try the draw situations then#
                self.makeMove(child)
                return
        for child in self.currentNode.children: #return some position#
            self.makeMove(child)
            return

    def restart(self):# restart the game#
        for i in range(0,9):
            self.buttons[i]["text"] = " "
        self.label1["text"] = "Sua vez!"
        self.label2["text"] = " "

        self.tree = tree
        self.board = Board(tree.root)
        self.currentNode = tree.root
        self.turn = 'player'
        self.gameover = 0

    def gameOver(self, value):
        if value == MAX:
            self.label2["text"] = "Você venceu!"
        elif value == MIN:
            self.label2["text"] = "Você perdeu!"
        elif value == 0:
            self.label2["text"] = "Empate!"
        self.label1["text"] = " "
        self.gameover = 1

    def check(self):
        board = Board(self.currentNode)
        result = board.checkWinner()
        if result == MIN:
            self.gameOver(MIN)
        elif result == MAX:
            self.gameOver(MAX)
        elif self.currentNode.level == 9:
            self.gameOver(0) #draw
        return

    def updateValue(self, i):
        if (self.turn == "player") & (self.buttons[i]["text"] == " ") & (self.gameover == 0):
            for child in self.currentNode.children:
                if child.position == i: #gets the child with the choosen position#
                    self.currentNode = child
            self.board.positions[i] = MAX #Player is MAX
            self.buttons[i]["text"] = "X"
            self.buttons[i]["fg"] = "#ff6600"
            self.turn = "PC"
            self.check()
            self.chooseMove()
            self.check()

    def drawText(self):
        label1 = tk.Label(self.init, text="Sua vez!", width=30, height=2, fg="white", bg=BACKGROUND_COLOR)
        label1.pack()
        self.label1 = label1
        label2 = tk.Label(self.init, text=" ", width=30, height=2, fg="white", bg=BACKGROUND_COLOR)
        label2.pack()
        self.label2 = label2

    def drawBoard(self):
        for i in range(0, MAX_DEPTH):  #draw all the buttons, we cant' directly pass the argument to a command without partial#
            button = tk.Button(self.window, text=" ", width=10, height=5, fg="white", bg=BUTTON_COLOR, command=partial(self.updateValue, i))
            button.grid(row=int(i / 3)+1, column=(i % 3))
            self.buttons[i] = button

    def drawInterface(self):
        self.init.configure(background=BACKGROUND_COLOR)
        self.window["bg"] = BACKGROUND_COLOR
        self.drawText()
        button = tk.Button(self.window, text="Reiniciar", width=10, height=2, fg="white", bg=RESTART_COLOR, command=self.restart)
        button.grid(row=0, column=2)
        self.drawBoard()

tree = Tree()
tree.buildTree()
tree.minMaxSearch()
game = TicTacToe(tree)
