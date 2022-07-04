""" This is the 'pieces' module that handles all move generation for all piece classes. """

from constants import TOP, BOTTOM, LEFT, RIGHT
from board import GeneratePieces
from board import GenerateGameBoard

obj_board = GenerateGameBoard()

class GenerateMoves(GeneratePieces):

    def __init__(self, rank: int, file: int, player: str) -> None:
        super().__init__(rank = rank, file = file, player = player)
        self.board = obj_board.board
        self.move_boundaries()
                
                
    def move_boundaries(self) -> None:
        """ This function generates the boundries for each type of move. """
    
        self.top = (self.rank > TOP and
                    (self.board[self.rank - 1][self.file] == 0 or
                     self.board[self.rank - 1][self.file] != 0))

        self.right = (self.file < RIGHT and
                      (self.board[self.rank][self.file + 1] == 0 or
                       self.board[self.rank][self.file + 1] != 0))

        self.left = (self.file > LEFT and
                     (self.board[self.rank][self.file - 1] == 0 or
                      self.board[self.rank][self.file - 1] != 0))

        self.bottom = (self.rank < BOTTOM and
                       (self.board[self.rank + 1][self.file] == 0 or
                        self.board[self.rank + 1][self.file] != 0))

        self.top_right = ((self.rank > TOP and self.file < RIGHT) and
                          (self.board[self.rank - 1][self.file + 1] == 0 or
                           self.board[self.rank - 1][self.file + 1] != 0))

        self.top_left = ((self.rank > TOP and self.file > LEFT) and
                         (self.board[self.rank - 1][self.file - 1] == 0 or
                          self.board[self.rank - 1][self.file - 1] != 0))

        self.bottom_right = ((self.rank < BOTTOM and self.file < RIGHT) and
                             (self.board[self.rank + 1][self.file + 1] == 0 or
                              self.board[self.rank + 1][self.file + 1] != 0))

        self.bottom_left = ((self.rank < BOTTOM and self.file > LEFT) and
                            (self.board[self.rank + 1][self.file - 1] == 0 or
                             self.board[self.rank + 1][self.file - 1] != 0))
        
    
    def generate_base_moves(self, board, move_set: list, capture_set: list,
                            condition: bool, pos: tuple) -> None:
        """ This function generates and appends all the base moves for each piece. """

        match condition:
            case True:
                
                # If move is on an empty space, add to move set
                if board[pos[0]][pos[1]] == 0:
                    move_set.append((pos[1], pos[0]))

                # If move is on an enemy piece, add to capture and move set
                elif board[pos[0]][pos[1]].player != self.player:
                    move_set.append((pos[1], pos[0]))
                    capture_set.append((pos[0], pos[1]))
        

    def generate_promoted_base_moves(self, board: list[int], move_list: list[int], capture_list: list[int]) -> None:
        """ This function generates the extra moves for a promoted bishop piece. """
        
        self.move_boundaries()
        
        match self.player:
            
            case 'sente':
        
                legal_moves = [self.top, self.right, self.left, self.bottom, self.top_right, self.top_left]

                # New legal moves for promoted piece
                positions = [(self.rank - 1, self.file), (self.rank, self.file + 1), (self.rank, self.file - 1),
                            (self.rank + 1, self.file), (self.rank - 1, self.file + 1), (self.rank - 1, self.file - 1)]

                for moves in range(len(legal_moves)):  
                    # Function call to generate moves                   
                    self.generate_base_moves(board, move_list, capture_list, legal_moves[moves], positions[moves])
                                        
                    
            case 'gote':
                
                legal_moves = [self.bottom, self.left, self.right, self.top, self.bottom_left, self.bottom_right]

                # New legal moves for promoted piece
                positions = [(self.rank + 1, self.file), (self.rank, self.file - 1), (self.rank, self.file + 1),
                            (self.rank - 1, self.file), (self.rank + 1, self.file - 1), (self.rank + 1, self.file + 1)]
    
                for moves in range(len(legal_moves)):
                    # Function call to generate moves                   
                    self.generate_base_moves(board, move_list, capture_list, legal_moves[moves], positions[moves]) 


    def generate_promoted_rook_moves(self, board: list[int], move_list: list[int], capture_list: list[int]) -> None:
        """ This function generates the extra moves for a promoted rook piece. """
        
        self.move_boundaries()
        
        match self.player:

            case 'sente':
                legal_moves = [self.top_right, self.top_left, self.bottom_right, self.bottom_left]
                
                # Extra legal moves for promoted piece
                positions = [(self.rank - 1, self.file + 1), (self.rank - 1, self.file - 1), 
                             (self.rank + 1, self.file + 1), (self.rank + 1, self.file - 1)]
    
                for moves in range(len(legal_moves)):
                    # Function call to generate moves                     
                    self.generate_base_moves(board, move_list, capture_list, legal_moves[moves], positions[moves])
                    
                                
            case 'gote':
                legal_moves = [self.top_right, self.top_left, self.bottom_right, self.bottom_left]
                
                # Extra legal moves for promoted piece  
                positions = [(self.rank - 1, self.file + 1), (self.rank - 1, self.file - 1),
                            (self.rank + 1, self.file + 1), (self.rank + 1, self.file - 1)]
    
                for moves in range(len(legal_moves)):  
                    # Function call to generate moves                   
                    self.generate_base_moves(board, move_list, capture_list, legal_moves[moves], positions[moves])
        


    def generate_promoted_bishop_moves(self, board: list[int], move_list: list[int], capture_list: list[int]) -> None:
        
        self.move_boundaries()
        
        match self.player:

            case 'sente':
                legal_moves = [self.top, self.right, self.left, self.bottom,]

                # Extra legal moves for promoted piece
                positions = [(self.rank - 1, self.file), (self.rank, self.file + 1),
                             (self.rank, self.file - 1),(self.rank + 1, self.file)]
    
                for moves in range(len(legal_moves)):
                    # Function call to generate moves                     
                    self.generate_base_moves(board, move_list, capture_list, legal_moves[moves], positions[moves])
                    
                                
            case 'gote':
                legal_moves = [self.top, self.right, self.left, self.bottom,]

                # Extra legal moves for promoted piece
                positions = [(self.rank - 1, self.file), (self.rank, self.file + 1),
                             (self.rank, self.file - 1),(self.rank + 1, self.file)]
    
                for moves in range(len(legal_moves)):       
                    # Function call to generate moves              
                    self.generate_base_moves(board, move_list, capture_list, legal_moves[moves], positions[moves])


