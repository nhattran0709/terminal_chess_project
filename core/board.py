from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__ (self):
        self.en_passant_target = None #tracks en passant pawns

        self.chess_board = [ #this replicates how the board looks when you initialize a game
            [Rook("black"),Knight("black"),Bishop("black"),Queen("black"), King("black"),Bishop("black"),Knight("black"),Rook("black")], #basically a list of black chess pieces in their class form so i can check their legal moves
            [Pawn("black") for _ in range(8)],
            [" "] * 8,
            [" "] * 8,
            [" "] * 8,
            [" "] * 8,
            [Pawn("white") for _ in range(8)],
            [Rook("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"), Bishop("white"), Knight("white"), Rook("white")]#white chess pieces
        ]

    def take_input_move(self, square):
        # converts a square like "e4" into board indices (row, col), or None if it's invalid
        if len(square) != 2:
            return None
        col_char = square[0].lower()
        row_char = square[1]
        if not 'a' <= col_char <= 'h':
            return None
        if not '1' <= row_char <= '8':
            return None
        # try/except removed: the checks above already guarantee the input is safe to convert
        return (8 - int(row_char), ord(col_char) - ord('a'))

    def print_board(self):
        print("    a   b   c   d   e   f   g   h") #the letters representing each column
        print(" +---+---+---+---+---+---+---+---+")# grid lines
        for x in range(8):
            print(8-x, end="" ) #this is the numbered rows
            for y in range(8):
                if isinstance(self.chess_board[x][y], Piece):
                    print(f"| {self.chess_board[x][y].icon} ",end="") #prints a wall with a piece on the current board
                else:
                    print(f"| {self.chess_board[x][y]} ",end="")
            print("|")
            print(" +---+---+---+---+---+---+---+---+")#grid lines after each piece to make it look like a box
    
    def find_king(self,color):
        for r in range(8):
            for c in range(8):
                piece = self.chess_board[r][c]
                if isinstance(piece, King) and piece.color == color:
                    return r,c    

    def king_check (self, r_king, c_king, color):
        for r in range(8):
            for c  in range(8):
                piece = self.chess_board[r][c]
                if isinstance(piece, Piece) and piece.color != color:
                    if isinstance(piece, Pawn): #pawns are weird in checking because it only checks diagonally so I have to write an exception for pawns
                        if piece.color == "white":
                            direction = -1
                        else: 
                            direction = 1

                        for col_dir in (-1, 1):
                            if 0<= r + direction < 8 and 0<= c + col_dir<8: #checking board bounds
                                if (r + direction, c + col_dir) == (r_king, c_king): #if the diagonals have a king then the king is in check
                                    return True
                        continue #continue so the legal moves dont check pawns
                        
                    if isinstance(piece, King): #after a kings move, if the relative position of the 2 king's column and rows are either 0 or 1 apart then it would count as an illegal move as kings cannot be adjacent
                        if abs(r-r_king) <= 1 and abs (c-c_king) <= 1: 
                            return True
                        continue

                    if (r_king,c_king) in piece.legal_moves(r,c,self.chess_board):
                        return True
        return False

    def move_piece (self,start_move,end_move, color):

        if start_move.lower() == "castle":  #checks if input is castle
            rk, ck = self.find_king(color) 
            king = self.chess_board[rk][ck]  #finds king
            
            side = end_move.lower()
            if side not in ["kingside", "queenside"]:
                print("Invalid castle side! Enter 'kingside' or 'queenside'.") #invalid if not kingside or queenside
                return False
  
            if king.castle(self, side):
                print(f"{color.capitalize()} castled {side}!")
                self.en_passant_target = None  
                return True
            else:
                print("Cannot castle.")
                return False
        
        coords1 = self.take_input_move(start_move) #unpacks the tuple returned by take_input_move start_move is where the move the user wants start
        coords2 = self.take_input_move(end_move)# end_move is where the user wants the piece to end up

        if coords1 is None or coords2 is None:
            print("Invalid input. Use format like 'a2' or 'castle'.")
            return False

        row1, col1 = coords1
        row2, col2 = coords2

        start_piece = self.chess_board[row1][col1]
        old_has_moved = None
        if isinstance(start_piece, (King, Rook)):
            old_has_moved = start_piece.has_moved
        end_piece = self.chess_board[row2][col2]

        if start_piece == " ": #check if there is a piece in the starting position to move in the first place if there is no pieces then it will return nothing
            print("No piece there")
            return False
        
        if start_piece.color != color: #self explanatory
            print(f"Move {color} pieces only")
            return False
        
        if isinstance(end_piece, King) and end_piece.color != color:
            print("Cannot Take King") #cannot take king 
            return False
        
        if isinstance(start_piece, Pawn):
            legal_moves = start_piece.legal_moves(row1, col1, self.chess_board, self.en_passant_target)
        else:
            legal_moves = start_piece.legal_moves(row1,col1,self.chess_board)

        if (row2,col2) not in legal_moves: #check if the move is valid
            print("Illegal Move")
            return False
        
        old_ep = self.en_passant_target  # saved so the move can be undone if it leaves the king in check
        captured_ep = None  # will hold the pawn captured by en passant (if any)
        captured_row = None

        if isinstance(start_piece, Pawn) and self.en_passant_target == (row2, col2):
            if start_piece.color == "white":
                captured_row = row2 + 1
            else:
                captured_row = row2 - 1
            captured_ep = self.chess_board[captured_row][col2]  # remember it BEFORE removing it
            self.chess_board[captured_row][col2] = " "

        self.chess_board[row2][col2] = start_piece
        self.chess_board[row1][col1] = " "

        # a two-square pawn push creates a new en passant target, any other move clears it
        # (if/else replaces the two separate ifs that were here before)
        if isinstance(start_piece, Pawn) and abs(row2 - row1) == 2:
            self.en_passant_target = ((row1 + row2) // 2, col1)
        else:
            self.en_passant_target = None

        r_king, c_king = self.find_king(color)
        if self.king_check(r_king,c_king,color):
            print("King is in check") #if king is in check then it cannot run the move
            print("Illegal move")
            self.chess_board[row1][col1] = start_piece
            self.chess_board[row2][col2] = end_piece
            if captured_ep is not None:  # put back the pawn that en passant removed
                self.chess_board[captured_row][col2] = captured_ep
            self.en_passant_target = old_ep  # restore the en passant target from before this move

            if old_has_moved is not None:
                start_piece.has_moved = old_has_moved

            return False
        
        pawn_promotions_list = ["rook", "knight", "bishop", "queen"]
        
        if isinstance(start_piece, Pawn):
            if (start_piece.color == "white" and row2 == 0) or (start_piece.color == "black" and row2 == 7):
                while True:
                    promotion = input("What pawn promotion? (eg. rook, knight, bishop, queen): ").strip().lower()
                    if promotion in pawn_promotions_list:
                        index = pawn_promotions_list.index(promotion)
                        self.chess_board[row2][col2] = start_piece.promotion(start_piece.color, index)
                        print(f"Pawn promoted to {promotion}!")
                        break
                    else:
                        print("Invalid promotion name. Try again!")

        if isinstance(start_piece, (King, Rook)):
            start_piece.has_moved = True

        return True
    
    def no_legal_escapes (self,r1,c1, legal, color): #checking for pins and discovered checks
        start_piece = self.chess_board[r1][c1]

        for r,c in legal:
            end_piece = self.chess_board[r][c]

            captured_piece = None
            if isinstance(start_piece, Pawn) and self.en_passant_target == (r,c):
                if start_piece.color == "white":
                    captured_row = r + 1
                else:
                    captured_row = r - 1
                captured_piece = self.chess_board[captured_row][c]
                self.chess_board[captured_row][c] = " "

            self.chess_board[r][c] = start_piece
            self.chess_board[r1][c1] = " "
            r_king, c_king = self.find_king(color)

            if not self.king_check(r_king,c_king,color):
                self.chess_board[r1][c1] = start_piece #these codes are basically the king_check codes but it is now checking every move a person could take in a color then seeing if that move will result in a king check
                self.chess_board[r][c] = end_piece
                if captured_piece:
                    self.chess_board[captured_row][c] = captured_piece

                return False
            
            self.chess_board[r1][c1] = start_piece
            self.chess_board[r][c] = end_piece
            if captured_piece:
                self.chess_board[captured_row][c] = captured_piece

        return True
    
    def stalemate(self,color):
        r_king, c_king = self.find_king(color)
        king_check = self.king_check(r_king,c_king,color)

        if king_check:
            return False
        
        for r in range(8):
            for c  in range(8):
                piece = self.chess_board[r][c]
                if isinstance(piece, Piece) and piece.color == color:
                    if isinstance(piece, Pawn):
                        legal = piece.legal_moves(r,c,self.chess_board, self.en_passant_target)
                    else:
                        legal = piece.legal_moves(r,c,self.chess_board)
                    if not self.no_legal_escapes(r,c,legal,color): #same code as checkmate but the king is not in check
                        return False
        
        return True
    
    def position_key(self, side_to_move):
        # a hashable snapshot of the position, used as a dictionary key to count repeats
        # it stores icons instead of Piece objects so the key can be hashed and compared
        placement = tuple(
            tuple(p.icon if p != " " else " " for p in row)
            for row in self.chess_board
        )
        # a repeated position only counts if castling rights are the same too
        rights = []
        for r, c in [(7, 0), (7, 4), (7, 7), (0, 0), (0, 4), (0, 7)]:  # rook/king start squares
            p = self.chess_board[r][c]
            rights.append(isinstance(p, (King, Rook)) and not p.has_moved)
        # side_to_move and en_passant_target are part of the position too
        return (placement, side_to_move, tuple(rights), self.en_passant_target)

    def checkmate (self, color):
        r_king, c_king = self.find_king(color)
        king_check = self.king_check(r_king,c_king,color)

        if not king_check:
            return False

        for r in range(8):
            for c in range(8): #checks every piece
                piece = self.chess_board[r][c]
                if isinstance(piece, Piece) and piece.color == color:
                    if isinstance(piece, Pawn):
                        legal = piece.legal_moves(r,c,self.chess_board, self.en_passant_target)
                    else:
                        legal = piece.legal_moves(r,c,self.chess_board) #if there is no legal moves then it will mean checkmate + king is in check
                    if not self.no_legal_escapes (r,c,legal,color):
                        return False
        return True
