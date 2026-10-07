from .piece import Piece
from .rook import Rook

class King(Piece):
    def __init__ (self,color):
        super().__init__(color)
        if self.color == "black":
            self.icon = "♚"
        else:
            self.icon = "♔"
        self.has_moved = False #flag to check if castle is possible

    def legal_moves(self, r1,c1,board): #king can only go one block so I don't need to use scanner function from the Piece class
        legal = []  
        directions = [(-1,-1), (-1,0), (-1,1), # basically the directions the king could move, i format it this way so it is easier to visualize
                      (0,-1),          (0,1),
                      (1,-1),  (1,0),  (1,1)]
        
        for row_dir, col_dir in directions: #splits the tuple into the row direction it moves and the colum direction it moves and goes through the direcitons list to check each king move
            row_move, col_move = (r1 + row_dir, c1 + col_dir) #unpacking the tuple
            if 0 <= row_move < 8 and 0<= col_move < 8:
                target_move = board[row_move][col_move]
                if target_move == " " or target_move.color != self.color:  #if its not " " then it has to be apart of Piece class 
                    legal.append((row_move, col_move))

        return legal
    
    def castle(self, board, side):
        if self.has_moved: 
            return False
            
        r, c = board.find_king(self.color)
        
        # Determine path and rook position
        if side == "kingside": 
            rook_col = 7
            path = [(r, c+1), (r, c+2)]
        elif side == "queenside": 
            rook_col = 0
            path = [(r, c-1), (r, c-2), (r, c-3)]
        else:
            return False
        
        rook = board.chess_board[r][rook_col]
        
        # also check the rook's color so a promoted enemy rook in the corner can't be used to castle
        if not isinstance(rook, Rook) or rook.color != self.color or rook.has_moved: 
            return False
        
        # Check if path is clear
        for path_r, path_c in path: 
            if board.chess_board[path_r][path_c] != " ":
                return False

        # Check if King passes through check
        if board.king_check(r, c, self.color): # Check starting position
            return False
            
        if side == "kingside":
            check_squares = [(r,c), (r,c+1), (r,c+2)] #if it is kingside or the side with the king then these squares must be checked
        else:
            check_squares = [(r,c), (r,c-1), (r,c-2)]

        for sr, sc in check_squares:
            if board.king_check(sr, sc, self.color): #if a piece can check the king in these squares then castle is not allowed
                return False
            
        #moving the king
        board.chess_board[r][c] = " "
        if side == "kingside":
            new_king_col = c+2 #its new position in column
            new_rook_col = c+1
        else:
            new_king_col = c-2  
            new_rook_col = c-1
            
        board.chess_board[r][new_king_col] = self
        self.has_moved = True #makes sure that it is true so the king or rook cant castle again

        board.chess_board[r][rook_col] = " "
        board.chess_board[r][new_rook_col] = rook
        rook.has_moved = True
        return True