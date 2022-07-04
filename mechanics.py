""" This is the 'board' module in which most of the game logic and mechanics are handled. """


import itertools
from board import Board
from constants import *
from pieces import *
from pieces import Pawn

from interface import PromotionWindow
promotion_menu = PromotionWindow()


class GameMechanics(Board):

    def __init__(self, ranks = 9, files = 9) -> None:
        super().__init__(ranks = ranks, files = files)
        self.current_player = 'sente'
        self.user = ''
        self.engine = False
        self.start_game = True
        self.starting_move = True
        self.sente_move_made = False
        self.gote_move_made = False
        self.game_over = False
        
        self.sente_time = 300
        self.gote_time = 300
        self.start_timer = False

        self.sente_initial_byoyomi = True
        self.sente_byoyomi_period = False

        self.gote_initial_byoyomi = True
        self.gote_byoyomi_period = False
    
        self.clicks = 0

        self.winner = ''
        self.reason_for_win = ''
                    

    def piece_movement(self, start_position, end_position) -> bool:
        """ This function handles piece movement within the board array. """
        
        # Checks to see if a move has been made during the main byoyomi period
        if self.sente_initial_byoyomi is False:
            self.sente_move_made = True

        if self.gote_initial_byoyomi is False:
            self.gote_move_made = True

        current_piece_position = self.board[start_position[0]][start_position[1]]  # Current piece selected
        reset_current_piece_position = 0 
                          
        # Positional indexes in array are swapped
        current_piece_position.rank, current_piece_position.file = end_position[0], end_position[1]
        
        # Start game timer after gote makes there first move
        if ((current_piece_position.player == 'gote' and self.user == 'sente') or
            (current_piece_position.player == 'sente' and self.user == 'gote')):
            self.start_timer = True
            self.starting_move = False
        
        # If the current piece moves to a space with an enemy piece, it will be captured and pushed onto the komadai stack
        if (self.board[end_position[0]][end_position[1]] != 0 and 
            self.board[end_position[0]][end_position[1]].player != self.current_player and
            str(self.board[end_position[0]][end_position[1]]) != 'King'):
        
            new_capture = self.board[end_position[0]][end_position[1]]            
            new_capture.player = self.current_player
            self.captured_pieces.get(self.current_player).get(str(new_capture)).append(new_capture)
            
            CAPTURE_SFX.play()
                               
        self.check_for_piece_promotion(start_position, end_position) # Function call to check if a piece can be promoted

        self.board[end_position[0]][end_position[1]] = current_piece_position
        self.board[start_position[0]][start_position[1]] = reset_current_piece_position  # Resets that pieces old position to 0

        # Filter moves that can be made when a king is in check
        valid_moves = self.filter_valid_moves(start_position, end_position)
        return valid_moves is not False
    
    
    def contains(self, stack: list, value: int) -> bool:
        """ This function returns True if a piece was selected from the komadai. """
        
        return value in stack
    
    
    def valid_drop(self) -> bool:
        """ This function returns all valid spaces a piece can be dropped on. """
        
        # loops through each space on the board, and finds an empty spot
        return [(x, y) for x, y in itertools.product(range(self.ranks), range(self.files)) if self.board[x][y] == 0]

    
    def reset_koma_selection(self, rank, pieces) -> None:
        """ This function resets the selection of the piece selcted in the komadai. """
        
        # Loop through all of the top pieces from each stack until one of those pieces are found as selected
        for i in range(len(self.captured_select)-1):
            if i == rank:
                continue    
            
            # For every piece, reset there selection, then break out of loop
            if self.captured_select[i]:
                character = pieces[i]
                self.captured_pieces[self.current_player][character][0].koma_selected = False
                break
        
                        
    def reinstate_piece(self, index: int, rank: int, file: int) -> None:
        """ This function drops a selected piece from the komadai, back onto the board. """
        
        players = {"sente": "gote", "gote": "sente"}
        pieces = ('Pawn', 'Lance', 'Knight', 'Silver General', 'Gold General', 'Bishop', 'Rook')

        # Checks if a piece from the komadai is selected
        if self.contains(self.captured_select, True) and file != 7 and index == 10:
            select = self.captured_select.index(True)
            piece = pieces[select]
            
            # If the move is valid, the piece is popped out of the stack                         
            if (rank, file) in self.valid_drop():
                self.captured_pieces[self.current_player][piece][0].koma_selected = False                    
                piece_draw = self.captured_pieces[self.current_player][piece].pop()

                # Removed piece is placed back onto board
                self.board[rank][file] = piece_draw
                piece_draw.rank, piece_draw.file = rank, file
                MOVE_SFX.play()
                
                self.validate_checkmate()

                # Komadai selection is reset
                self.captured_select[select] = False
                self.change_player_turns() 
                return
                                    
        # Function call for selecting a certain piece from the komadai  
        self.komadai_selection(index, players, pieces, rank)


    def komadai_selection(self, index, players, pieces, rank) -> None:
        """ This function is used to select a piece from the komadai. """
            
        if (self.current_player == players["sente"] and index == 0):
            piece = pieces[rank]
                        
            if len(self.captured_pieces[self.current_player][piece]) > 0:
                if self.captured_select[rank]:
                    self.captured_pieces[self.current_player][piece][0].koma_selected = False

                else: 
                    self.captured_pieces[self.current_player][piece][0].koma_selected = True    
                    self.reset_koma_selection(rank, pieces) 
                    self.reset_piece_selection()

                self.captured_select[rank] = not self.captured_select[rank]


        elif self.current_player == players["gote"] and index == 1:
            piece = pieces[-(rank-6)]            

            if len(self.captured_pieces[self.current_player][piece]) > 0:
                if self.captured_select[-(rank-6)]:
                    self.captured_pieces[self.current_player][piece][0].koma_selected = False

                else:
                    self.captured_pieces[self.current_player][piece][0].koma_selected = True
                    self.reset_koma_selection(-(rank-6), pieces)  
                    self.reset_piece_selection()

                self.captured_select[-(rank-6)] = not self.captured_select[-(rank-6)]
        

    
    def piece_selection(self, rank, file, current_pos) -> None:
        """ This function checks if the user has selected a piece. """
        
        if self.board[rank][file] != 0 and self.board[rank][file].player == self.current_player: 
            self.reset_piece_selection()

            # If the piece the user selected is equal to their turn, then that piece is selected
            self.board[rank][file].selected = True
                
            # Mouse logic to allow for deselection of piece if it has been clicked twicce
            if self.board[current_pos[0]][current_pos[1]] != self.board[rank][file]:
                self.clicks = 1              
            else:
                self.clicks += 1
                            
            if self.clicks == 2:
                self.clicks = 0
                self.reset_piece_selection()  # Deselects piece if it has been clicked twice

        # If a piece has been selected, the tile the user chooses to move their piece to is checked to see if its a legal move
        elif current_pos != (rank, file):
            self.clicks += 1
            self.check_if_move_is_legal(rank, file, current_pos)
            self.reset_piece_selection()
                
                
    def reset_piece_selection(self) -> None:
        """ This function loops through the board array and resets any piece that had been selected. """
        
        for x, y in itertools.product(range(self.ranks), range(self.files)):
            if self.board[x][y] != 0:  # Loops through all pieces and deselects them
                self.board[x][y].selected = False
                
        self.captured_select = [False, False, False, False, False, False, False]
 
    
    def current_piece_position(self, rank: int, file: int):
        """ This function loops through board array and returns the current position of a piece. """
        
        current_piece_position = rank, file

        for x, y in itertools.product(range(self.ranks), range(self.files)):
            if self.board[x][y] != 0 and self.board[x][y].selected is True:
                # If a piece has been selected, its position is stored and returned as the current position
                current_piece_position = x, y

        return current_piece_position


    def check_if_move_is_legal(self, rank, file, current_pos) -> None:
        """ This function moves a piece if it's within the legal move set. """
        
        move_made = False
        
        self.generate_moves()
        moves = self.board[current_pos[0]][current_pos[1]].move_set
        piece = self.board[current_pos[0]][current_pos[1]]

        if (file, rank) in moves:
            # If the selected rank and file within the move list, the piece can be moved       
            move_made = self.move_piece_on_board(current_pos, rank, file)

        self.reset_piece_selection()
        
        if move_made is True:  # If a move has been made, turns are swapped and mouse clicks are reset
            MOVE_SFX.play()
            print(f'{piece}: {self.board_notation(current_pos[0], current_pos[1])} ➟ {self.board_notation(rank, file)}')
            self.change_player_turns()
            
            if self.king_in_check():
                MOVE_SFX.stop()
                CAPTURE_SFX.stop()
                KING_IN_CHECK_SFX.play()
                        
            self.clicks = 0
        
                                 
    def move_piece_on_board(self, current_pos, rank, file) -> bool:
        """ This function moves a selected piece """
    
        return bool(self.piece_movement(current_pos, (rank, file)))


    def change_player_turns(self) -> str:
        """ This function swaps the turn after a turn has been made. """

        match self.current_player:
            case 'sente':  # If sente's turn has been made, the current turn is switched to gote
                self.current_player = 'gote'
                return 'sente'

            case 'gote':  # If gote's turn has been made, the current turn is switched to sente
                self.current_player = 'sente'
                return 'gote'
        
        self.captured_select = [False, False, False, False, False, False, False]
    
    
    def check_for_piece_promotion(self, start_position, end_position) -> None:
        """ This function handles the promotion logic for each piece. """
        
        if self.board[start_position[0]][start_position[1]].unpromotable_token is True:
            self.board[start_position[0]][start_position[1]].promotion_boundry_reached = True

        elif (  # Checks to see if promotion conditions have been met
                self.board[start_position[0]][start_position[1]].token_promoted is False
                and self.board[start_position[0]][start_position[1]].promotion_boundry_reached is False
                and ((self.board[start_position[0]][start_position[1]].player == 'sente' and end_position[0] in [2, 1])
                     or (self.board[start_position[0]][start_position[1]].player == 'gote' and end_position[0] in [7, 6]))
            ):
            
            # Renders promotion window to ask player if they would like to promote their piece
            promotion_menu.promotion_window(self.board[start_position[0]][start_position[1]]) 
             
            if promotion_menu.promoted:  # If the user selects 'yes', that piece is promoted
                self.board[start_position[0]][start_position[1]].token_promoted = True
                self.board[start_position[0]][start_position[1]].promotion_status = True
                self.board[start_position[0]][start_position[1]].unpromotable_token = True

            self.board[start_position[0]][start_position[1]].promotion_boundry_reached = False
        
        # If the player's piece has reached the end of the board, they are automatically promoted
        elif ((end_position[0] in [0] and self.board[start_position[0]][start_position[1]].player == 'sente')
              or (end_position[0] in [8] and self.board[start_position[0]][start_position[1]].player == 'gote')):
            
                self.board[start_position[0]][start_position[1]].token_promoted = True
                self.board[start_position[0]][start_position[1]].promotion_status = True
                self.board[start_position[0]][start_position[1]].unpromotable_token = True
            
            
    def find_king(self):
        """ This function finds the current posititon of the King piece. """
        
        king_position = (4, 8) if self.current_player == 'sente' else (4, 0)
        
        for x, y in itertools.product(range(self.ranks), range(self.files)):
            # If the piece is a king belonging to the current player, its position is returned
            if self.board[x][y] != 0 and self.board[x][y].find_king is True and self.board[x][y].player == self.current_player:
                king_position = (y, x)
                
        return king_position

    
    def generate_moves(self):
        """ This function generates every move for every piece of a player. """
        
        moves = None
        for x, y in itertools.product(range(self.ranks), range(self.files)):
            if self.board[x][y] != 0 and self.board[x][y].selected:
                moves = self.board[x][y]._moves(self.board)  # Function call to retrieve all moves
                
        return moves
            
        
    def generate_opponents_moves(self):
        """ This function generates every move for every piece of the opposing player. """
        
        opp_moves = []
        for x, y in itertools.product(range(self.ranks), range(self.files)):
            if self.board[x][y] != 0 and self.board[x][y].player != self.current_player:
                opp_moves.extend(iter(self.board[x][y]._moves(self.board))) # Function call to retrieve all moves

        return opp_moves
    
            
    def king_in_check(self) -> bool:
        """ This function checks to see if king's position is in the move set of a piece, if so the king is in check. """

        king_position = self.find_king()
        
        # If king in any of the opponets moves, its in check
        if king_position in self.generate_opponents_moves():
            self.board[king_position[1]][king_position[0]].king_in_check = True
            return True

        # If the player turn swapped and the king isnt in any of the opponets moves, its not in check
        elif self.current_player != self.current_player or self.board[king_position[1]][king_position[0]].king_in_check:
            self.board[king_position[1]][king_position[0]].king_in_check = False
            return False

    
    def validate_checkmate(self) -> None:
        """ This function validates if the king piece is in a state of checkmate. """
        
        kings_moves = []
        king_position = self.find_king()
        self.board[king_position[1]][king_position[0]].checkmate = False

        # Find all current king moves
        for x, y in itertools.product(range(self.ranks), range(self.files)):
            if self.board[x][y] != 0 and self.board[x][y].find_king is True and self.board[x][y].player == self.current_player:
                kings_moves.extend(iter(self.board[x][y]._moves(self.board)))

        for moves in self.generate_opponents_moves():
            # If any of the opponents moves share the same moves as the king, then that move is removed from the king piece
            if moves in kings_moves:
                kings_moves.remove(moves)
        
        # If the king has no more moves, and is in check, then checkmate has occured
        if not kings_moves and self.king_in_check() is True:
            self.board[king_position[1]][king_position[0]].checkmate = True

        # Game over once checkmate occurs
        if self.board[king_position[1]][king_position[0]].checkmate:
            self.change_player_turns()
            self.winner = self.current_player.upper()
            self.reason_for_win = 'CHECKMATE'
            self.game_over = True
    

    def filter_valid_moves(self, start_position, end_position) -> bool:
        """ This function prevents moves that put the king in check or leave the king in check. """
        
        prev_check = self.king_in_check()
        self.generate_moves()
        
        # Current check status or future check status
        if self.king_in_check() or (prev_check is True and self.king_in_check()):
            
            current_piece_pos = self.board[end_position[0]][end_position[1]]  # Current piece selected
            reset_current_piece_position = 0
                        
            current_piece_pos.move_img_pos(start_position)  # Moves piece to the desired end position
            
            MOVE_SFX.stop()
             
            self.board[start_position[0]][start_position[1]] = current_piece_pos
            self.board[end_position[0]][end_position[1]] = reset_current_piece_position  # Resets that pieces old position to 0
            
            return False

        return True
    
            