class King(GenerateMoves):
    pc_idx = 0

    def __init__(self, rank: int, file: int, player: str) -> None:
        super().__init__(rank = rank, file = file, player = player)
        self.unpromotable_token = True
        self.find_king = True
    
    def __repr__(self) -> str:
        return 'King'
        
        
    def generate_move_list(self, board: list[int]) -> list[int]:
        """ This function appends the legal and capture moves and returns it. """

        move_list = []
        capture_list = []

        match self.player:

            case 'sente':
                self.move_boundaries()
                
                legal_moves = [self.top, self.right, self.left, self.bottom,
                               self.top_right, self.top_left, self.bottom_right, self.bottom_left]
        
                # All legal moves for sente's King piece            
                positions = [(self.rank - 1, self.file), (self.rank, self.file + 1), (self.rank, self.file - 1),
                            (self.rank + 1, self.file), (self.rank - 1, self.file + 1), (self.rank - 1, self.file - 1),
                            (self.rank + 1, self.file + 1), (self.rank + 1, self.file - 1)]
    
                for moves in range(len(legal_moves)):
                    # Function call to generate base moves                     
                    self.generate_base_moves(board, move_list, capture_list, legal_moves[moves], positions[moves])
                    
                    if legal_moves[moves] != 0:
                        self.checkmate = False
                    
                                
            case 'gote':
                self.move_boundaries()
                
                legal_moves = [self.top, self.right, self.left, self.bottom,
                               self.top_right, self.top_left, self.bottom_right, self.bottom_left]
        
                # All legal moves for gote's King piece 
                positions = [(self.rank - 1, self.file), (self.rank, self.file + 1), (self.rank, self.file - 1),
                            (self.rank + 1, self.file), (self.rank - 1, self.file + 1), (self.rank - 1, self.file - 1),
                            (self.rank + 1, self.file + 1), (self.rank + 1, self.file - 1)]
    
                for moves in range(len(legal_moves)):
                    # Function call to generate base moves                     
                    self.generate_base_moves(board, move_list, capture_list, legal_moves[moves], positions[moves])
                
        return move_list, capture_list
        

