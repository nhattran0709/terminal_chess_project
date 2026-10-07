import os

class MoveRecorder:
    def __init__(self): 
        self.moves = [] #the moves list to see what moves are played

    def record(self, color, move_text): #records one move with its color label, e.g. "White: e2 e4"
        self.moves.append(f"{color.capitalize()}: {move_text}") #capitalize turns "white" into "White" so no if/else is needed

    def save(self, filename=None): #writes one line per turn, with White's move first and Black's move after it
            if filename is None: #no name given, so pick the next free one: game1.txt, game2.txt, ...
                game_number = 1
                while os.path.exists(f"game{game_number}.txt"): #keeps counting up until it finds a name that isn't taken
                    game_number += 1
                filename = f"game{game_number}.txt"

            with open(filename, "w", encoding="utf-8") as f:
                for i in range(0, len(self.moves), 2): #steps through the list two moves at a time (white, then black)
                    turn = i // 2 + 1 #turn number: moves 0,1 are turn 1, moves 2,3 are turn 2, etc.
                    line = f"{turn}. {self.moves[i]}" #white's move
                    if i + 1 < len(self.moves): #black may not have moved yet if the game ended on white's move
                        line += f"   {self.moves[i + 1]}" #black's move goes on the same line
                    f.write(line + "\n")

            print(f"Game saved to {filename}") #tells the player which file their game went into
