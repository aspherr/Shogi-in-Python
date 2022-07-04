"""
Author: Huzaifa Syed
This is the 'main' module that is responsible for controlling the main game loop
"""

import os
import sys
import pygame as game
from pygame import *
from time import sleep

from constants import *
from interface import GameAttributes, MusicManager, MenuButtonsUI, ManualMenuUI, OptionMenuUI, CreditsMenuUI, GameOverUI
from mechanics import InitializeGame

os.environ['SDL_VIDEO_CENTERED'] = '1'  # centers game window
game.init()

# All the system classes that make up the game
game_mechanics = InitializeGame()
system = [MusicManager(), ManualMenuUI(), OptionMenuUI(), CreditsMenuUI(), GameOverUI(), GameAttributes()] 


class GameWindow:
        
    def game_window(self) -> None:
        """ This function creates the base window for the game. """

        game.display.set_caption('SHOGI ENGINE')
        GAME_DISPLAY.blit(TITLE_SCREENS[1], (0, 0))

        GAME_DISPLAY.blit(BOARD_IMG, (GAME_WIDTH / 2 - 387, GAME_HEIGHT / 2 - 365))  # Game Board Image
        GAME_DISPLAY.blit(S_KOMA_IMG, (GAME_WIDTH / 2 + 330, GAME_HEIGHT / 2 - 285)) # Sente's Komadai Image
        GAME_DISPLAY.blit(G_KOMA_IMG, (GAME_WIDTH / 2 - 430, GAME_HEIGHT / 2 - 285)) # Gote's Komadai Image
        
        game_mechanics.display_pieces_on_board(game_mechanics.valid_drop())
                    
        promotion_zone_indicators = [(354, 271), (536, 271), (354, 453), (536, 453)]

        for promotion_zone_indicator in promotion_zone_indicators:
            # Draws the circles that indicate each player's promotion zone on the board
            game.draw.circle(GAME_DISPLAY, DARK_GREY, promotion_zone_indicator, 7, 0)
    
    
    def display_game_timer(self, sente_time, gote_time):
        """ This function displays the gamer timer in the MM:SS format"""

        # Sente's formatted time
        sente_min, sente_sec = divmod(sente_time, 60)
        sente_formatted_time = f'{int(sente_min):02d}:{int(sente_sec):02d}' 
        
        sente_timer_txt = TIMER_FONT.render(str(sente_formatted_time), 1, LIGHT_WHITE)
        GAME_DISPLAY.blit(sente_timer_txt, (GAME_WIDTH / 2 + 350, GAME_HEIGHT / 2 + 270))

        # Gote's formatted time
        gote_min, gote_sec = divmod(gote_time, 60) 
        gote_formatted_time = f'{int(gote_min):02d}:{int(gote_sec):02d}'

        gote_timer_txt = TIMER_FONT.render(str(gote_formatted_time), 1, LIGHT_WHITE)
        GAME_DISPLAY.blit(gote_timer_txt, (GAME_WIDTH / 2 - 409, GAME_HEIGHT / 2 - 263))
                

    def update_game_window(self, sente_time: float, gote_time: float) -> None:
        """ This function updates the game window every frame. """
        
        self.game_window()
        
        # Handles the icon logic, if the player chose to be 'gote' 
        if game_mechanics.user == 'gote':
            GAME_DISPLAY.blit(PLAYER_ICONS[1], (GAME_WIDTH / 2 + 355, GAME_HEIGHT / 2 + 187))
            GAME_DISPLAY.blit(game.transform.rotate(PLAYER_ICONS[0], 180), (GAME_WIDTH / 2 - 404, GAME_HEIGHT / 2 - 215)) 
            
            # Enlarges current players icon
            if game_mechanics.current_player == 'gote': 
                GAME_DISPLAY.blit(PLAYER_ICONS[3], (GAME_WIDTH / 2 + 353, GAME_HEIGHT / 2 + 183))
                GAME_DISPLAY.blit(game.transform.rotate(PLAYER_ICONS[0], 180),  (GAME_WIDTH / 2 - 404, GAME_HEIGHT / 2 - 215))
            
            elif game_mechanics.current_player == 'sente':
                GAME_DISPLAY.blit(PLAYER_ICONS[1], (GAME_WIDTH / 2 + 355, GAME_HEIGHT / 2 + 187))
                GAME_DISPLAY.blit(game.transform.rotate(PLAYER_ICONS[2], 180), (GAME_WIDTH / 2 - 407, GAME_HEIGHT / 2 - 216))

         # Handles the icon logic, if the player chose to be 'sente' 
        elif game_mechanics.user == 'sente':
            GAME_DISPLAY.blit(PLAYER_ICONS[0], (GAME_WIDTH / 2 + 355, GAME_HEIGHT / 2 + 187))
            GAME_DISPLAY.blit(game.transform.rotate(PLAYER_ICONS[1], 180), (GAME_WIDTH / 2 - 404, GAME_HEIGHT / 2 - 215))
            
            # Enlarges current players icon
            if game_mechanics.current_player == 'gote':
                GAME_DISPLAY.blit(PLAYER_ICONS[0], (GAME_WIDTH / 2 + 355, GAME_HEIGHT / 2 + 187))
                GAME_DISPLAY.blit(game.transform.rotate(PLAYER_ICONS[3], 180), (GAME_WIDTH / 2 - 407, GAME_HEIGHT / 2 - 216))
            
            elif game_mechanics.current_player == 'sente':
                GAME_DISPLAY.blit(PLAYER_ICONS[2], (GAME_WIDTH / 2 + 353, GAME_HEIGHT / 2 + 183))
                GAME_DISPLAY.blit(game.transform.rotate(PLAYER_ICONS[1], 180), (GAME_WIDTH / 2 - 404, GAME_HEIGHT / 2 - 215))

        self.display_game_timer(sente_time, gote_time)

        # Displays the byoyomi period durations for either player once the main game time has run out
        byoyomi_txt = BYOYOMI_FONT.render('+10', 1, LIGHT_WHITE)

        if game_mechanics.sente_byoyomi_period is True:
            GAME_DISPLAY.blit(byoyomi_txt, (GAME_WIDTH / 2 + 390, GAME_HEIGHT / 2 + 307))

        if game_mechanics.gote_byoyomi_period is True:
            GAME_DISPLAY.blit(byoyomi_txt, (GAME_WIDTH / 2 - 415, GAME_HEIGHT / 2 - 298))