class GoldGeneral(GenerateMoves):
    pc_idx = 1

    def __init__(self, rank: int, file: int, player: str) -> None:
        super().__init__(rank, file, player)
        self.unpromotable_token = True
        self.token_type = 'Gold General'

    def __repr__(self) -> str:
        return 'Gold General'


    def generate_move_list(self, board: list[int]) -> list[int]:
        """ This function appends the legal and capture moves and returns it. """
        
        move_list = []
        capture_list = []

        match self.player:

            case 'sente':
                self.move_boundaries()
                
                legal_moves = [self.top, self.right, self.left, self.bottom,
                            self.top_right, self.top_left]

                # All legal moves for sente's Gold General piece 
                positions = [(self.rank - 1, self.file), (self.rank, self.file + 1), (self.rank, self.file - 1),
                            (self.rank + 1, self.file), (self.rank - 1, self.file + 1), (self.rank - 1, self.file - 1)]
    
                for moves in range(len(legal_moves)):  
                    # Function call to generate base moves                   
                    self.generate_base_moves(board, move_list, capture_list, legal_moves[moves], positions[moves])

            case 'gote':
                self.move_boundaries()
                
                legal_moves = [self.bottom, self.left, self.right, self.top,
                            self.bottom_left, self.bottom_right]

                # All legal moves for gote's Gold General piece 
                positions = [(self.rank + 1, self.file), (self.rank, self.file - 1), (self.rank, self.file + 1),
                            (self.rank - 1, self.file), (self.rank + 1, self.file - 1), (self.rank + 1, self.file + 1)]
    
                for moves in range(len(legal_moves)): 
                    # Function call to generate base moves                    
                    self.generate_base_moves(board, move_list, capture_list, legal_moves[moves], positions[moves]) 

        return move_list, capture_list


class SilverGeneral(GenerateMoves):
    pc_idx = 2
    promoted_pc_idx = 0

    def __init__(self, rank: int, file: int, player: str) -> None:
        super().__init__(rank, file, player)
        self.token_type = 'Silver General'

    def __repr__(self) -> str:
        return 'Silver General'


    def generate_move_list(self, board: list[int]) -> list[int]:
        """ This function appends the legal and capture moves and returns it. """
        
        move_list = []
        capture_list = []

        match self.player:

            case 'sente':
                self.move_boundaries()
                
                # If piece is promoted, use new move set
                if self.token_promoted:
                    self.generate_promoted_base_moves(board, move_list, capture_list)
                
                else:
                    legal_moves = [self.top, self.top_right, self.top_left, self.bottom_right, self.bottom_left]

                    # All legal moves for sente's Silver General piece 
                    positions = [(self.rank - 1, self.file), (self.rank - 1, self.file + 1), (self.rank - 1, self.file - 1),
                                (self.rank + 1, self.file + 1), (self.rank + 1, self.file - 1)]
        
                    for moves in range(len(legal_moves)):              
                        # Function call to generate base moves       
                        self.generate_base_moves(board, move_list, capture_list, legal_moves[moves], positions[moves])
                                
                                
            case 'gote':
                self.move_boundaries()
                
                # If piece is promoted, use new move set
                if self.token_promoted:
                    self.generate_promoted_base_moves(board, move_list, capture_list)
                
                else:
                    legal_moves = [self.bottom, self.bottom_left, self.bottom_right, self.top_left, self.top_right]

                    # All legal moves for gote's Silver General piece 
                    positions = [(self.rank + 1, self.file), (self.rank + 1, self.file - 1), (self.rank + 1, self.file + 1),
                                (self.rank - 1, self.file - 1), (self.rank - 1, self.file + 1)]
        
                    for moves in range(len(legal_moves)):
                        # Function call to generate base moves                     
                        self.generate_base_moves(board, move_list, capture_list, legal_moves[moves], positions[moves])
                
        return move_list, capture_list


