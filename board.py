""" This is the 'generate' module that generates the game's base object attributes as well as handle any logic
related to the board and piece. """

import pygame as game
from abc import ABC

from pygame import *
from constants import *

game.init()


class GenerateGameBoard(ABC):

    def __init__(self, ranks: int = 9, files: int = 9) -> None:
        self.ranks = ranks  # Rows
        self.files = files  # Columns
        self.board = [[0 for _ in range(ranks)] for _ in range(files)]  # 9x9 2D array that represents the board


    @staticmethod
    def board_notation(files: int, ranks: int) -> str:
        """ This function takes the mouse position and swaps it with its notation from a dictionary. """

        ranks_dict = {'1': 8, '2': 7, '3': 6, '4': 5, '5': 4, '6': 3, '7': 2, '8': 1, '9': 0}
        ranks_notation = {value: rank_key for rank_key, value in ranks_dict.items()}  # Reverses key:value pairs

        files_dict = {'一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, '七': 6, '八': 7, '九': 8}
        files_notation = {value: file_key for file_key, value in files_dict.items()}  # Reverses key:value pairs

        return ranks_notation[ranks] + files_notation[files]


    def display_pieces_on_board(self, moves) -> None:
        """ This function loops through the ranks and files, and draws the pieces in their assigned locations. """

        for x in range(self.ranks):
            for y in range(self.files):
                if self.board[x][y] != 0:  # Checks if there is a class object assigned in that location
                    self.board[x][y].display_piece_imgs(self.board)
        
        players = ["sente", "gote"]
        
        for player in players:
            # For every piece in the komadai stack
            for capture in self.captured_pieces.get(player):
                if len(self.captured_pieces.get(player).get(capture)) > 0:
                    
                    match player:
                        case 'sente':
                            piece, position = self.get_sente(88, capture, 61)

                        case 'gote':
                            piece, position = self.get_gote(220, capture, 61) 
                    
                    # Draws captured piece onto the komadai
                    self.captured_pieces.get(player).get(capture)[0].display_captured_pieces(piece, position, moves)
    
                        
    def get_sente(self, base: int, capture: str, offset: int) -> str and int:
        """ This function returns the pixel location of a certain captured piece. """
        
        match capture:
            case 'Pawn':
                piece = SENTE[7]
                base += (6*offset)
            
            case 'Lance':
                piece = SENTE[4]
                base += (5*offset)
            
            case 'Silver General':
                piece = SENTE[2]
                base += (3*offset)
            
            case 'Gold General':
                piece = SENTE[1]
                base += (2*offset)
            
            case 'Rook':
                piece = SENTE[5]
            
            case 'Knight':
                piece = SENTE[3]
                base += (4*offset)
            
            case 'Bishop':
                piece = SENTE[6]
                base += (1*offset)
        
        return piece, (int(S_KOMA_X) + 5, base)
                
                
    def get_gote(self, base: int, capture: str, offset: int) -> str and int:
        """ This function returns the pixel location of a certain captured piece. """
        
        match capture:
            case 'Pawn':
                piece = GOTE[7]
                
            case 'Lance':
                piece = GOTE[4]
                base += (1*offset)
            
            case 'Silver General':
                piece = GOTE[2]
                base += (3*offset)
            
            case 'Gold General':
                piece = GOTE[1]
                base += (4*offset)
            
            case 'Rook':
                piece = GOTE[5]
                base += (6*offset)
            
            case 'Knight':
                piece = GOTE[3]
                base += (2*offset)
            
            case 'Bishop':
                piece = GOTE[6]
                base += (5*offset)
                
        return piece, (int(G_KOMA_X) + 5, base)
                
        
""" ---------------------------------------------------------------------------------------------------------------------------------------- """


class Board(GenerateGameBoard):

    def __init__(self, ranks = 9, files = 9) -> None:
        super().__init__(ranks = ranks, files = files)
        self.first_rank_pieces = [
            Lance, Knight, SilverGeneral, GoldGeneral, King, GoldGeneral, SilverGeneral, Knight, Lance
        ]
        self.second_and_third_rank_pieces = [Bishop, Rook, Pawn]
        
        self.generate_board_status()


    def generate_board_status(self) -> None:
        """ This functions assigns each piece class to their locations within the board. """

        # Player 1s (sente) pieces
        for n in range(9):
            self.board[8][n] = self.first_rank_pieces[n](8, n, 'sente')

        self.board[7][1] = self.second_and_third_rank_pieces[0](7, 1, 'sente')
        self.board[7][7] = self.second_and_third_rank_pieces[1](7, 7, 'sente')

        for n in range(9):
            self.board[6][n] = self.second_and_third_rank_pieces[2](6, n, 'sente')

        # Sente's komadai stack
        self.sente_captures = {"Pawn":[],'Lance':[],'Knight':[],'Silver General':[],'Gold General':[],'Bishop':[],'Rook':[]}

        # Player 2s (gote) pieces
        for n in range(9):
            self.board[0][n] = self.first_rank_pieces[n](0, n, 'gote')

        self.board[1][7] = self.second_and_third_rank_pieces[0](1, 7, 'gote')
        self.board[1][1] = self.second_and_third_rank_pieces[1](1, 1, 'gote')

        for n in range(9):
            self.board[2][n] = self.second_and_third_rank_pieces[2](2, n, 'gote')

        # Gote's komadai stack
        self.gote_captures = {"Pawn":[],'Lance':[],'Knight':[],'Silver General':[],'Gold General':[],'Bishop':[],'Rook':[]}

        self.captured_pieces = {"sente": self.sente_captures, "gote": self.gote_captures}
        
        self.captured_select = [[0],[0],[0],[0],[0],[0],[0]]  # All pieces are set to 0 in terms of selection
        

class GeneratePieces:

    def __init__(self, rank: int, file: int, player: str) -> None:
        self.rank = rank
        self.file = file
        self.player = player
        self.move_set = []

        self.selected = False
        self.koma_selected = False
        self.promotion_boundry_reached = False
        self.token_promoted = False
        self.unpromotable_token = False
        self.find_king = False
        self.king_in_check = False
        self.checkmate = False
        
        self.token_type = '' 


    def piece_position(self) -> int:
        """ This function creates and returns the [x] and [y] positions within the board.  """

        piece_x = int(BOARD_X + (self.file * BOARD_TILE_SIZE)) + 5
        piece_y = int(BOARD_Y + (self.rank * BOARD_TILE_SIZE)) + 2

        return piece_x, piece_y


    def move_img_pos(self, position) -> None:
        """ This function changes the position of a piece to a selected rank and file. """

        self.rank = position[0]
        self.file = position[1]
        
    
    def display_piece_imgs(self, board) -> None:
        """ This function displays each player's piece. """

        match self.player:
            case 'sente':
                if self.token_promoted is True:
                    piece = PROMOTED_SENTE[self.promoted_pc_idx]  # Draws the promotion piece for sente
                else:
                    piece = SENTE[self.pc_idx]  # Draws the default piece for sente

            case 'gote':
                if self.token_promoted is True:
                    piece = PROMOTED_GOTE[self.promoted_pc_idx]  # Draws the promotion piece for gote
                else:
                    piece = GOTE[self.pc_idx]  # Draws the default piece for gote
        
        self.draw_selection_attributes(board)
        GAME_DISPLAY.blit(piece, (self.piece_position()))


    def display_captured_pieces(self, piece, position, moves) -> None:
        
        if self.koma_selected and self.player == 'gote':
            game.draw.rect(GAME_DISPLAY, GREY, (position[0] - 4, position[1] - 3, 60, 60), 0)
            self.draw_drop_moves(moves)
        
        elif self.koma_selected and self.player == 'sente':
            game.draw.rect(GAME_DISPLAY, GREY, (position[0] - 4, position[1] - 1, 60, 60), 0)
            self.draw_drop_moves(moves)
            
        GAME_DISPLAY.blit(piece, position)


    def _moves(self, board) -> list[int]:
        """ This function returns the legal move set for each piece. """
        
        self.move_set, _ = self.generate_move_list(board)
        return self.move_set

    
    def draw_drop_moves(self, moves):
        """ This function draws all the valid drop spaces for a captured piece. """
        
        for move in moves:

            legal_x_pos = int(BOARD_X + (move[1] * BOARD_TILE_SIZE)) + 1
            legal_y_pos = int(BOARD_Y + (move[0] * BOARD_TILE_SIZE)) + 1

            game.draw.rect(GAME_DISPLAY, GREY, (int(legal_x_pos), int(legal_y_pos), 60, 60), 0)   
             

    def draw_legal_moves(self, board) -> None:
        """ This function draws the legal moves of a selected piece. """

        draw_moves, capture_move = self.generate_move_list(board)
        draw_moves, capture_move = list(draw_moves), list(capture_move)
        
        for i in capture_move:
            capture_x = i[1]
            capture_y = i[0]

            # If a space contains an enemy space, they are indicated with a highlight
            if (board[capture_y][capture_x] != 0 and (capture_x, capture_y) in draw_moves
                    and board[capture_y][capture_x].player != self.player):
                
                capture_x_pos = int(BOARD_X + (capture_x * BOARD_TILE_SIZE)) + 1
                capture_y_pos = int(BOARD_Y + (capture_y * BOARD_TILE_SIZE)) + 1

                # Legal moves that are on an enemy piece are removed and replaced with a capture indicator
                draw_moves.remove((capture_x, capture_y))
                game.draw.rect(GAME_DISPLAY, GREEN, (int(capture_x_pos), int(capture_y_pos), 60, 60), 1)

        for j in draw_moves:

            legal_x_pos = int(BOARD_X + (j[0] * BOARD_TILE_SIZE)) + 1
            legal_y_pos = int(BOARD_Y + (j[1] * BOARD_TILE_SIZE)) + 1

            # Legal moves on empty spaces are displayed
            game.draw.rect(GAME_DISPLAY, GREY, (int(legal_x_pos), int(legal_y_pos), 60, 60), 0)        
        


    def draw_selection_attributes(self, board) -> None:
        """ This function highlights any selected piece and draws their legal moves. """
        
        match self.selected:
            case True:                
                game.draw.rect(
                    GAME_DISPLAY, GREY, (self.piece_position()[0] - 4, self.piece_position()[1] - 1, 60, 60), 0
                    )   # Draws a square on under a piece to indicate it has been selected
                self.draw_legal_moves(board)
        
        match self.king_in_check:
            case True:
                game.draw.rect(
                    GAME_DISPLAY, RED, (self.piece_position()[0] - 4, self.piece_position()[1] - 1, 60, 60), 1
                    )    # Draws a red highlight over the king piece that is in check
    
        
from pieces import King, GoldGeneral, SilverGeneral, Knight, Lance, Rook, Bishop, Pawn