class GameLoop:
        
    def calculate_pos(self, mx: int, dimensions: int, my: int, type: str) -> int:
        """ This function mathematically determines the position of the mouse on the board or komodai as single digits. """
                
        if type == 'board':
            mx -= dimensions[0]
            my -= dimensions[1]

            # Returns a single digit value of a space within the board 
            return int(my // BOARD_TILE_SIZE), int(mx // BOARD_TILE_SIZE)  

        elif type == 'komadai':
            mx -= dimensions[0]
            my -= dimensions[1]

            # Returns a single digit value of a space within either komadai
            return int(my // KOMA_TILE_SIZE), 9   
            

    def mouse_pos(self, position: tuple) -> int:
        """ This function returns the mouse position of either when its on the board or komodai. """
        
        x, y = position[0], position[1]

        if (
                BOARD_SIZE[0] < x < BOARD_SIZE[0] + BOARD_SIZE[2] and
                BOARD_SIZE[1] < y < BOARD_SIZE[1] + BOARD_SIZE[3]
        ):
            # Calls the function to calculate the mouse position of the mouse was clicked within the board
            return self.calculate_pos(x, BOARD_SIZE, y, 'board')

        if (
                S_KOMA_SIZE[0] < x < S_KOMA_SIZE[0] + S_KOMA_SIZE[2] and
                S_KOMA_SIZE[1] < y < S_KOMA_SIZE[1] + S_KOMA_SIZE[3]
        ):
            # Calls the function to calculate the mouse position of the mouse was clicked within sente's komadai
            return self.calculate_pos(x, S_KOMA_SIZE, y, 'komadai')

        if (
                G_KOMA_SIZE[0] < x < G_KOMA_SIZE[0] + G_KOMA_SIZE[2] and
                G_KOMA_SIZE[1] < y < G_KOMA_SIZE[1] + G_KOMA_SIZE[3]
        ):
            # Calls the function to calculate the mouse position of the mouse was clicked within gote's komadai
            return self.calculate_pos(x, G_KOMA_SIZE, y, 'komadai')
    
    
    def input_controller(self) -> None:
        """ This function handles all input that occurs in the main game loop. """
        
        for event in game.event.get():
            
            if event.type == game.QUIT:
                game.quit()
                sys.exit()

            if event.type == game.MOUSEBUTTONDOWN:
                mouse_position = game.mouse.get_pos()  # Stores the mouse position
                mx, my = mouse_position[0], mouse_position[1]

                if (  # Checks if the mouse is within the boundaries of the board 
                    BOARD_SIZE[0] < mx < BOARD_SIZE[0] + BOARD_SIZE[2] and
                    BOARD_SIZE[1] < my < BOARD_SIZE[1] + BOARD_SIZE[3]
                ):
                    mouse_rank, mouse_file = self.mouse_pos(mouse_position)   
                    game_mechanics.play_move(mouse_rank, mouse_file)  # Executes game mechanics on any chosen tile in the board
                                        
                if (
                
                    S_KOMA_SIZE[0] < mx < S_KOMA_SIZE[0] + S_KOMA_SIZE[2] and
                    S_KOMA_SIZE[1] < my < S_KOMA_SIZE[1] + S_KOMA_SIZE[3]
                ):
                    mouse_rank, mouse_file = self.mouse_pos(mouse_position)    
                    game_mechanics.reinstate_piece(1, mouse_rank, mouse_file)  # calls function to select a captured piece
                    
                elif (
                    G_KOMA_SIZE[0] < mx < G_KOMA_SIZE[0] + G_KOMA_SIZE[2] and
                    G_KOMA_SIZE[1] < my < G_KOMA_SIZE[1] + G_KOMA_SIZE[3]
                ):
                    mouse_rank, mouse_file = self.mouse_pos(mouse_position)  
                    game_mechanics.reinstate_piece(0, mouse_rank, mouse_file)   # calls function to select a captured piece
       
                
            # If the 'esc' is pressed during the main game loop, the user returns the main menu and the board is reset
            if event.type == game.KEYDOWN and event.key == game.K_ESCAPE:
                if system[0].is_playing is False:
                    system[0].main_menu_music(esc_key_pressed = True)
               
                game_mechanics.reset_board_status()
                self.main_menu()  
        
        
    def main(self):
        """ This function runs the main game loop. """
             
        running = True

        # Plays game music track
        if MusicManager().is_playing is True:
            system[0].game_loop_music()
        
        # Plays the start game sfx
        if game_mechanics.start_game is True:
            sleep(0.25)
            START_GAME_SFX.play()
            game_mechanics.start_game = False

        while running:

            # Makes it wear AI makes the first turn if the user is gote and/or makes sente the starting player
            if game_mechanics.starting_move and (game_mechanics.engine is True or 
                                                 (game_mechanics.engine is False and game_mechanics.user == 'gote')):
                game_mechanics.starting_move = False
                game_mechanics.change_player_turns()
            
            # Plays the starting timer once the starting moves have been made
            if game_mechanics.starting_move is False and game_mechanics.start_timer:   
                game_mechanics.game_timer()

            # time variables for each player
            sente_time = game_mechanics.gote_time
            gote_time = game_mechanics.sente_time

            GameWindow().update_game_window(sente_time, gote_time)
            self.input_controller()

            # If king is in check, keep checking for checkmate
            if game_mechanics.king_in_check():
                game_mechanics.validate_checkmate()

            # If the game is finished, the board is reset
            if game_mechanics.game_over is True:
                game_mechanics.reset_board_status()
                system[4].game_over_screen(self.main_menu, game_mechanics.winner, game_mechanics.reason_for_win)
                game_mechanics.reset_winner()
            
            game.display.update()
            GAME_CLOCK.tick(FPS)

        
class MenuScreen(GameWindow, GameLoop):
    
    def __init__(self) -> None:
        # x and y positions that changes each frame 
        self.pos_x_velocity = 0
        self.pos_y_velocity = 0 
        
        # Variables that displaces an image by a certain amount of pixels per frame
        self.x_acceleration = 4
        self.y_acceleration = 2

        self.start_button = MenuButtonsUI(MENU_BUTTONS[0], MENU_BUTTONS[1], (290, 65),
                                                (GAME_WIDTH / 2 - 150, GAME_HEIGHT / 2 - 114),
                                                (GAME_WIDTH / 2 - 155, GAME_HEIGHT / 2 - 130), 37, 'large')

        self.manual_button = MenuButtonsUI(MENU_BUTTONS[6], MENU_BUTTONS[7], (290, 65),
                                        (GAME_WIDTH / 2 - 150, GAME_HEIGHT / 2 - 3),
                                        (GAME_WIDTH / 2 - 155, GAME_HEIGHT / 2 - 20), 37, 'large')

        self.options_button = MenuButtonsUI(MENU_BUTTONS[8], MENU_BUTTONS[9], (290, 65),
                                        (GAME_WIDTH / 2 - 150, GAME_HEIGHT / 2 + 107),
                                        (GAME_WIDTH / 2 - 155, GAME_HEIGHT / 2 + 90), 37, 'large')

        self.credits_button = MenuButtonsUI(MENU_BUTTONS[10], MENU_BUTTONS[11], (130, 40),
                                        (GAME_WIDTH / 2 + 290, GAME_HEIGHT / 2 + 272),
                                        (GAME_WIDTH / 2 + 265, GAME_HEIGHT / 2 + 262), 35, 'small')

        self.exit_button = MenuButtonsUI(MENU_BUTTONS[12], MENU_BUTTONS[13], (215, 65),
                                    (GAME_WIDTH / 2 - 112, GAME_HEIGHT / 2 + 217),
                                    (GAME_WIDTH / 2 - 156.5, GAME_HEIGHT / 2 + 200), 37, 'large')
        

    def render_menu(self) -> None:
        """ The function renders/animates the title and background. """

        # Animates the background into a scolling animation by decreasing the x position each frame
        relative_x_velocity = self.pos_x_velocity % TITLE_SCREENS[0].get_rect().width
        GAME_DISPLAY.blit(TITLE_SCREENS[0], (relative_x_velocity - TITLE_SCREENS[0].get_rect().width, 0))
        
        # If the x position is past the image's end boundry, the same image is blited to the end of the previous image
        if relative_x_velocity < 1767:
            GAME_DISPLAY.blit(TITLE_SCREENS[0], (relative_x_velocity, 0))
                        
        self.pos_x_velocity -= self.x_acceleration
        
        # Animates the title to bounce up and down
        GAME_DISPLAY.blit(WINDOW_TITLES[0], (GAME_WIDTH / 2 - 255, self.pos_y_velocity + 15))
        self.pos_y_velocity += self.y_acceleration
        
        # If the y position is past a certain range it reverses the change in pixel displacement, so the image moves up or down
        if self.pos_y_velocity > 9:
            self.y_acceleration = -2
        
        elif self.pos_y_velocity < -9:
            self.y_acceleration = 2
                           
            
    def main_menu_input_controller(self) -> None:
        """ This function handles all the button input in the main menu. """
        
        for event in game.event.get():
                                            
            if event.type == QUIT:
                game.quit()
                sys.exit()
            
            # If the 'start' button is selected, the main game loop is executed
            self.start_button.check_input()
            if self.start_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                UI_CLICK_SFX.play()                
                system[5].choose_player(self.main_menu, self.main, game_mechanics)
                                    
            # If the 'manual' button is selected, then instructions that tell the user how to play, is displayed
            self.manual_button.check_input()
            if self.manual_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                UI_CLICK_SFX.play()
                system[1].manual_page_one(self.main_menu)
                
            # If the 'options' button is selected, then the options menu is displayed
            self.options_button.check_input()
            if self.options_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                UI_CLICK_SFX.play()
                system[2].options_window(self.main_menu)
            
            # If the 'credits' button is selected, then the credits screen is displayed
            self.credits_button.check_input()
            if self.credits_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                UI_CLICK_SFX.play() 
                system[3].credits_window(self.main_menu)
        
            # If the 'exit' button is selected, then game loop breaks 
            self.exit_button.check_input()
            if self.exit_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                UI_CLICK_SFX.play()
                sleep(0.25)
                game.quit()
                sys.exit()

      
    def main_menu(self) -> None:
        """ This function displays the game's main menu. """
            
        game.display.set_caption('SHOGI')                
        running = True
                
        buttons = [self.start_button, self.manual_button, self.options_button, self.credits_button, self.exit_button]
    
        while running:
                
            # Function call to animate the main menu background and title
            self.render_menu()
                    
            # Function call to blit the button images to the main game window
            for button in buttons:
                button.draw_button()
                                                        
            # Function call to handle user input within the main menu
            self.main_menu_input_controller()
                        
            game.display.update()
            GAME_CLOCK.tick(FPS)
        
        
if __name__ == '__main__':
    system[0].main_menu_music(esc_key_pressed = False)
    app = MenuScreen()
    os.system('clear')
    app.main_menu()
    