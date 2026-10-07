from .piece import Piece

class Rook(Piece):
    def __init__ (self,color):
        super().__init__(color)
        if self.color == "black":
            self.icon = "♜"
        else:
            self.icon = "♖"
        self.has_moved = False #flag for checking if castle is possible

    def legal_moves(self,r1,c1,board):
        legal = [] 
        directions = [ (-1,0),# rook is same as queen except diagonals
                      (0,-1), (0,1), # i removed diagonals from the direction
                      (1,0)]
        for row_dir, col_dir in directions:
            legal.extend(self.scanner(r1,c1,row_dir,col_dir,board))
        return legal