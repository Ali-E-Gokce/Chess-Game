The game is run from play_chess.py

This is a GUI chess game, written in Python. It uses the
python-chess module, which needs to be installed for the code
to run. It can be downloaded via:
sudo pip3 install python-chess

More information regarding python-chess can be found in:
pypi.org/project/python-chess/

The code was tested in Python 3.7.2
We tried using functions in Tkinter that would also work
on Python2, but we have not tested that and do not guarantee
it would work properly, or run at all on older versions.

All squares on the board are denoted by a letter from A-H
and a number 1-8.

The code takes a UCI protocol move as input, which is usually
a four character string, with the first two chars denoting
the square the piece is being moved from, and the second
two chars being the square you are moving to. The characters
are all lower case.

To move from A1 to H8. the user would input a1h8.

There are two unusual cases here.
If a move is a promotion move, the regular UCI expression
will be followed by a character denoting what piece
the user wants to promote to, q for Queen, n for Knight,
r for Rook and b for Bishop. If the user tries to put in a
regular move, the program will prompt them to add their
choice of promotion. To promote a piece to a Queen,
the move would be g7h8q.

If a move is castling move, the input is the King moving two
square to the left for a kingside castling, and two squares
to the left for a queenside castling.

The game ends when the game is over for any chess condition,
with the exception of the fifty-move and the
threefold-repetition rule. The latter can be very time consuming
to check.

You can restart the game from the top left drop down bar.
