from string import ascii_lowercase
from copy import copy


class Board:
    DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __init__(self, fen=DEFAULT_FEN):
        fen = fen.split()

        self._board, self.pieces = self.fen2board(fen[0])
        self.turn = fen[1]
        self.castle = fen[2]
        self.en_passant = fen[3]
        self.halfmove_clock = int(fen[4])
        self.fullmove_counter = int(fen[5])

    def copy(self):
        new = copy(self)
        new._board, new.pieces = self.fen2board(self.board2fen())

        return new

    def get_piece(self, x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            return self._board[y][x]

        raise IndexError

    def set_piece(self, x, y, piece):
        # remove our piece from original position
        self._board[self.y][self.x] = None

        # remove enemy piece if captured
        if self._board[y][x]:
            del self.piece[color][id]

        # update board to new piece position
        self._board[y][x] = piece

        # update piece x and y values to new position
        self.x, self.y = x, y

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
        pieces = {"White": {}, "Black": {}}
        fen = fen.split('/')
        id = 0

        for y in range(len(fen)):
            rank = []

            for x in range(len(fen[y])):
                if fen[y][x].isdigit():
                    rank.extend([None for _ in range(int(fen[y][x]))])
                else:
                    # if uppercase, piece is white
                    if fen[y][x].isupper():
                        color = "White"
                        enemy_color = "Black"
                    # black otherwise
                    else:
                        color = "Black"
                        enemy_color = "White"

                    piece = Piece(self, id, len(rank), y, fen[y][x].lower(), color, enemy_color)

                    rank.append(piece)
                    pieces[color][id] = piece
                    id += 1

            board.append(rank)

        return board, pieces

    def board2fen(self):
        fen = []

        for row in self._board:
            counter = 0
            section = ""

            for p in row:
                if p:
                    if counter > 0:
                        section += str(counter)
                        counter = 0

                    section += str(p)
                else:
                    counter += 1

            if counter > 0:
                section += str(counter)

            fen.append(section)

        return '/'.join(fen)

    def get_new_state(self):
        return Board(self.board2fen())


class Piece:
    def __init__(self, board, id, x, y, type, color, enemy_color, has_moved=False):
        self.board = board
        self.id = id
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.enemy_color = enemy_color
        self.has_moved = has_moved

    def __str__(self):
        return self.type if self.color == "Black" else self.type.upper()

    def __repr__(self):
        return str(self)

    def _get_diagonal_moves(self, start_x, end_x, step_x, start_y, end_y, step_y):
        legal_moves = []
        board = self.board

        # for every diagonal x and y coordinate
        for x, y in zip(range(start_x, end_x, step_x), range(start_y, end_y, step_y)):
            move = x, y

            try:
                piece = board.get_piece(*move)

                # if square is empty
                if not piece:
                    legal_moves.append(move)

                # else if square has an enemy piece
                elif self.is_enemy(piece):
                    legal_moves.append(move)
                    return legal_moves

                # else square has a friendly piece
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

                # if square is empty
                if not piece:
                    legal_moves.append(move)

                # else if square has an enemy piece
                elif self.is_enemy(piece):
                    legal_moves.append(move)
                    return legal_moves

                # else square has a friendly piece
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

                # if square is empty
                if not piece:
                    legal_moves.append(move)

                # else if square has an enemy piece
                elif self.is_enemy(piece):
                    legal_moves.append(move)
                    return legal_moves

                # else square has a friendly piece
                else:
                    return legal_moves

            except IndexError:
                pass

        return legal_moves

    # TODO: implement en passant
    def _get_pawn_moves(self):
        moves = []
        board = self.board
        x, y = self.x, self.y

        if self.color == "White":
            # check movement north 1
            move = x, y-1

            try:
                piece = board.get_piece(*move)

                if not piece:
                    moves.append(move)

                    # if pawn has not yet moved, check movement north 2
                    if not self.has_moved:
                        move = x, y-2
                        
                        try:
                            board.get_piece(*move)
                            moves.append(move)

                        except IndexError:
                            pass

            except IndexError:
                pass

            possible_captures = (
                (x-1, y-1), # west 1, north 1
                (x+1, y-1)  # east 1, north 1
            )

            # check possible captures
            for capture in possible_captures:
                try:
                    piece = board.get_piece(*move)

                    if piece and self.is_enemy(piece):
                        moves.append(move)

                except IndexError:
                    pass
        else:
            # check movement south 1
            move = x, y+1

            try:
                piece = board.get_piece(*move)

                if not piece:
                    moves.append(move)

                    # if pawn has not yet moved, check movement south 2
                    if not self.has_moved:
                        move = x, y+2
                        
                        try:
                            board.get_piece(*move)
                            moves.append(move)

                        except IndexError:
                            pass

            except IndexError:
                pass

            possible_captures = (
                (x-1, y+1), # west 1, south 1
                (x+1, y+1)  # east 1, south 1
            )

            # check possible captures
            for capture in possible_captures:
                try:
                    piece = board.get_piece(*move)

                    if piece and self.is_enemy(piece):
                        moves.append(move)

                except IndexError:
                    pass

        return moves

    def _get_knight_moves(self):
        legal_moves = []
        board = self.board
        x, y = self.x, self.y

        possible_moves = (
            (x+1, y-2), # east 1, north 2
            (x+2, y-1), # east 2, north 1
            (x+2, y+1), # east 2, south 1
            (x+1, y+2), # east 1, south 2
            (x-1, y+2), # west 1, south 2
            (x-2, y+1), # west 2, south 1
            (x-2, y-1), # west 2, north 1
            (x-1, y-2)  # west 1, north 2
        )

        # check possible moves
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
        x, y = self.x, self.y

        # check northeast
        legal_moves.extend(self._get_diagonal_moves(x+1, 8, 1, y-1, -1, -1))

        # check southeast
        legal_moves.extend(self._get_diagonal_moves(x+1, 8, 1, y+1, 8, 1))

        # check southwest
        legal_moves.extend(self._get_diagonal_moves(x-1, -1, -1, y+1, 8, 1))

        # check northwest
        legal_moves.extend(self._get_diagonal_moves(x-1, -1, -1, y-1, -1, -1))

        return legal_moves

    def _get_rook_moves(self):
        legal_moves = []
        x, y = self.y, self.x

        # check east
        legal_moves.extend(self._get_horizontal_moves(x+1, 8, 1))

        # check south
        legal_moves.extend(self._get_vertical_moves(y+1, 8, 1))

        # check west
        legal_moves.extend(self._get_horizontal_moves(x-1, 0, -1))

        # check north
        legal_moves.extend(self._get_vertical_moves(y-1, 0, -1))
        
        return legal_moves

    def _get_queen_moves(self):
        # queen moves are just bishop + rook moves
        return self._get_bishop_moves() + self._get_rook_moves()

    # TODO: implement castling
    def _get_king_moves(self):
        legal_moves = []
        
        # check adjacent squares (+2 because range upper bound is exclusive)
        for y in range(self.y-1, self.y+2):
            for x in range(self.x-1, self.x+2):
                # if not the square we're in
                if not (x == self.x and y == self.y):
                    move = x, y

                    try:
                        piece = self.board.get_piece(*move)

                        if not piece or self.is_enemy(piece):
                            legal_moves.append(move)

                    except IndexError:
                        pass

        return legal_moves

    def in_check(self):
        # for every enemy piece
        for piece in self.board.pieces[self.enemy_color]:
            # for every possible move
            for move in piece.get_moves():
                # if enemy can move to king location, we're in check
                if (self.x, self.y) == (piece.x, piece.y):
                    return True

        return False

    def get_moves(self):
        PIECE_MAP = {
            'p': self._get_pawn_moves,
            'n': self._get_knight_moves,
            'b': self._get_bishop_moves,
            'r': self._get_rook_moves,
            'q': self._get_queen_moves,
            'k': self._get_king_moves
        }

        return Piece.PIECE_MAP[self.type.lower()]()

    def move(self, file, rank, promotion_type=""):
        x, y = fr2coord(file, rank)

        self.board.set_piece(x, y, self)
        self.has_moved = True

        if promotion_type:
            self.type = promotion_type

    def is_enemy(self, other):
        return self.color != other.color

    @staticmethod
    def coord2fr(x, y):
        return ascii_lowercase[x], 8-y

    @staticmethod
    def fr2coord(file, rank):
        return ord(file)-97, 8-rank


class Player:
    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.pieces = board.pieces[color]