class Knight(GenerateMoves):
    pc_idx = 3
    promoted_pc_idx = 1

    def __init__(self, rank: int, file: int, player: str) -> None:
        super().__init__(rank, file, player)
        self.token_type = 'Knight'

    def __repr__(self) -> str:
        return 'Knight'

    def generate_move_list(self, board: list[int]) -> list[int]:
        """ This function appends the legal and capture moves and returns it. """
        
        move_list = []
        capture_list = []
        
        self.top_right = ((self.rank > TOP and self.file < RIGHT) and
                          (self.board[self.rank - 2][self.file + 1] == 0 or
                           self.board[self.rank - 2][self.file + 1] != 0))

        self.top_left = ((self.rank > TOP and self.file > LEFT) and
                         (self.board[self.rank - 2][self.file - 1] == 0 or
                          self.board[self.rank - 2][self.file - 1] != 0))
        
        self.bottom_right = ((self.rank < BOTTOM and self.file < RIGHT) and
                             (self.board[self.rank + 2][self.file + 1] == 0 or
                              self.board[self.rank + 2][self.file + 1] != 0))

        self.bottom_left = ((self.rank < BOTTOM and self.file > LEFT) and
                            (self.board[self.rank + 2][self.file - 1] == 0 or
                             self.board[self.rank + 2][self.file - 1] != 0))

        match self.player:

            case 'sente':
                
                # If piece is promoted, use new move set
                if self.token_promoted:
                    self.generate_promoted_base_moves(board, move_list, capture_list)
                
                else:    
                    legal_moves = [self.top_right, self.top_left]

                    # All legal moves for sente's Knight piece 
                    positions = [(self.rank - 2, self.file + 1), (self.rank - 2, self.file - 1)]
        
                    for moves in range(len(legal_moves)): 
                        # Function call to generate base moves                   
                        self.generate_base_moves(board, move_list, capture_list, legal_moves[moves], positions[moves])
                    
                                
            case 'gote':

                # If piece is promoted, use new move set
                if self.token_promoted:
                    self.generate_promoted_base_moves(board, move_list, capture_list)
                
                else:    
                    legal_moves = [self.bottom_right, self.bottom_left]

                    # All legal moves for gote's Knight piece 
                    positions = [(self.rank + 2, self.file + 1), (self.rank + 2, self.file - 1)]
        
                    for moves in range(len(legal_moves)): 
                        # Function call to generate base moves                         
                        self.generate_base_moves(board, move_list, capture_list, legal_moves[moves], positions[moves])
                
        return move_list, capture_list
        

