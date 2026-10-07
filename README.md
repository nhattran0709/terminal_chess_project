# terminal_chess_project
A two-player, text-based chess game in Python with full move validation, castling, en passant, promotion, and automatic game logs. Final Project for CICS110.

My final project is redesigning chess in python. My aim is to create a game which can run only
within python’s terminal and don’t need to do anything else.

There are a lot of designing processes that I started with. To begin with the code, I tried to
create the board first so that I can visualize where each piece is going. At first, I just used
functions to achieve this but I thought of using a class so I could add other methods within the
board. Since there are a lot of rules in chess, if I create a board class then I could implement
those rules and check them in the gameplay loop without making it too confusing.

The second thing that I focused on was the movement of pieces. At first, I created a list for the
board with only the chess icons but I realized that since each piece has their own movement it
would be confusing. So I created a class for the pieces then sub classes for each type of piece,
so pawn, king, queen, bishop, rook, knight. I thought of using sub classes because each piece
has a different movement but they are all “pieces” with color.

For the movement, I went with the legal moves approach to simplify it, so I just started with the
pawn and tried to see what moves it could make. First it can go forward if it's empty or eat the
enemy pieces if not. So I just followed that logic and appended all possible moves into its class
method of legal_moves. One thing I noticed is the direction of movement is different for white
and black pieces so I added a direction.

I followed this logic until I got to the bishop rook and queen pieces which can go as far as the
board can take them. This makes it harder but I had the direction idea and tried to see what
legal moves can go in one direction. Through this, I created the scanner which scans all
directions inputted in the function until it hits an enemy or ally piece or until the bounds. This
works perfectly as I could use it for bishop, rook and queen together.

The thing that gave me the most trouble was finding a good method for seeing the king_checks
because of pinning and discovered checks which made it very complicated and also the en
passant as it is quite hard to implement. I have done some testing on the code overall, but I feel
like a lot of the code is pretty rushed and there might be some bugs that I didn’t attend to.
If there were any further plans for the code, I would try to add a chess bot if I ever learned more
about algorithms and AI then I could make different varying levels of difficulty so it can be a
single player game. I think it would challenge my skills a lot and make the project more
interesting if I ever were to implement it.

To use the code, just need to press run and the gameplay loop goes by itself. There is a start
move which is what piece you want to move, that piece must be the same color as the person’s
turn. White is at the bottom while black is on top. The end move is where you want the thing to
go. After that, the game is just similar to chess with all of the rules implemented. There is also a move recorder that makes a txt file with all the moves during a game after the game ends.
