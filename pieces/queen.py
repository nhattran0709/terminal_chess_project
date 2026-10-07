from .piece import Piece

class Queen(Piece):
    def __init__ (self,color):
        super().__init__(color)
        if self.color == "black":
            self.icon = "♛"
        else:
            self.icon = "♕"
        
    def legal_moves(self,r1,c1,board):
        legal = [] 
        directions = [(-1,-1), (-1,0), (-1,1), # the direcitons the queen could move, i format it this way so it is easier to visualize
                      (0,-1),          (0,1),
                      (1,-1),  (1,0),  (1,1)]
        for row_dir, col_dir in directions:
            legal.extend(self.scanner(r1,c1,row_dir,col_dir,board))
        return legal