class Lance(GenerateMoves):
    pc_idx = 4
    promoted_pc_idx = 2

    def __init__(self, rank: int, file: int, player: str) -> None:
        super().__init__(rank, file, player)
        self.token_type = 'Lance'
        self.token_promoted = False

    def __repr__(self) -> str:
        return 'Lance'
    
    def generate_move_list(self, board: list[int]) -> list[int]:
        """ This function appends the legal and capture moves and returns it. """
        
        move_list = []
        capture_list = []
                
        match self.player:

            case 'sente':
                
                # If piece is promoted, use new move set
                if self.token_promoted:
                   self.generate_promoted_base_moves(board, move_list, capture_list)
              
                else:
                    # All forward legal moves for sente's lance piece                                     
                    for incr_rank in range(self.rank, 0, -1):
                        
                        self.top = (self.rank > TOP and (self.board[incr_rank - 1][self.file] == 0 
                                                        or self.board[incr_rank - 1][self.file] != 0))  
                        
                        # Function call to generate base moves 
                        self.generate_base_moves(board, move_list, capture_list, self.top, (incr_rank - 1, self.file))
                        
                        # Break for loop if past board borders
                        if board[incr_rank - 1][self.file] != 0:
                            break
                                          
            case 'gote':
                
                # If piece is promoted, use new move set
                if self.token_promoted:
                    self.generate_promoted_base_moves(board, move_list, capture_list)
                   
                else:
                    # All forward legal moves for gote's lance piece
                    for incr_rank in range(self.rank, 8, +1):
                        
                        self.bottom = (self.rank < BOTTOM and (board[incr_rank + 1][self.file] == 0 
                                                            or board[incr_rank + 1][self.file] != 0)) 
                        
                        # Function call to generate base moves 
                        self.generate_base_moves(board, move_list, capture_list, self.bottom, (incr_rank + 1, self.file))
                        
                        # Break for loop if past board borders
                        if board[incr_rank + 1][self.file] != 0:
                            break
                
        return move_list, capture_list


