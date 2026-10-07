from core import Board, MoveRecorder

def gameplay_loop():
    print("Welcome to Chess")
    board = Board()
    recorder = MoveRecorder()  # records every successful move so it can be saved at the end
    board.print_board()
    turns = 0
    # counts how many times each position has happened (replaces the old Turns_board list)
    positions = {board.position_key("white"): 1}

    while True:
        print("White's Turn")
        while True:
            start = input("Start move (e.g. e2 or 'castle'): ").strip()
            if start.lower() == "castle":
                end = input("Side (kingside/queenside): ").lower()
            else:
                end = input("End move (e.g. e4): ").strip()

            if board.move_piece(start, end, "white"):
                recorder.record("white", f"{start} {end}")  # only record moves that were actually legal
                break

        board.print_board()
        turns += 1

        # checkmate and stalemate are tested BEFORE the move limit so a mate on the last ply still counts
        if board.checkmate("black"):
            print("Checkmate! White wins")
            break

        if board.stalemate("black"):
            print("Stalemate! No one wins!")
            break

        key = board.position_key("black")  # black is the side to move next
        positions[key] = positions.get(key, 0) + 1
        if positions[key] >= 3:  # third occurrence of the same position = draw
            print("Draw by threefold repetition")
            break

        if turns >= 100:
            print("Draw: move limit reached")  # now prints a message instead of quitting silently
            break

        print("Black's Turn")
        while True:
            start = input("Start move (e.g. e7 or 'castle'): ").strip()
            if start.lower() == "castle":
                end = input("Side (kingside/queenside): ").lower()
            else:
                end = input("End move (e.g. e5): ").strip()

            if board.move_piece(start, end, "black"):
                recorder.record("black", f"{start} {end}")
                break

        board.print_board()
        turns += 1

        if board.checkmate("white"):
            print("Checkmate! Black wins")
            break

        if board.stalemate("white"):
            print("Stalemate! No one wins!")
            break

        key = board.position_key("white")  # white is the side to move next
        positions[key] = positions.get(key, 0) + 1
        if positions[key] >= 3:
            print("Draw by threefold repetition")
            break

        if turns >= 100:
            print("Draw: move limit reached")
            break

    recorder.save()  # writes the move list to the next free file (game1.txt, game2.txt, ...) once the game is over


if __name__ == "__main__":  # only start the game when the file is run directly, not when imported
    gameplay_loop()

