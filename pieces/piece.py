class Piece:
    def __init__ (self, color):
        self.color = color

    def scanner (self, r, c, row_dir, col_dir, board):
        moves = [] #scans in one direction to stops when there is a Piece
        r += row_dir #used for bishop queen rook since they can move as far as possible
        c += col_dir
        while 0 <= r < 8 and 0 <= c < 8: #checking the b ounds of rows and columns
            target_move = board[r][c] #the target move or the next move it is going
            if target_move == " ":
                moves.append((r, c))  #if empty then means it is legal
            elif target_move.color != self.color: #if diffenret color then it is enemy so the piece can take
                moves.append((r, c))
                break      #breaks because it can only take and the moves further than that is illegal
            else:
                break     

            r += row_dir #iterates until the loop breaks to "scan" the  board in that direction
            c += col_dir
        return moves #returns the moves list