class Rook(GenerateMoves):
    pc_idx = 5
    promoted_pc_idx = 3

    def __init__(self, rank: int, file: int, player: str) -> None:
        super().__init__(rank, file, player)
        self.token_type = 'Rook'

    def __repr__(self) -> str:
        return 'Rook'
    
    def generate_move_list(self, board: list[int]) -> list[int]:
        """ This function appends the legal and capture moves and returns it. """
        
        move_list = []
        capture_list = []
                
        match self.player:

            case 'sente':
                
                # If piece is promoted, add extra move set
                if self.token_promoted:
                    self.generate_promoted_rook_moves(board, move_list, capture_list)
                
                # All forward legal moves for sente's Rook piece                           
                for incr_top_rank in range(self.rank, 0, -1):
                    
                    self.top = (self.rank > TOP and (self.board[incr_top_rank - 1][self.file] == 0 
                                                     or self.board[incr_top_rank - 1][self.file] != 0))  
                    
                    # Function call to generate base moves 
                    self.generate_base_moves(board, move_list, capture_list, self.top, (incr_top_rank - 1, self.file))
                    
                    # Break for loop if past board borders
                    if board[incr_top_rank - 1][self.file] != 0:
                        break


                # All right legal moves for sente's Rook piece  
                for incr_right_file in range(self.file, 8, +1):
                    
                    self.right = (self.file < RIGHT and (self.board[self.rank][incr_right_file + 1] == 0 
                                                     or self.board[self.rank][incr_right_file + 1] != 0))  
                    
                    # Function call to generate base moves      
                    self.generate_base_moves(board, move_list, capture_list, self.right, (self.rank, incr_right_file + 1))
                    
                    # Break for loop if past board borders
                    if board[self.rank][incr_right_file + 1] != 0:
                        break


                # All left legal moves for sente's Rook piece 
                for incr_left_file in range(self.file, 0, -1):
                    
                    self.left = (self.file > LEFT and (self.board[self.rank][incr_left_file - 1] == 0 
                                                     or self.board[self.rank][incr_left_file - 1] != 0))  
                    
                    # Function call to generate base moves      
                    self.generate_base_moves(board, move_list, capture_list, self.left, (self.rank, incr_left_file - 1))
                    
                    # Break for loop if past board borders
                    if board[self.rank][incr_left_file - 1] != 0:
                        break         


                # All bottom legal moves for sente's Rook piece 
                for incr_bottom_rank in range(self.rank, 8, +1):
                    
                    self.bottom = (self.rank < BOTTOM and (self.board[incr_bottom_rank + 1][self.file] == 0 
                                                     or self.board[incr_bottom_rank + 1][self.file] != 0))  
                    
                    # Function call to generate base moves      
                    self.generate_base_moves(board, move_list, capture_list, self.bottom, (incr_bottom_rank + 1, self.file))
                    
                    # Break for loop if past board borders
                    if board[incr_bottom_rank + 1][self.file] != 0:
                        break

                                          
            case 'gote':
                
                # All forward legal moves for gote's Rook piece   
                for incr_top_rank in range(self.rank, 8, +1):
                    
                    self.bottom = (self.rank < BOTTOM and (self.board[incr_top_rank + 1][self.file] == 0 
                                                     or self.board[incr_top_rank + 1][self.file] != 0))  
                    
                    # Function call to generate base moves      
                    self.generate_base_moves(board, move_list, capture_list, self.bottom, (incr_top_rank + 1, self.file))
                    
                    # Break for loop if past board borders
                    if board[incr_top_rank + 1][self.file] != 0:
                        break

                # All left legal moves for gote's Rook piece 
                for incr_left_file in range(self.file, 8, +1):
                    
                    self.right = (self.file < RIGHT and (self.board[self.rank][incr_left_file + 1] == 0 
                                                     or self.board[self.rank][incr_left_file + 1] != 0))  
                    
                    # Function call to generate base moves      
                    self.generate_base_moves(board, move_list, capture_list, self.right, (self.rank, incr_left_file + 1))
                    
                    # Break for loop if past board borders
                    if board[self.rank][incr_left_file + 1] != 0:
                        break


                # All right legal moves for gote's Rook piece
                for incr_right_file in range(self.file, 0, -1):
                    
                    self.left = (self.file > LEFT and (self.board[self.rank][incr_right_file - 1] == 0 
                                                     or self.board[self.rank][incr_right_file - 1] != 0))  
                    
                    # Function call to generate base moves      
                    self.generate_base_moves(board, move_list, capture_list, self.left, (self.rank, incr_right_file - 1))
                    
                    # Break for loop if past board borders
                    if board[self.rank][incr_right_file - 1] != 0:
                        break    
                     
                
                # All bottom legal moves for gote's Rook piece
                for incr_bottom_rank in range(self.rank, 0, -1):
                    
                    self.top = (self.rank > TOP and (self.board[incr_bottom_rank - 1][self.file] == 0 
                                                     or self.board[incr_bottom_rank - 1][self.file] != 0))  
                    
                    # Function call to generate base moves      
                    self.generate_base_moves(board, move_list, capture_list, self.top, (incr_bottom_rank - 1, self.file))
                    
                    # Break for loop if past board borders
                    if board[incr_bottom_rank - 1][self.file] != 0:
                        break
                
                # If piece is promoted, add extra move set
                if self.token_promoted:
                    self.generate_promoted_rook_moves(board, move_list, capture_list)
                
        return move_list, capture_list


