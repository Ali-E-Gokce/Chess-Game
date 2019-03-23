
from tkinter import *
import chess
import sys
import os
from positions import *

#Generates the GUI
class GUI():

    rows = 8 #rows and columns to generate chess board
    columns = 8
    color1 = "#DDB88C" #colors of the squares
    color2 = "#A66D4F"
    square_size = 64

    def __init__(self, parent): #generates canvas
    #generates board using py-chess.
    #This will be used under the hood to keep track of the game.
    #It does not create a GUI. Can be printed in ASCI.
        self.white_queen_castle=True #white has queenside castling rights
        self.white_king_castle=True #white has queenside castling rights
        self.black_queen_castle=True #black has queenside castling rights
        self.black_king_castle=True #black has kingside castling rights


        self.board = chess.Board()
        self.turn='white' #keeps track of the turn

        self.parent = parent
        parent.title("Chess")
        #this creates the chess board for py-chess

        #GUI configuration 
        canvas_width = (self.columns+4) * self.square_size
        canvas_height = (self.rows+4) * self.square_size

        self.canvas = Canvas(self.parent, width=canvas_width,
                                          height=canvas_height,
                                          background="white")

        self.canvas.grid(rowspan=10, columnspan=10)
        #Canvas,board background
        
        self.menubar = Menu(self.parent)#Menu Option, could include more features
        self.filemenu=Menu(self.menubar,tearoff=0)
        self.filemenu.add_command(label="Restart Game", command=self.game_restart)#Restart game option
        self.menubar.add_cascade(label="Option", menu=self.filemenu)
        self.parent.config(menu=self.menubar)

        self.label = Label(self.parent, text="Input command")#Indicate where to input
        self.label.grid(row=2,column=0)


        self.command = Entry(self.parent)#This creates the entry point
        self.command.grid(row=2,column=1)

        #Create buttons associated with methods
        self.close_button = Button(self.parent , text="Enter",
                                                 command=self.command_display)
        self.close_button.grid(row=2,column=2)

        self.close_button = Button(self.parent , text="Close",
                                                 command=self.exit_program)
        self.close_button.grid(row=2,column=3)

        #Create text box for info trace
        self.text=Text(self.parent,height = 40, width =25)
        self.text.grid(row=0,column=8)
        self.text.insert(1.0,"Command History\n")
        self.text.configure(state='disabled')#Unable external edit on the text box

        #this is used to keep track of the squares
        self.boardArr=[(chr(i),j) for i in range(97,105) for j in range(1,9)]

        #creates Positions object using Positions class
        self.positions=Positions()
        self.draw_board() #draws the board.


    def exit_program(self): #to exit the code
        sys.exit()
    #restarts the game by re-runnning the code
    def game_restart(self):
        python=sys.executable
        os.execl(python,python, *sys.argv)

    #displays the command history,
    #takes input move
    #validates if the moves are valid
    def command_display(self):

        board_move=self.command.get() #takes move

        self.text.configure(state='normal')

        #this validates the input
        #if the input is not valid, i.e. in the wrong format,
        #it will display invalid input and return
        #the user will have to input a new move
        #does not check of move is legal

        try:
            uci_move=chess.Move.from_uci(board_move)
        except:
            self.text.insert(END, "Invalid Input\n")
            return

        #checks if the move is castling or promotion
        #returns false or a move (as a string)
        unusual=self.is_unusual(board_move)
        #not executed if is_unusal is false, i.e. is not castling or promotion
        if unusual:
            board_move = unusual
            uci_move=chess.Move.from_uci(board_move)

        #checks if the move is legal under the current board state
        if self.is_legal(uci_move):
            pass

        #if it is not, it tells the user it is an invalid input,
        #and that they are under the check if they are
        else:
            if self.board.is_into_check(uci_move):
                self.text.insert(END, "%s is in check\n" % self.turn
                                    + "or this might be an illegal move\n")
            self.text.insert(END, "Invalid move\n")
            return

        #checks if the move is a capture
        #adjusts positions and gui accordingly if it is
        self.check_capture(uci_move,board_move)
        #moves the piece on the gui
        self.move_piece(board_move)
        #makes the move in the
        self.board.push(uci_move)
        self.text.insert(END,self.turn+" turn: "+board_move+"\n")
        self.turn = "white" if self.turn == "black" else "black"
        
        #After move, inform under check or game over, or game results
        if self.board.is_check():
                self.text.insert(END, self.turn + " is under check\n")

        if self.board.is_game_over():
            outcome=self.board.result()

            if outcome=='1-0':
                self.text.insert(END, "Checkmate!!\nWhite wins\n")
            elif outcome=='0-1':
                self.text.insert(END, "Checkmate!!\nBlack wins\n")
            else:
                self.text.insert(END, "Draw. Well played!")

            self.text.insert(END, score + " is the result\n")
            return
        
        #Print command 
        self.text.insert(END, "It's "+self.turn+" turn\n")
        self.text.configure(state='disabled')
        return



    def is_unusual(self,board_move): #unusual moves, promotion etc.
        #if the move is a promotion, this will return a string
        #if not, it will return false.
        sq=board_move[0:2] #the origin squares

        #checks if square is empty
        try:
            self.positions.get_piece(sq)
        except:
            self.text.insert(END, "That square is empty\n")
            return False
        #checks if  move is a promotion. Promotion moves have different syntax,
        # Returns the adjusted move if it is.
        # Returns false if it isn
        promotion_move=self.is_promotion(board_move)

        #Evaluates pnly if promotion move is a string, hence it is a promotion
        if promotion_move:
            board_move=promotion_move #changes move to adjusted promotion syntax

        #the function being called is enough to make a castling moves
        #it is as an elif statement for style, and to prevent it from being
        #run unnecessarily since no move can be both promotion and castling
        elif self.is_castling(board_move):
            pass
        #if move is neither promotion nor castling, returns false
        else:
            return False
        return board_move

    #checks if a given move is a promotion move
    def is_promotion(self,board_move):

        old_sq=board_move[0:2] #original square
        new_sq=board_move[2:4] #new square
        old_row=old_sq[1] #the row of the current posiiton
        new_row=new_sq[1] #row of the new position

        #type and color of the piece being moved
        piece,color=self.positions.get_piece(old_sq)

        #only pawns can be promoted
        if piece=="P":
            #black pieces can only be promoted when moving from row 2 to 1
            if color == "black" and new_row=='1' and old_row=='2':
                promoted_color=self.positions.blackPositions
            #white pieces can only be promoted when moving from row 8 to 7
            elif color == "white" and new_row=='8' and old_row=='7':
                promoted_color=self.positions.whitePositions
            else:
                return False
        else:
            return False

        #in uci protocol, promotion moves are normal moves followed by
        #the sign of the chosen promotion (Q,N,B,R)
        #if promotion input is not right syntax, will ask for new input
        if len(board_move)!=5:
            #more than 70 chars, but makes it more readable
            self.text.insert(END, "For promotion,please add your choice after the move.\n"+
            "q for queen, n for jumper, r for rook, b for bishop\n")
            return False

        #the new piece has the sign of the last characther of the promotion move
        new_piece=board_move[4]
        #adjusts the position object for the new piece
        promoted_color[old_sq]=new_piece.upper()
        #generates syntactically correct promotion move
        board_move=(old_sq+new_sq+new_piece)
        return board_move

    #checks if a move changes castling rights
    #if a piece has been moved, it can not be part of a castling ever again
    def castling_rights(self,board_move):
        moved=board_move[0:2]
        uci_move=chess.Move.from_uci(board_move)

        if moved=="e8" and self.is_legal(uci_move):
            self.black_king_castle=False
            self.black_queen_castle=False

        if moved=="e1" and self.is_legal(uci_move):
            self.white_king_castle=False
            self.white_queen_castle=False

        if moved=="h8" and self.is_legal(uci_move):
            self.black_king_castle=False

        if moved=="a8" and self.is_legal(uci_move):
            self.black_queen_castle=False

        if moved=="h1" and self.is_legal(uci_move):
            self.white_king_castle=False

        if moved=="a1" and self.is_legal(uci_move):
            self.white_queen_castle=False

        return

    #checks if a given move is a castling move
    #the function being called is enough to do the castling,
    #if it is a castling move
    def is_castling(self,board_move):
        uci_move=chess.Move.from_uci(board_move)
        row=board_move[3] #castling can only occur on the last row of the board

        #checks if the type of castling is allowed in the current board state
        if self.board.is_kingside_castling(uci_move):
            if row == '1': #all white castlings happen in row 1
                if self.white_king_castle: #checks for proper castling right
                    self.move_piece("h1f1")
            if row == '8': #all black casltings happen in row 8
                if self.black_king_castle:#checks for proper castling right
                    self.move_piece("h8f8")
            else:
                self.text.insert(END, "%s has already used their castling\n"
                                                                % self.turn)

        elif self.board.is_queenside_castling(uci_move):
            if row == '1':
                if self.white_queen_castle:
                    self.move_piece("a1d1")
            if row == '8':
                if self.black_queen_castle:
                    self.move_piece("a8d8")
            else:
                self.text.insert(END, "%s has already used their castling\n"
                                                                % self.turn)
        #updates castling rights
        self.castling_rights(board_move)
        return board_move

    #checks if a move is legal under current board state
    def is_legal(self,uci_move):
        if uci_move in self.board.legal_moves:
            return True
        else:
            return False

    #checks if a move is a capture, and makes proper adjustments if it is
    #do not use is_capture, will cause as py-chess bug
    def check_capture(self,uci_move,board_move):
        if self.board.is_capture(uci_move)==True: #this includes en passant
            if self.board.is_en_passant(uci_move): #checks if en passant
                #square where the captured piece is
                sq=self.capture_en_passant(board_move)#
                self.canvas.delete(sq) #removes piece that was captured
            elif not self.board.is_en_passant(uci_move) :
                sq=board_move[2:4] #square where the captured piece is
                self.canvas.delete(sq) #removes piece
        return

    #in an en passant capture, the square that will be removed is not the
    #square that the new move is moving to
    #this returns the square of the en passante captured piece
    def capture_en_passant(self,board_move):
        new_sq=board_move[2:4]#square being moved to
        letter=new_sq[0]#letter of that square
        number=int(new_sq[1])#number of the square as an integer
        #if turn is white, captured piece is above moved square
        if self.turn=="white":
            number-=1
        #if turn is black, captured piece is below moved square
        if self.turn=="black":
            number+=1
        #converts number to string for new square
        number=str(number)
        captured_sq=letter+number
        return captured_sq

