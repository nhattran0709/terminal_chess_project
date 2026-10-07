from .piece import Piece

class Bishop(Piece):
    def __init__ (self,color):
        super().__init__(color)
        if self.color == "black":
            self.icon = "♝"
        else:
            self.icon = "♗"

    def legal_moves(self,r1,c1,board):
        legal = [] 
        directions = [(-1,-1), (-1,1), # bishop is same as queen but only moves in diagonals
                      (1,-1),  (1,1)] # so i remove sideways and updown from directions
        for row_dir, col_dir in directions:
            legal.extend(self.scanner(r1,c1,row_dir,col_dir,board)) #uses scanner from main class Piece
        return legal
    