
from tkinter import *
import chess
import sys
import os

"""
This class stores the positions of the pieces. They are stored in a dictionary,
with the uci position as a key and the piece as a value. The pieces are denoted
by letters, but we can turn them to pngs later.  The black and white Positions
are seperate because the program will validate whether the right color is
playing.

In the entire code, board_move is a move that is input by UCI standards,
like e6f7, or a4c2, which is the raw input into the code.

uci_move is the type of move that py-chess accepts.
This might sounds counter-intuitice, but it makes it easier to keep track
because the function that converts from human-move to py-chess move
is called Move.from_uci. It takes a board_move and returns a uci_move
"""

class Positions(): #for backend
    def __init__(self):
        #this is the size of each square, which is generated in the GUI class
        self.square_size=64

        #these are the white positions
        self.whitePositions={'a1': "R", 'a2': 'P', 'b1': "N", 'b2': 'P', 'c1': "B",
        'c2': 'P', 'd1': "Q", 'd2': 'P', 'e1': "K", 'e2': 'P', 'f1': "B", 'f2':'P', 'g1': "N",
         'g2': 'P', 'h1': "R", 'h2': 'P'}

         #these are the black positions
        self.blackPositions={'a8': "R", 'a7': 'P', 'b8': "N", 'b7': 'P', 'c8': "B",
        'c7': 'P', 'd8': "Q", 'd7': 'P', 'e8': "K", 'e7': 'P', 'f8': "B", 'f7':'P', 'g8': "N",
         'g7': 'P', 'h8': "R", 'h7': 'P'}

        #these are used to convert uci squares to coordinates
        self.letterValue={'a':1,'b':2,'c':3,"d":4,'e':5,'f':6,'g':7,'h':8}

#this takes a square (e.g. e7f7), returns the centre coordinate of the square
#it doesn't need any validation because invalid input won't make it until here
    def square_centre(self,sq):
        l=sq[0] #letter of the square
        y_edge=float(sq[1]) #y cordinate of the square's bottom left edge
        x_edge=self.letterValue[l] #x cordinate of the square's bottom left edge
        x_centre=x_edge-0.5 #centre of the square using edge coordinate
        y_centre=y_edge-0.5#centre of the square using edge coordinate
        #multiples by the square size to find actual centre
        return x_centre*self.square_size, y_centre*self.square_size

#The following function changes the position of a piece by deleting
#the key value from the self.whitePositions or self.whitePositions,
#and adds the new values.

    def change_positions(self,move):
        old_sq=move[0:2] #initial square
        new_sq=move[2:4] #new square

        #the four lines will only do something if the move is a capture
        #deletes captured position
        #if this is not done, promotion and casting won't work right
        if new_sq in self.blackPositions:
            del self.blackPositions[new_sq]

        elif new_sq in self.whitePositions:
            del self.whitePositions[new_sq]

        #deletes square and piece of the right color
        #sets color to generate the same piece on a new square
        if old_sq in self.blackPositions:
            piece=self.blackPositions[old_sq]
            self.blackPositions[new_sq]=piece
            del self.blackPositions[old_sq]
            color="black" #used for generating piece.

        elif old_sq in self.whitePositions:
            piece=self.whitePositions[old_sq]
            self.whitePositions[new_sq]=piece
            del self.whitePositions[old_sq]
            color="white"#used for generating piece.
        else:
            #this means the input move is from an empty square
            #the error will be caught, and the user will be asked for new input
            raise ValueError("Piece not in positions")
        #returns piece and color, so the GUI can generate the right piece
        return piece,color



#takes board_move, returns square positions.
    def uci_to_square(self,board_move):

        old_sq=board_move[0:2] #old square
        new_sq=board_move[2:4] #new square

        f_cen=self.square_centre(old_sq)#centre of the previous square
        new_cen=self.square_centre(new_sq) #new centre

        piece,color=self.change_positions(board_move) #returns new piece position
        #returns a lot of things, but this is used only once,
        #and it makes that code  more simple to keep it like this
        return old_sq,new_sq,piece

#takes square, returns piece and color of piece if square is occupied,
#otherwise raises error
    def get_piece(self,pos):

        if pos in self.blackPositions:
            color="black"
            piece=self.blackPositions[pos]
        elif pos in self.whitePositions:
            color="white"
            piece=self.whitePositions[pos]
        else:
            #this means the move is from an empty square
            #this error will be caught elsewhere,
            #and the user will be asked to put in a new input
            raise ValueError('no such piece')
        #these will be used by the GUI to create a new piece in the new square
        return piece, color