#same as Positions.square_centre
    def square_centre(self,s): #takes square as an argument, TODO validation

        l=s[0] #letter
        y_edge=float(s[1]) #y cordinate of the squares bottom left edge
        x_edge=self.positions.letterValue[l] #x cordinate of the squares bottom left edge

        x_centre=x_edge-0.5#takes the centre x coordinate of the square
        y_centre=y_edge-0.5#takes the centre y coordinate of the square
        #returns coordinates of the middle of the square
        return x_centre*self.square_size, y_centre*self.square_size

     #draws the board. The first 17 lines
     #have been taken from an online 'how to make
     #a chess game in python' turtorial I found on O'Reily.
     #the rest we made ourselves to adjust to our game

    def draw_board(self):
        color = self.color2
        for r in range(self.rows):#creates rows
            if color==self.color2: #switches color to make board pattern
                color=self.color1
            else:
                color=self.color2
            #creates rectangles
            for c in range(self.columns):
                x1 = (c * self.square_size)
                y1 = ((7-r) * self.square_size)
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                color = self.color1 if color == self.color2 else self.color2

        ucis=self.boardArr
        for i in range(self.rows): #this writes a-h 1-8 next to the squares
            #adding 0.5 to the position puts it in the centre of the square
            self.canvas.create_text((i+0.5)* self.square_size,  8.5* self.square_size,font="Times 40 bold", text=ucis[8*i][0])
            self.canvas.create_text((8.5)* self.square_size,  (i+0.5)* self.square_size,font="Times 40 bold", text=i+1)

        self.draw_pieces() #draws the pieces on the board

    def draw_pieces(self): #draws the pieces

        whites=self.positions.whitePositions #white positions and pieces
        blacks=self.positions.blackPositions #black positions and pieces

        #generates pieces in the right squares
        #tag is used for removing a piece from the square when needed
        for pos  in whites:
            x,y=self.positions.square_centre(pos) #gets centre of the square
            pos=self.canvas.create_text(x,y ,font="Times 20 bold",
            text=whites[pos], fill="white", tag=pos)



        for pos  in blacks:
            x,y=self.positions.square_centre(pos)
            pos=self.canvas.create_text(x,y ,font="Times 20 bold",
            text=blacks[pos],fill="black",  tag=pos)

    #moves piece in the GUI
    def move_piece(self,board_move):
        #There was no simple way to split this into smaller functions
        #old_sq and new_sq are tuples consisting of the x-y coirdinates
        #piece is the piece (P for pawn)
        #old_sq is the tag used to remove the moved piece from gui
        old_sq,new_sq,piece=self.positions.uci_to_square(board_move)
        x,y= self.square_centre(new_sq)
        self.canvas.delete(old_sq)#deletes piece that was moved, using the tag
        #fill is the color, text piece type,
        self.canvas.create_text(x, y, font="Times 20 bold",
                                      fill=self.turn, text=piece,tag=new_sq)
