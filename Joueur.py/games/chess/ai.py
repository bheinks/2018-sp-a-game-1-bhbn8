# This is where you build your AI for the Chess game.

from random import randint, choice
from string import ascii_lowercase

# local imports
from joueur.base_ai import BaseAI
from games.chess.board import Board, Player

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
# <<-- /Creer-Merge: imports -->>

PROMOTION_MAP = {
    "Knight": 'n',
    "Bishop": 'b',
    "Rook": 'r',
    "Queen": 'q'
}

class AI(BaseAI):
    """ The basic AI functions that are the same between games. """

    def get_name(self):
        """ This is the name you send to the server so your AI will control the player named this string.

        Returns
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "Chess Python Player" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self):
        """ This is called once the game starts and your AI knows its playerID and game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        
        self.board = Board(self.game.fen)
        self.local_player = Player(self.board, self.player.color)

        # <<-- /Creer-Merge: start -->>

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why you won or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        # <<-- /Creer-Merge: end -->>
    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """
        # <<-- Creer-Merge: runTurn -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.

        if len(self.game.moves) > 0:
            self.update_last_move()
            print(f"Opponent's last move: '{self.game.moves[-1].san}'")

        moves = []
        while not moves:
            local_piece, piece = self.select_piece()
            moves = local_piece.get_moves()

        move = choice(local_piece.get_moves())
        new_board = AI.get_new_state(self.board, local_piece, *move)

        print(f"Moving {self.player.color} {local_piece} at {local_piece.x}, {local_piece.y} to {x}, {y}")
        print(f"Or {ascii_lowercase[local_piece.x]}, {8-local_piece.y} to {ascii_lowercase[x]}, {8-y}")

        print(local_piece.get_moves())
        print("Remote board:")
        self.print_current_board()
        print("\nLocal board:")
        self.board.print()

        promotionType = ""

        if piece.type == "Pawn":
            if (self.player.color == "White" and  y == 0) or (
                    self.player.color == "Black" and y == 7):
                promotionType = choice(list(PROMOTION_MAP.keys()))

        piece.move(*Board.coord2fr(x, y), promotionType)
        local_piece.move(*Board.coord2fr(x, y), PROMOTION_MAP.get(promotionType, ""))

        return True
        # <<-- /Creer-Merge: runTurn -->>

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.

    @staticmethod
    def get_new_state(board, local_piece, x, y)
        new = Board(board.board2fen())

    def select_piece(self):
        local_piece, piece = None, None

        # if we're in check, we have to move the king
        if self.player.in_check:
            for p in self.local_player.pieces:
                if p.type == 'k':
                    local_piece = p
                    break

            for p in self.player.pieces:
                if p.type == "King":
                    piece = p
                    break
        else:
            local_piece = choice(local_player.pieces)
            
            for p in self.player.pieces:
                if Board.rf2coord(p.file, p.rank) == (local_piece.x, local_piece.y):
                    piece = p
                    break

        return local_piece, piece

    def update_last_move(self):
        move = self.game.moves[-1]
        local_piece = self.board.get_piece(*Board.fr2coord(move.from_file, move.from_rank))
        local_piece.move(move.to_file, move.to_rank)

    def print_current_board(self):
        """Prints the current board using pretty ASCII art
        Note: you can delete this function if you wish
        """

        # iterate through the range in reverse order
        for r in range(9, -2, -1):
            output = ""
            if r == 9 or r == 0:
                # then the top or bottom of the board
                output = "   +------------------------+"
            elif r == -1:
                # then show the ranks
                output = "     a  b  c  d  e  f  g  h"
            else:  # board
                output = " " + str(r) + " |"
                # fill in all the files with pieces at the current rank
                for file_offset in range(0, 8):
                    # start at a, with with file offset increasing the char
                    f = chr(ord("a") + file_offset)
                    current_piece = None
                    for piece in self.game.pieces:
                        if piece.file == f and piece.rank == r:
                            # then we found the piece at (file, rank)
                            current_piece = piece
                            break

                    code = "."  # default "no piece"
                    if current_piece:
                        # the code will be the first character of their type
                        # e.g. 'Q' for "Queen"
                        code = current_piece.type[0]

                        if current_piece.type == "Knight":
                            # 'K' is for "King", we use 'N' for "Knights"
                            code = "N"

                        if current_piece.owner.id == "1":
                            # the second player (black) is lower case.
                            # Otherwise it's uppercase already
                            code = code.lower()

                    output += " " + code + " "

                output += "|"
            print(output)

    # <<-- /Creer-Merge: functions -->>
