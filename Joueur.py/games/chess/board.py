from string import ascii_lowercase


class Board:
    DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __init__(self, fen=DEFAULT_FEN):
        fen = fen.split()

        self.pieces = {"white": [], "black": []}
        self._board = self.fen2board(fen[0])
        self.turn = fen[1]
        self.castle = fen[2]
        self.en_passant = fen[3]
        self.halfmove_clock = int(fen[4])
        self.fullmove_counter = int(fen[5])

    def get_piece(self, x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            return self._board[y][x]

        raise IndexError

    def print(self):
        print("   +" + '-'*24 + '+')

        for i, rank in enumerate(self._board):
            print(" {} |".format(8-i), end='')

            for piece in rank:
                print(" {} ".format(piece or '.'), end='')

            print('|')

        print("   +" + '-'*24 + '+')
        print("     " + "  ".join(list(ascii_lowercase)[:8]))

    def fen2board(self, fen):
        board = []
        fen = fen.split('/')

        for y in range(len(fen)):
            rank = []

            for x in range(len(fen[y])):
                if fen[y][x].isdigit():
                    rank.extend([None for _ in range(int(fen[y][x]))])
                else:
                    color = "white" if fen[y][x].isupper() else "black"
                    piece = Piece(self, len(rank), y, fen[y][x], color)

                    rank.append(piece)
                    self.pieces[color].append(piece)

            board.append(rank)

        return board


class Piece:
    def __init__(self, board, x, y, type, color, has_moved=False):
        self.board = board
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.has_moved = has_moved

    def __str__(self):
        return self.type

    def _get_diagonal_moves(self, start_x, end_x, step_x, start_y, end_y, step_y):
            legal_moves = []
            board = self.board

            for x, y in zip(range(start_x, end_x, step_x), range(start_y, end_y, step_y)):
                move = x, y

                try:
                    piece = board.get_piece(*move)

                    if not piece:
                        legal_moves.append(move)
                        continue
                    
                    if self.is_enemy(piece):
                        legal_moves.append(move)
                        return legal_moves
                    else:
                        return legal_moves
                except IndexError:
                    pass

            return legal_moves

    def _get_horizontal_moves(self, start, end, step):
        legal_moves = []
        board = self.board

        for x in range(start, end, step):
            move = x, self.y

            try:
                piece = board.get_piece(*move)

                if not piece:
                    legal_moves.append(move)
                    continue
                
                if self.is_enemy(piece):
                    legal_moves.append(move)
                    return legal_moves
                else:
                    return legal_moves
            except IndexError:
                pass

        return legal_moves

    def _get_vertical_moves(self, start, end, step):
        legal_moves = []
        board = self.board

        for y in range(start, end, step):
            move = self.x, y

            try:
                piece = board.get_piece(*move)

                if not piece:
                    legal_moves.append(move)
                    continue
                
                if self.is_enemy(piece):
                    legal_moves.append(move)
                    return legal_moves
                else:
                    return legal_moves
            except IndexError:
                pass

        return legal_moves

    # TODO: implement en passant and promotion
    def _get_pawn_moves(self):
        moves = []
        board = self.board
        x, y = self.x, self.y

        if self.color == "white":
            # check up 1
            try:
                piece = board.get_piece(x, y-1)

                if not piece:
                    moves.append((x, y-1))
                    
                    try:
                        piece = board.get_piece(x, y-2)

                        if not self.has_moved and not piece:
                            moves.append((x, y-2))
                    except IndexError:
                        pass

            except IndexError:
                pass

            # check up 1, left 1
            try:
                piece = board.get_piece(x-1, y-1)

                if piece and self.is_enemy(piece):
                    moves.append((x-1, y-1))
            except IndexError:
                pass

            # check up 1, right 1
            try:
                piece = board.get_piece(x+1, y-1)

                if piece and self.is_enemy(piece):
                    moves.append((x+1, y-1))
            except IndexError:
                pass
        else:
            # check down 1
            try:
                piece = board.get_piece(x, y+1)

                if not piece:
                    moves.append((x, y+1))
                    
                    try:
                        piece = board.get_piece(x, y+2)

                        if not self.has_moved and not piece:
                            moves.append((x, y+2))
                    except IndexError:
                        pass

            except IndexError:
                pass

            # check down 1, right 1
            try:
                piece = board.get_piece(x+1, y+1)

                if piece and self.is_enemy(piece):
                    moves.append((x+1, y+1))
            except IndexError:
                pass

            # check down 1, left 1
            try:
                piece = board.get_piece(x-1, y+1)

                if piece and self.is_enemy(piece):
                    moves.append((x-1, y+1))
            except IndexError:
                pass

        return moves

    def _get_knight_moves(self):
        legal_moves = []
        board = self.board
        x, y = self.x, self.y

        possible_moves = (
            (x+1, y-2), # right 1, up 2
            (x+2, y-1), # right 2, up 1
            (x+2, y+1), # right 2, down 1
            (x+1, y+2), # right 1, down 2
            (x-1, y+2), # left 1, down 2
            (x-2, y+1), # left 2, down 1
            (x-2, y-1), # left 2, up 1
            (x-1, y-2)  # left 1, up 2
        )

        for move in possible_moves:
            try:
                piece = board.get_piece(*move)
     
                if not piece or self.is_enemy(piece): 
                    legal_moves.append(move)
            except IndexError:
                pass

        return legal_moves

    def _get_bishop_moves(self):
        legal_moves = []
        board = self.board
        x, y = self.x, self.y

        # check right-up
        legal_moves.extend(self._get_diagonal_moves(
            x+1, 8, 1, y-1, -1, -1))

        # check right-down
        legal_moves.extend(self._get_diagonal_moves(
            x+1, 8, 1, y+1, 8, 1))

        # check left-down
        legal_moves.extend(self._get_diagonal_moves(
            x-1, -1, -1, y+1, 8, 1))

        # check left-up
        legal_moves.extend(self._get_diagonal_moves(
            x-1, -1, -1, y-1, -1, -1))

        return legal_moves

    def _get_rook_moves(self):
        legal_moves = []
        board = self.board

        # get right
        legal_moves.extend(self._get_horizontal_moves(self.x+1, 8, 1))

        # get down
        legal_moves.extend(self._get_vertical_moves(self.y+1, 8, 1))

        # get left
        legal_moves.extend(self._get_horizontal_moves(self.x-1, 0, -1))

        # get up
        legal_moves.extend(self._get_vertical_moves(self.y-1, 0, -1))
        
        return legal_moves

    def _get_queen_moves(self):
        # queen moves are just bishop + rook moves
        return self._get_bishop_moves() + self._get_rook_moves()

    # TODO: implement castling
    def _get_king_moves(self):
        legal_moves = []
        board = self.board
        
        for y in range(self.y-1, self.y+2):
            for x in range(self.x-1, self.x+2):
                if not (x == self.x and y == self.y):
                    move = x, y

                    try:
                        piece = board.get_piece(*move)

                        if not piece or self.is_enemy(piece):
                            legal_moves.append(move)
                    except IndexError:
                        pass

        return legal_moves

    def get_moves(self):
        PIECE_MAP = {
            'p': self._get_pawn_moves,
            'n': self._get_knight_moves,
            'b': self._get_bishop_moves,
            'r': self._get_rook_moves,
            'q': self._get_queen_moves,
            'k': self._get_king_moves
        }

        return PIECE_MAP[self.type.lower()]()

    def move(self, x, y):
        pass

    def is_enemy(self, other):
        return self.color != other.color

class Player:
    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.pieces = board.pieces[color]


#board = Board("rnbqkbnr/pppppppp/1P6/8/8/8/P1PPPPPP/RNBQKBNR w KQkq - 0 1")
board = Board("1nb3nr/pppppppp/r2q1b2/8/8/4k3/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
#board = Board()
board.print()
print(board.get_piece(5, 2).get_moves())
print(board.get_piece(0, 1).get_moves())
print(board.get_piece(1, 0).get_moves())
print(board.get_piece(0, 2).get_moves())
print(board.get_piece(3, 2).get_moves())
print(board.get_piece(4, 5).get_moves())
