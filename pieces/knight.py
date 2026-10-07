from .piece import Piece

class Knight(Piece):
    def __init__ (self,color):
        super().__init__(color)
        if self.color == "black":
            self.icon = "♞"
        else:
            self.icon = "♘"
    
    def legal_moves(self,r1,c1,board):
        legal = []
        directions = [(-1, -2), (-2,-1), (-2,1), (-1,2),
                      (1,-2), (2,-1), (2,1), (1,2)] #moves in Lshape so I made all the possible directions the knight could go
        for row_dir, col_dir in directions:#sharing the same code with king 
            row_move, col_move = (r1 + row_dir, c1 + col_dir) #unpacking the tuple 
            if 0 <= row_move < 8 and 0<= col_move < 8:
                target_move = board[row_move][col_move]
                if target_move == " " or target_move.color != self.color:  #if its not " " then it has to be apart of Piece class 
                    legal.append((row_move, col_move))
            
        return legal


    