class Bishop(GenerateMoves):
    pc_idx = 6
    promoted_pc_idx = 4

    def __init__(self, rank: int, file: int, player: str) -> None:
        super().__init__(rank, file, player)
        self.token_type = 'Bishop'
    
    def __repr__(self) -> str:
        return 'Bishop'
    
    def generate_move_list(self, board: list[int]) -> list[int]:
        """ This function appends the legal and capture moves and returns it. """
        
        move_list = []
        capture_list = []
                
        match self.player:

            case 'sente':
                
                self.move_boundaries()
                incr_top_right_file, incr_top_left_file  = self.file, self.file  
                
                # All top right legal moves for sente's Bishop piece
                for incr_top_right_rank in range(self.rank, 0, -1):
                    
                    self.top_right = ((incr_top_right_rank > TOP and incr_top_right_file < RIGHT) and
                                    (self.board[incr_top_right_rank- 1][incr_top_right_file + 1] == 0 or
                                    self.board[incr_top_right_rank - 1][incr_top_right_file + 1] != 0))
                    
                    self.generate_base_moves(board, move_list, capture_list, self.top_right, 
                                             (incr_top_right_rank - 1, incr_top_right_file + 1))
                        
                    if self.top_right is False or board[incr_top_right_rank - 1][incr_top_right_file + 1] != 0:
                        break
                    
                    incr_top_right_file += 1

                
                # All top left legal moves for sente's Bishop piece
                for incr_top_left_rank in range(self.rank, 0, -1):
                    
                    self.top_left = ((incr_top_left_rank > TOP and incr_top_left_file > LEFT) and
                                    (self.board[incr_top_left_rank - 1][incr_top_left_file - 1] == 0 or
                                    self.board[incr_top_left_rank - 1][incr_top_left_file - 1] != 0))
                    
                    self.generate_base_moves(board, move_list, capture_list, self.top_left, 
                                             (incr_top_left_rank - 1, incr_top_left_file - 1))
                        
                    if self.top_left is False or board[incr_top_left_rank - 1][incr_top_left_file - 1] != 0:
                        break
                    
                    incr_top_left_file -= 1
                    
                
                incr_bottom_right_file, incr_bottom_left_file  = self.file, self.file      
                
                
                # All bottom right legal moves for sente's Bishop piece
                for incr_bottom_right_rank in range(self.rank, 8, +1):
                    
                    self.bottom_right = ((incr_bottom_right_rank < BOTTOM and incr_bottom_right_file < RIGHT) and
                                        (self.board[incr_bottom_right_rank + 1][incr_bottom_right_file + 1] == 0 or
                                        self.board[incr_bottom_right_rank + 1][incr_bottom_right_file + 1] != 0))
                    
                    self.generate_base_moves(board, move_list, capture_list, self.bottom_right, 
                                             (incr_bottom_right_rank + 1, incr_bottom_right_file + 1))
                        
                    if self.bottom_right is False or board[incr_bottom_right_rank + 1][incr_bottom_right_file + 1] != 0:
                        break
                    
                    incr_bottom_right_file += 1
                    
                
                # All bottom left legal moves for sente's Bishop piece
                for incr_bottom_left_rank in range(self.rank, 8, +1):
                    
                    self.bottom_left = ((incr_bottom_left_rank < BOTTOM and incr_bottom_left_file > LEFT) and
                                        (self.board[incr_bottom_left_rank + 1][incr_bottom_left_file - 1] == 0 or
                                        self.board[incr_bottom_left_rank + 1][incr_bottom_left_file - 1] != 0))
                    
                    self.generate_base_moves(board, move_list, capture_list, self.bottom_left, 
                                             (incr_bottom_left_rank + 1, incr_bottom_left_file - 1))
                    
                    # Break for loop if past board borders
                    if self.bottom_left is False or board[incr_bottom_left_rank + 1][incr_bottom_left_file - 1] != 0:
                        break
                    
                    incr_bottom_left_file -= 1

                # If piece is promoted, add extra move set
                if self.token_promoted:
                    self.generate_promoted_bishop_moves(board, move_list, capture_list)
                   
            case 'gote':
                
                incr_top_right_file, incr_top_left_file  = self.file, self.file   
                
                # All top right legal moves for gote's Bishop piece
                for incr_top_right_rank in range(self.rank, 8, +1):
                    
                    self.bottom_left = ((incr_top_right_rank < BOTTOM and incr_top_right_file > LEFT) and
                                        (self.board[incr_top_right_rank + 1][incr_top_right_file - 1] == 0 or
                                        self.board[incr_top_right_rank + 1][incr_top_right_file - 1] != 0))
                    
                    self.generate_base_moves(board, move_list, capture_list, self.bottom_left, 
                                             (incr_top_right_rank + 1, incr_top_right_file - 1))
                        
                    if self.bottom_left is False or board[incr_top_right_rank + 1][incr_top_right_file - 1] != 0:
                        break
                    
                    incr_top_right_file -= 1
                    

                # All top left legal moves for gote's Bishop piece
                for incr_top_left_rank in range(self.rank, 8, +1):
                    
                    self.bottom_right = ((incr_top_left_rank < BOTTOM and incr_top_left_file < RIGHT) and
                                        (self.board[incr_top_left_rank + 1][incr_top_left_file + 1] == 0 or
                                        self.board[incr_top_left_rank + 1][incr_top_left_file + 1] != 0))
                    
                    self.generate_base_moves(board, move_list, capture_list, self.bottom_right, 
                                             (incr_top_left_rank + 1, incr_top_left_file + 1))
                        
                    if self.bottom_right is False or board[incr_top_left_rank + 1][incr_top_left_file + 1] != 0:
                        break
                    
                    incr_top_left_file += 1
                
                
                incr_bottom_right_file, incr_bottom_left_file  = self.file, self.file  
                
                
                # All bottom right legal moves for gote's Bishop piece
                for incr_bottom_right_rank in range(self.rank, 0, -1):
                    
                    self.top_left = ((incr_bottom_right_rank > TOP and incr_bottom_right_file > LEFT) and
                                    (self.board[incr_bottom_right_rank - 1][incr_bottom_right_file - 1] == 0 or
                                    self.board[incr_bottom_right_rank - 1][incr_bottom_right_file - 1] != 0))
                    
                    # Function call to generate base moves
                    self.generate_base_moves(board, move_list, capture_list, self.top_left, 
                                             (incr_bottom_right_rank - 1, incr_bottom_right_file - 1))
                        
                    if self.top_left is False or board[incr_bottom_right_rank - 1][incr_bottom_right_file - 1] != 0:
                        break
                    
                    incr_bottom_right_file -= 1


                # All bottom left legal moves for gote's Bishop piece
                for incr_bottom_left_rank in range(self.rank, 0, -1):
                    
                    self.top_right = ((incr_bottom_left_rank > TOP and incr_bottom_left_file < RIGHT) and
                                    (self.board[incr_bottom_left_rank- 1][incr_bottom_left_file + 1] == 0 or
                                    self.board[incr_bottom_left_rank - 1][incr_bottom_left_file + 1] != 0))
                    
                    # Function call to generate base moves
                    self.generate_base_moves(board, move_list, capture_list, self.top_right, 
                                             (incr_bottom_left_rank - 1, incr_bottom_left_file + 1))
                        
                    # Break for loop if past board borders
                    if self.top_right is False or board[incr_bottom_left_rank - 1][incr_bottom_left_file + 1] != 0:
                        break
                    
                    incr_bottom_left_file += 1

                # If piece is promoted, add extra move set
                if self.token_promoted:
                    self.generate_promoted_bishop_moves(board, move_list, capture_list)
                                
        return move_list, capture_list



class Pawn(GenerateMoves):
    pc_idx = 7
    promoted_pc_idx = 5

    def __init__(self, rank: int, file: int, player: str) -> None:
        super().__init__(rank, file, player)
        self.token_type = 'Pawn'
        
    def __repr__(self) -> str:
        return 'Pawn'
    
    
    def generate_move_list(self, board: list[int]) -> list[int]:
        """ This function appends the legal and capture moves and returns it. """
        
        move_list = []
        capture_list = []

        match self.player:

            case 'sente':
                self.move_boundaries()
                
                # If piece is promoted, use new move set
                if self.token_promoted:
                    self.generate_promoted_base_moves(board, move_list, capture_list)
                                
                else:
                    # Function call to generate base moves
                    self.generate_base_moves(board, move_list, capture_list, self.top, (self.rank - 1, self.file))
                
                return move_list, capture_list

            case 'gote':
                self.move_boundaries()

                # If piece is promoted, use new move set
                if self.token_promoted:
                    self.generate_promoted_base_moves(board, move_list, capture_list)
                    
                else:    
                    # Function call to generate base moves
                    self.generate_base_moves(board, move_list, capture_list, self.bottom, (self.rank + 1, self.file))

                return move_list, capture_list
    
    