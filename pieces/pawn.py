from .piece import Piece
from .rook import Rook
from .knight import Knight
from .bishop import Bishop
from .queen import Queen

class Pawn(Piece):
    def __init__ (self,color):
        super().__init__(color)
        if self.color == "black":
            self.icon = "♟"
        else:
            self.icon = "♙"

    def legal_moves(self,r1,c1,board, en_passant_target =None):
        legal = []

        if self.color == "white": #if white then the direction is upwards
            direction = -1
        else:
            direction = 1 #if black then pawn moves downwards
        
        if self.color == "white": #starts at 6 because the array is from top down so white is below which means its at the 7th index
            start_row = 6
        else:
            start_row = 1 #starts at the 2nd index in the board array

        next_row = r1 + direction

        if 0<= next_row <8:
        
            forward = board[next_row][c1] #pawn moves weird so I don't use scanner function inside pawn but insteaad make a new system

            if forward == " ": #forward movement only if square is empty
                legal.append((next_row,c1))
                if r1 == start_row:
                    forward_2 = r1 + (2*direction)
                    if board[forward_2][c1] == " " and forward == " ":
                        legal.append((forward_2,c1))
            if 0<=c1 + 1 < 8:
                up_diag1 = board[next_row][c1+1]
                if up_diag1 != " " and up_diag1.color != self.color: #if the diagonal space is not empty so a piece is there and is an enemy color, the pawn can take
                    legal.append((next_row,c1+1))
            if 0<= c1 -1 < 8:
                up_diag2 = board[next_row][c1-1]
                if up_diag2 != " " and up_diag2.color != self.color: #same with the one above for the other diagonal square
                    legal.append((next_row,c1-1))

            if en_passant_target: #if there is an enpassant target
                ep_row, ep_col = en_passant_target
                if next_row == ep_row and abs(ep_col - c1) == 1: #if the enpassant piece is on the same row and adjacent column then taking the pawn is legal
                    legal.append((next_row, ep_col))

        return legal

    def promotion(self, color, index):
        promotions = [Rook(color), Knight(color), Bishop(color), Queen(color) ] #promotions list and it follows the index given and it will return the class that you want the pawn to evolve to
        return promotions[index]