class InitializeGame(GameMechanics):
    
    def __init__(self, ranks = 9, files = 9) -> None:
        super().__init__(ranks = ranks, files = files)

    def reset_board_status(self) -> None:
        """ This function resets all game objects/attributes when the game finishes. """
        
        self.current_player = 'sente'
        self.user = 'sente'
        self.start_game = True
        self.starting_move = True
        self.sente_move_made = False
        self.gote_move_made = False
        self.game_over = False
        
        self.engine_turn = False

        self.sente_time = 300
        self.gote_time = 300

        self.sente_initial_byoyomi = True
        self.sente_byoyomi_period = False

        self.gote_initial_byoyomi = True
        self.gote_byoyomi_period = False
    
        self.clicks = 0

        # Resets board state to orginal starting state
        self.reset_piece_selection()
        self.generate_board_status()

    
    def reset_winner(self) -> None:
        " This function resets winner objects to default value once game is finished. "

        self.winner = ''
        self.reason_for_win = ''


    def game_timer(self) -> None:
        """ This function creates the game timer and runs it once it's the corresponding player's turn. """

        match self.current_player:

            case 'sente':
                self.gote_time -= 0.075  # Decrements timer

                # Byoyomi timer that resets the timer to 10 seconds once a move has been made
                if self.sente_time <= 10 and self.sente_move_made is True:
                    self.sente_time = 10
                    self.sente_move_made = False

                 # Boolean checks to see if gote is low on their initial time before their byoyomi period
                if self.gote_initial_byoyomi is True:

                    if 10.915 > self.gote_time > 10.900:
                        LOW_TIME_SFX.play()

                    if self.gote_time <= 0:
                        self.gote_time = 11
                        self.gote_initial_byoyomi = False
                        self.sente_byoyomi_period = True
                        PERIOD_SFX.play()

                elif self.gote_time <= 0.5:

                    # If gote's time is less the 1, then they loose by time out
                    if 0.50 >= self.gote_time >= 0.49:
                        GAME_OVER_SFX.play()
                    else:
                        self.gote_time = 0
                        self.winner = 'GOTE'
                        self.reason_for_win = 'TIME OUT'
                        self.game_over = True

            case 'gote':

                self.sente_time -= 0.075  # Decrements timer

                # Byoyomi timer that resets the timer to 10 seconds once a move has been made
                if self.gote_time <= 10 and self.gote_move_made is True:
                    self.gote_time = 10
                    self.gote_move_made = False

                # Boolean checks to see if gote is low on their initial time before their byoyomi period
                if self.sente_initial_byoyomi is True:

                    if 10.915 >= self.sente_time >= 10.880:
                        LOW_TIME_SFX.play()

                    if self.sente_time <= 0:
                        self.sente_time = 11
                        PERIOD_SFX.play()
                        self.sente_initial_byoyomi = False
                        self.gote_byoyomi_period = True

                elif self.sente_time <= 0.50:
                    
                    # If gote's time is less the 1, then they loose by time out
                    if 0.50 >= self.sente_time >= 0.49:
                        GAME_OVER_SFX.play()
                    else:
                        self.sente_time = 0
                        self.winner = 'SENTE'
                        self.reason_for_win = 'TIME OUT'
                        self.game_over = True
                                        

    def play_move(self, rank: int, file: int) -> None:
        """ This function executes the main game mechanics on the current piece selected. """
        
        # Executes the main game logic once a piece has been selected
        self.piece_selection(rank, file, self.current_piece_position(rank, file))
        self.reinstate_piece(10, rank, file)
        
