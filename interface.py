"""
This the 'interface' module in which the graphical user interface is created. This module controls all the menu
states with any images, all button logic and all music logic.
"""

import sys
from tkinter import N
import pygame as game

from time import sleep
from pygame import *
from constants import *


# This class handles all the methods surrounding music/audio
class MusicManager:
    
    def __init__(self) -> None:
        self.is_playing = game.mixer.music.get_busy()  # Checks if music is playing
        
        self.sounds = [MOVE_SFX, CAPTURE_SFX, START_GAME_SFX, LOW_TIME_SFX, PERIOD_SFX, 
                       GAME_OVER_SFX, UI_NAVIGATION_SFX, UI_CLICK_SFX]
        
        self.audio_levels = [0.3, 0.4, 0.7, 0.5, 0.5, 0.7, 0.4, 0.5]
    

    def main_menu_music(self, esc_key_pressed: bool) -> None:
        """ This function plays the menu music if the music button is 'on'. """
        
        # If audio is not playing or the user leaves the game loop, then music is played
        if self.is_playing is False or esc_key_pressed:
            game.mixer.music.load(os.path.join('Assets', 'SFX', 'Call of Silence.wav'))
            game.mixer.music.play(-1)  # '-1' means infinite loop
            game.mixer.music.set_volume(0.3)
    
        else:
            game.mixer.music.stop()
            self.is_playing = game.mixer.music.get_busy() 
         

    def game_loop_music(self) -> None:
        """ This function plays the game music if the music button is 'on'. """
        
        game.mixer.music.load(os.path.join('Assets', 'SFX', 'Nandemonaiya.wav'))
        game.mixer.music.play(-1)   # '-1' means infinite loop
        game.mixer.music.set_volume(0.1)
    
    
    def sfx_volume_levels(self, volume_on: bool) -> None:
        """ This function mutes all sfx audio if the sfx button is turned 'off' otherwise it sets them to their
            respective volume levels. """

        if volume_on:            
            for sound in self.sounds:  
                # Loops through each sfx file and sets the volume to 0
                sound.set_volume(0)
        else:
            for sound in range(len(self.sounds)):
                # Loops through the audio_levels list and appends each volume level to the corresponding sfx file
                self.sounds[sound].set_volume(self.audio_levels[sound])
        
                
# This class handles the logic of the menu screen buttons
class MenuButtonsUI:
    
    def __init__(self, image_1, image_2, dimensions, position, 
                 image_pos, image_center, pointer_size) -> None:
        
        self.button = game.Rect(position, (dimensions[0], dimensions[1]))  # Rect surface for button
        
        self.image = image_1
        self.selected_image = image_2
        self.reset_image = image_1
        self.image_pos = image_pos
        
        self.pointer_x = position[0] - 80
        self.pointer_y = self.button.center[1] - (image_center - 5)
        self.pointer_size = pointer_size
                
        self.play_sound = True
        self.clicked = False
        
    
    def check_input(self) -> None:
        """ This function checks for button input and executes the appropriate action. """
        
        mouse_position = game.mouse.get_pos()  # Returns the position of the mouse
        
        if self.button.collidepoint(mouse_position):
            # Replaces current image with a lighter coloured image to show its currently selected
            self.image = self.selected_image  
            
            if self.play_sound:  # Prevets sfx file from playing more than once
                UI_NAVIGATION_SFX.play()
                self.play_sound = False

            match self.pointer_size:  # Allocates the big pointer for the big buttons and vice versa
                case 'large':
                    GAME_DISPLAY.blit(POINTERS[0], (self.pointer_x, self.pointer_y))
                case 'small':
                    GAME_DISPLAY.blit(POINTERS[1], (self.pointer_x + 20, self.pointer_y + 4))
            
            if self.button.collidepoint(mouse_position) and game.mouse.get_pressed()[0]:
                self.clicked = True
            
            # Once button is clicked, its reset back to false to prevent mulitple clicks occuring at once
            elif self.clicked:  
                self.clicked = False
                self.play_sound = True
                
        else:  # Resets image to orginal image if the mouse leaves the area of the button
            self.image = self.reset_image
            self.play_sound = True
            self.clicked = False
            

    def draw_button(self) -> None:
        """ This function draws the button to the game display. """
        
        GAME_DISPLAY.blit(self.image, (self.image_pos[0], self.image_pos[1]))
        self.check_input()
        
        

# This class handles the logic of the buttons that are within the different menu states
class SceneButtonsUI:
    
    def __init__(self, image_1, image_2, dimensions, position) -> None:
        self.button = game.Rect(position, (dimensions[0], dimensions[1])) 
        
        self.image = image_1
        self.selected_image = image_2
        self.reset_image = image_1
        self.image_pos = position
            
        self.play_sound = True
        self.clicked = False
        

    def check_input(self) -> None:
        """ This function checks for button input and executes the appropriate action. """
        
        mouse_position = game.mouse.get_pos()  # Returns the position of the mouse

        if self.button.collidepoint(mouse_position):
            # Replaces current image with a lighter coloured image to show its currently selected
            self.image = self.selected_image  
            
            if self.play_sound:  # Prevents sfx file from playing more than once
                UI_NAVIGATION_SFX.play()
                self.play_sound = False
            
            if self.button.collidepoint(mouse_position) and game.mouse.get_pressed()[0]:
                self.clicked = True
                
            elif self.clicked:  
                UI_CLICK_SFX.play()
                self.clicked = False
                self.play_sound = True

                
        else:   # Resets image to orginal image if the mouse leaves the area of the button
            self.image = self.reset_image
            self.play_sound = True
            
            
    def draw_button(self) -> None:
        """ This function draws the button to the game display. """
        
        GAME_DISPLAY.blit(self.image, (self.image_pos[0], self.image_pos[1]))


class InfoCards:
    
    def __init__(self, deck: list[str], width: int, height: int, deck_type: str) -> None:
        self.cards = deck
        self.deck_type = deck_type

        if self.deck_type in {'game info', 'board info'}:
            self.prev_pointer_x = GAME_WIDTH / 2 - 415
            self.next_pointer_x = GAME_WIDTH / 2 + 360

        else:
            self.prev_pointer_x = GAME_WIDTH / 2 - 200
            self.next_pointer_x = GAME_WIDTH / 2 + 145

        self.prev_card_button = SceneButtonsUI(POINTERS[6], POINTERS[8], (55, 55), 
                                               (self.prev_pointer_x, GAME_HEIGHT / 2))

        self.next_card_button = SceneButtonsUI(POINTERS[5], POINTERS[7], (55, 55),
                                               (self.next_pointer_x, GAME_HEIGHT / 2))

        self.card_idx = 0
        self.width = width
        self.height = height
        self.draw_next_button = True
        self.draw_prev_button = False
        self.remove_prev_button = False
        self.remove_next_button = False


    def card_buttons(self, max_idx: int) -> None:
        """ This function handles button input with the info cards. """

        if self.card_idx >= 1 or self.card_idx >= max_idx:
            self.draw_prev_button = True
            self.draw_next_button = True
            self.remove_prev_button = False
            self.remove_next_button = False

        if self.card_idx >= max_idx:
            self.draw_next_button = False
            self.remove_next_button = True
            self.next_card_button.image = self.next_card_button.reset_image

        if self.card_idx < 1:
            self.draw_prev_button = False
            self.remove_prev_button = True
            self.prev_card_button.image = self.prev_card_button.reset_image
            
    
    def info_cards(self, event: event, max_idx: int) -> None:
        """ This function animates the cards that display the move set for each piece. """

        if event.type == game.QUIT:
            game.quit()
            sys.exit()

        if self.remove_next_button is False:
            self.next_card_button.check_input()

            if self.next_card_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                self.next_card_button.clicked = not self.next_card_button.clicked
                UI_CLICK_SFX.play()
                self.card_idx += 1

        if self.remove_prev_button is False:
            self.prev_card_button.check_input()

            if self.prev_card_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                self.prev_card_button.clicked = not self.prev_card_button.clicked
                UI_CLICK_SFX.play()
                self.card_idx -= 1
        
        self.card_buttons(max_idx)


    def render_cards(self) -> None:
        """ This function redners each piece cards to the manual window. """

        if self.card_idx in [2] and self.deck_type == 'base':
            GAME_DISPLAY.blit(self.cards[2], (GAME_WIDTH / 2 - 320, self.height))
        else:
            GAME_DISPLAY.blit(self.cards[self.card_idx], (self.width, self.height))
        
        if self.draw_prev_button:
            self.prev_card_button.draw_button()
            
        if self.draw_next_button:  
            self.next_card_button.draw_button()
            
            

# This class handles all the methods surrounding the game attributes before starting a match
class GameAttributes:
    
    def __init__(self) -> None:
        
        self.engine_button = MenuButtonsUI(MENU_BUTTONS[20], MENU_BUTTONS[21], (290, 82),
                                            (GAME_WIDTH / 2 - 150, GAME_HEIGHT / 2 - 75),
                                            (GAME_WIDTH / 2 - 155, GAME_HEIGHT / 2 - 130), 37, 'large')
        
        self.player_button = MenuButtonsUI(MENU_BUTTONS[22], MENU_BUTTONS[23], (290, 82),
                                            (GAME_WIDTH / 2 - 150, GAME_HEIGHT / 2 + 57),
                                            (GAME_WIDTH / 2 - 155, GAME_HEIGHT / 2), 37, 'large') 

        self.sente_button = MenuButtonsUI(MENU_BUTTONS[24], MENU_BUTTONS[25], (290, 82),
                                            (GAME_WIDTH / 2 - 150, GAME_HEIGHT / 2 - 75),
                                            (GAME_WIDTH / 2 - 155, GAME_HEIGHT / 2 - 130), 37, 'large')
        
        self.gote_button = MenuButtonsUI(MENU_BUTTONS[26], MENU_BUTTONS[27], (290, 82),
                                            (GAME_WIDTH / 2 - 150, GAME_HEIGHT / 2 + 57),
                                            (GAME_WIDTH / 2 - 155, GAME_HEIGHT / 2), 37, 'large') 

        self.prev_scene_button = SceneButtonsUI(POINTERS[2], POINTERS[4], (55, 55), 
                                           (GAME_WIDTH / 2 - 30, GAME_HEIGHT / 2 + 260))
   
       
    def choose_player(self, main_menu, main, mechanics) -> None:
        """ This function displays the window where the user selects what colour they want to play as. """
    
        running = True
        while running:
        
            GAME_DISPLAY.blit(TITLE_SCREENS[1], (0, 0))

            # Displays text that asks the user to choose their colour
            opponent = GAME_FONT_1.render('CHOOSE YOUR COLOUR!', 1, LIGHT_WHITE)
            GAME_DISPLAY.blit(opponent, (GAME_WIDTH / 2 - 260, GAME_HEIGHT / 2 - 190))
            
            # Function call to render buttons on window
            self.sente_button.draw_button()
            self.gote_button.draw_button()
            self.prev_scene_button.draw_button()
                                    
            for event in game.event.get():
                                                
                if event.type == QUIT:
                    game.quit()
                    sys.exit()
                
                # If the user selects the 'sente' button, they are playing as sente and are redirected to the main game loop
                self.sente_button.check_input()
                if self.sente_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                    mechanics.user = 'sente'
                    UI_CLICK_SFX.play()
                    main()
                
                # If the user selects the 'gote' button, they are playing as gote and are redirected to the main game loop
                self.gote_button.check_input()
                if self.gote_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                    mechanics.user = 'gote'
                    UI_CLICK_SFX.play()
                    main()

                # If the return button was clicked, the user will be redirected to the choose opponent
                self.prev_scene_button.check_input()
                if self.prev_scene_button.clicked is True and event.type == game.MOUSEBUTTONDOWN:
                    self.prev_scene_button.clicked = not self.prev_scene_button.clicked
                    running = False
                    UI_CLICK_SFX.play()
                    main_menu()
                                        
            game.display.update()
                        
            GAME_CLOCK.tick(FPS)
    
    
# This class handles all the methods surrounding the manual menu
class ManualMenuUI:
    
    def __init__(self) -> None:
        self.y_velocity = 30
        self.y_acceleration = 1
        
        self.prev_scene_button = SceneButtonsUI(POINTERS[2], POINTERS[4], (55, 55), 
                                                (GAME_WIDTH / 2 - 420, GAME_HEIGHT / 2 + 260))
        
        self.next_scene_button = SceneButtonsUI(POINTERS[1], POINTERS[3], (55, 55),
                                                (GAME_WIDTH / 2 + 365, GAME_HEIGHT / 2 + 260))
        
    
    def __render_manual_title(self, title: str, width: int, hieght: int) -> None:
        """ This function displays the manual menu title and animates its movement. """
        
        GAME_DISPLAY.blit(title, (width, hieght))
        self.y_velocity += self.y_acceleration  # Displace the y position of the image to move down

        # If the y position is past a certain range it reverses the change in pixel displacement, so the image moves up or down
        if self.y_velocity > 30:
            self.y_acceleration = -1

        elif self.y_velocity < 20:
            self.y_acceleration = 1


    def manual_page_one(self, main_menu) -> None:
        """ This function displays the manual page 1. """
        
        running = True
        
        # Contains all information on how to play game
        info_slides = InfoCards(GAME_INFO_SLIDES, GAME_WIDTH / 2 - 350, GAME_HEIGHT / 2 - 200, 'game info') 
        
        while running:
        
            GAME_DISPLAY.blit(TITLE_SCREENS[1], (0, 0))
            info_slides.render_cards()
            
            # Function call to render title and buttons
            self.__render_manual_title(MANUAL_TITLES[0], GAME_WIDTH / 2 - 270, self.y_velocity + 15)
            
            # Function call to render buttons on window
            self.prev_scene_button.draw_button()
            self.next_scene_button.draw_button()

            for event in game.event.get():
                
                # Function call to check button input 
                self.prev_scene_button.check_input()
                self.next_scene_button.check_input()
                
                info_slides.info_cards(event, 4)
                
                if event.type == QUIT:
                    game.quit()
                    sys.exit()

                # If the user selects the 'next' button, they are redirected to manual page 2
                if self.next_scene_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                    self.next_scene_button.clicked = not self.next_scene_button.clicked
                    running = False
                    UI_CLICK_SFX.play()
                    self.manual_page_two(main_menu)
                
                # If the user selects the 'previous' button, they are redirected to the main menu
                if self.prev_scene_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                    self.prev_scene_button.clicked = not self.prev_scene_button.clicked
                    running = False
                    UI_CLICK_SFX.play()
                    main_menu()
                
            game.display.update()
                        
            GAME_CLOCK.tick(FPS)
     

    def manual_page_two(self, main_menu) -> None:
        """ This function displays the manual window which shows the move set of all the base pieces. """
        
        running = True
        board_info = InfoCards(BOARD_INFO_SLIDES, GAME_WIDTH / 2 - 350, GAME_HEIGHT / 2 - 200, 'board info') 
        
        while running:
        
            GAME_DISPLAY.blit(TITLE_SCREENS[1], (0, 0))
            self.__render_manual_title(MANUAL_TITLES[1], GAME_WIDTH / 2 - 270, self.y_velocity)
            board_info.render_cards()
            
            # Function call to render buttons on window
            self.prev_scene_button.draw_button()
            self.next_scene_button.draw_button()
            
            for event in game.event.get():
                
                # Function call to check button input
                self.prev_scene_button.check_input()
                self.next_scene_button.check_input()
                
                board_info.info_cards(event, 5)
                
                if event.type == QUIT:
                    game.quit()
                    sys.exit()

                # If the user selects the 'next' button, they are redirected to manual page 3
                if self.next_scene_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                    self.next_scene_button.clicked = not self.next_scene_button.clicked
                    running = False
                    UI_CLICK_SFX.play()
                    self.render_page_three(main_menu)
                
                # If the user selects the 'previous' button, they are redirected to manual page 1
                if self.prev_scene_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                    self.prev_scene_button.clicked = not self.prev_scene_button.clicked
                    running = False
                    UI_CLICK_SFX.play()
                    self.manual_page_one(main_menu)
                
            game.display.update()
                        
            GAME_CLOCK.tick(FPS)
        
    
    def render_page_three(self, main_menu) -> None:
        """ This function displays the manual window which shows the move set of all the base pieces. """
        
        running = True
        piece_info = InfoCards(PIECE_INFO_CARDS, GAME_WIDTH / 2 - 315, GAME_HEIGHT / 2 - 230, 'base')
        
        while running:
        
            GAME_DISPLAY.blit(TITLE_SCREENS[1], (0, 0))
            self.__render_manual_title(MANUAL_TITLES[2], GAME_WIDTH / 2 - 270, self.y_velocity + 15)
            piece_info.render_cards()
            
            # Function call to render buttons on window
            self.prev_scene_button.draw_button()
            self.next_scene_button.draw_button()
            
            for event in game.event.get():
                
                 # Function call to check button input
                self.prev_scene_button.check_input()
                self.next_scene_button.check_input()
            
                piece_info.info_cards(event, 7)
                
                if event.type == QUIT:
                    game.quit()
                    sys.exit()

                # If the user selects the 'next' button, they are redirected to manual page 4
                if self.next_scene_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                    self.next_scene_button.clicked = not self.next_scene_button.clicked
                    running = False
                    UI_CLICK_SFX.play()
                    self.render_page_four(main_menu)
                
                # If the user selects the 'previous' button, they are redirected to manual page 2
                if self.prev_scene_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                    self.prev_scene_button.clicked = not self.prev_scene_button.clicked
                    running = False
                    UI_CLICK_SFX.play()
                    self.manual_page_two(main_menu)
            
            game.display.update()
                        
            GAME_CLOCK.tick(FPS)
    

    
    def render_page_four(self, main_menu) -> None:
        """ This function displays the manual window which shows the move set of all the base pieces. """
        
        running = True
        piece_info = InfoCards(PROMOTED_PIECE_INFO_CARDS, GAME_WIDTH / 2 - 315, GAME_HEIGHT / 2 - 230, 'Promoted')
        
        while running:
            
            GAME_DISPLAY.blit(TITLE_SCREENS[1], (0, 0))
            self.__render_manual_title(MANUAL_TITLES[3], GAME_WIDTH / 2 - 380, self.y_velocity)
            piece_info.render_cards()

            # Function call to display button on window
            self.prev_scene_button.draw_button()
                
            for event in game.event.get():
                
                # Function call to check button input
                self.prev_scene_button.check_input()
                
                piece_info.info_cards(event, 5)
                
                if event.type == QUIT:
                    game.quit()
                    sys.exit()

                # If the user selects the 'previous' button, they are redirected to manual page 3
                if self.prev_scene_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                    self.prev_scene_button.clicked = not self.prev_scene_button.clicked
                    running = False
                    UI_CLICK_SFX.play()
                    self.render_page_three(main_menu)
                
            game.display.update()
                        
            GAME_CLOCK.tick(FPS)
          
          
# This class handles all the methods surrounding the options menu
class OptionMenuUI:
    
    def __init__(self) -> None:    
        self.y_velocity = 30
        self.y_acceleration = 1
        
        self.music_button = SceneButtonsUI(MENU_BUTTONS[14], MENU_BUTTONS[15], (300, 300),
                                         (GAME_WIDTH / 2 + 40, GAME_HEIGHT / 2 - 150))
        
        self.sfx_button = SceneButtonsUI(MENU_BUTTONS[16], MENU_BUTTONS[17], (300, 300), 
                                         (GAME_WIDTH / 2 - 340, GAME_HEIGHT / 2 - 150)) 
        
        self.prev_scene_button = SceneButtonsUI(POINTERS[2], POINTERS[4], (55, 55), 
                                           (GAME_WIDTH / 2 - 420, GAME_HEIGHT / 2 + 260))
        
        self.music_status = 'ON'
        self.sfx_status = 'ON'
        
        self.music_button_clicks = 0
        self.sfx_button_clicks = 0
                

    def __render_animated_title(self) -> None:
        """ This function displays the options menu title and animates its movement. """
        
        GAME_DISPLAY.blit(WINDOW_TITLES[3], (GAME_WIDTH / 2 - 200, self.y_velocity + 15))
        self.y_velocity += self.y_acceleration  # Displace the y position of the image to move down

        # If the y position is past a certain range it reverses the change in pixel displacement, so the image moves up or down
        if self.y_velocity > 30:
            self.y_acceleration = -1

        elif self.y_velocity < 20:
            self.y_acceleration = 1
    
    
    def __render_options_txt(self) -> None:
        """ This function displays all the text and buttons onto the options window. """
                        
        # Displays the status of the music button -> ON or OFF
        music_txt = GAME_FONT_1.render('MUSIC: ', 1, LIGHT_WHITE)
        GAME_DISPLAY.blit(music_txt, (GAME_WIDTH / 2 + 70, GAME_HEIGHT / 2 + 150))  

        music_status_txt = GAME_FONT_1.render(str(self.music_status), 1, LIGHT_WHITE)
        GAME_DISPLAY.blit(music_status_txt, (GAME_WIDTH / 2 + 235, GAME_HEIGHT / 2 + 150))

        # Displays the status of the SFX button -> ON or OFF
        volume_txt = GAME_FONT_1.render('SFX: ', 1, LIGHT_WHITE)
        GAME_DISPLAY.blit(volume_txt, (GAME_WIDTH / 2 - 280, GAME_HEIGHT / 2 + 150))

        volume_status_txt = GAME_FONT_1.render(str(self.sfx_status), 1, LIGHT_WHITE)
        GAME_DISPLAY.blit(volume_status_txt, (GAME_WIDTH / 2 - 170, GAME_HEIGHT / 2 + 150))
    
    


    def music_button_controller(self, event: event) -> None:
        """ This function handles the actions executed when toggling the music button. """
        
        # Function call to check music button input
        self.music_button.check_input()
        
        if self.music_button.clicked and event.type == game.MOUSEBUTTONDOWN:
            self.music_button_clicks += 1
        
            # If music button clicked once, it call the function to mute all music files
            if self.music_button_clicks == 1 and MusicManager().is_playing:
                MusicManager().main_menu_music(esc_key_pressed = False)
                self.music_status = 'OFF'

            # If music button clicked twice, it call the function to unmute all music files
            elif self.music_button_clicks == 2 and MusicManager().is_playing is False:
                MusicManager().main_menu_music(esc_key_pressed = False)
                self.music_status = 'ON'
                self.music_button_clicks = 0
            
    
    def sfx_button_controller(self, event: event) -> None:
        """ This function handles the actions executed when toggling the SFX button. """

        # Function call to check SFX button input
        self.sfx_button.check_input()
    
        if self.sfx_button.clicked and event.type == game.MOUSEBUTTONDOWN:
            self.sfx_button_clicks += 1
            
            # If SFX button clicked once, it call the function to mute all SFX audio files
            if self.sfx_button_clicks == 1:
                UI_CLICK_SFX.play()
                sleep(0.05)
                MusicManager().sfx_volume_levels(volume_on = True)
                self.sfx_status = 'OFF'
            
            # If SFX button clicked twice, it call the function to unmute all SFX audio files
            elif self.sfx_button_clicks == 2:
                MusicManager().sfx_volume_levels(volume_on = False)
                self.sfx_status = 'ON'
                self.sfx_button_clicks = 0
    
    
    def options_menu_input_controller(self, main_menu) -> None:
        """ This function handles all button inputs within the options window. """
                
        for event in game.event.get():
            
            self.prev_scene_button.check_input()
            
            if event.type == QUIT:
                game.quit()
                sys.exit()
            
            # Function calls to check music button status and SFX button status
            self.music_button_controller(event) 
            self.sfx_button_controller(event) 
            
            # If return button is clicked, the user will be redirected to main menu
            if self.prev_scene_button.clicked and event.type == game.MOUSEBUTTONDOWN:
                self.prev_scene_button.clicked = not self.prev_scene_button.clicked
                UI_CLICK_SFX.play()
                main_menu()
        
        # Function call to render text onto the options window 
        self.__render_options_txt()
            
    
    def options_window(self, main_menu) -> None:
        """ This function displays the options window. """
        
        running = True
        
        while running:
            
            GAME_DISPLAY.blit(TITLE_SCREENS[1], (0, 0))

            # Function call that renders the title for the options window
            self.__render_animated_title()
            
            # Function call to render buttons on window
            self.music_button.draw_button()
            self.sfx_button.draw_button()
            self.prev_scene_button.draw_button()
            
            # Function call to check button input
            self.options_menu_input_controller(main_menu)
            
            game.display.update()
            
            GAME_CLOCK.tick(FPS)
            
    
# This class handles all the methods surrounding the credits menu
class CreditsMenuUI:
    
    def __init__(self) -> None:
        self.y_velocity = 30
        self.y_acceleration = 1
        
        self.prev_scene_button = SceneButtonsUI(POINTERS[2], POINTERS[4], (55, 55), 
                                                (GAME_WIDTH / 2 - 420, GAME_HEIGHT / 2 + 260))
    
    def _render_credits_title(self) -> None:
        """ This function displays the credits menu title and animates its movement. """
        
        # Animates the title to bounce up and down
        GAME_DISPLAY.blit(WINDOW_TITLES[4], (GAME_WIDTH / 2 - 200, self.y_velocity ))
        self.y_velocity += self.y_acceleration
        
        # If the y position is past a certain range it reverses the change in pixel displacement, so the image moves up or down
        if self.y_velocity  > 30:
            self.y_acceleration = -1
        
        elif self.y_velocity  < 20:
            self.y_acceleration = 1
    
    
    def _render_credits_txt(self) -> None:
        """ This function displays all the text and buttons onto the credits window. """
        
        credits_txt_1 = GAME_FONT_1.render('THANK YOU FOR PLAYING!', 1, LIGHT_WHITE)
        GAME_DISPLAY.blit(credits_txt_1, (GAME_WIDTH / 2 - 300, GAME_HEIGHT / 2 - 170))

        credits_txt_2 = GAME_FONT_1.render(
            'THIS PROJECT WAS CREATED BY', 1, LIGHT_WHITE
        )

        GAME_DISPLAY.blit(credits_txt_2, (GAME_WIDTH / 2 - 390, GAME_HEIGHT / 2 - 40))

        credits_txt_3 = GAME_FONT_1.render('HUZAIFA SYED', 1, LIGHT_WHITE)
        GAME_DISPLAY.blit(credits_txt_3, (GAME_WIDTH / 2 - 180, GAME_HEIGHT / 2 + 40))

        credits_txt_4 = GAME_FONT_2.render('GITHUB: aspherr', 1, LIGHT_WHITE)
        GAME_DISPLAY.blit(credits_txt_4, (GAME_WIDTH / 2 - 140, GAME_HEIGHT / 2 + 180))

        # Function call to render button on window
        self.prev_scene_button.draw_button()
        
        
    def credits_window(self, main_menu) -> None:
        """ This function displays the credits window. """
        
        running = True
        
        while running:
        
            GAME_DISPLAY.blit(TITLE_SCREENS[1], (0, 0))
            
            # Function call to render title and text
            self._render_credits_title()    
            self._render_credits_txt()

            for event in game.event.get():
                
                # Function call to check button input 
                self.prev_scene_button.check_input()

                if event.type == QUIT:
                    game.quit()
                    sys.exit()
                
                # If the return button was clicked, the user will be redirected to the main menu
                if self.prev_scene_button.clicked is True and event.type == game.MOUSEBUTTONDOWN:
                    self.prev_scene_button.clicked = not self.prev_scene_button.clicked
                    running = False
                    UI_CLICK_SFX.play()
                    main_menu()
                
            game.display.update()
                        
            GAME_CLOCK.tick(FPS)


# This class handles all the methods surrounding the promotion menu                
class PromotionWindow:
    
    def __init__(self) -> None:
        self.yes_button = MenuButtonsUI(MENU_BUTTONS[2], MENU_BUTTONS[3], (290, 95),
                                        (GAME_WIDTH / 2 - 145, GAME_HEIGHT / 2 - 50),
                                        (GAME_WIDTH / 2 - 150, GAME_HEIGHT / 2 - 100), 37, 'large')
        
        self.no_button = MenuButtonsUI(MENU_BUTTONS[4], MENU_BUTTONS[5], (290, 95),
                                        (GAME_WIDTH / 2 - 145, GAME_HEIGHT / 2 + 100),
                                        (GAME_WIDTH / 2 - 150, GAME_HEIGHT / 2 + 50), 37, 'large')
        
        self.promoted = False


    def __render_promotion_winow(self) -> None: 
        """ This function renders the text and buttons for the promotion window. """
        
        GAME_DISPLAY.blit(TITLE_SCREENS[1], (0, 0))
        
        promotion_txt = GAME_FONT_1.render('WOULD YOU LIKE TO PROMOTE?', 1, LIGHT_WHITE)

        GAME_DISPLAY.blit(promotion_txt, (GAME_WIDTH / 2 - 360, GAME_HEIGHT / 2 - 170))

        # Function call to display buttons on window
        self.yes_button.draw_button()
        self.no_button.draw_button()
    
    
    def promotion_window(self, mechanics) -> None:
        """ This function displays the window that asks the user if they want to promote a piece. """
        
        runnning = True
        
        while runnning:
            
            # Function call to render promotion window text and buttons
            self.__render_promotion_winow()
                        
            for event in game.event.get():
                
                # Function call to check button input 
                self.yes_button.check_input()
                self.no_button.check_input()
                
                if event.type == game.QUIT:
                    game.quit()
                    sys.exit()
                
                # If the 'yes' button is selected, the piece will change to its promoted state    
                if self.yes_button.clicked and game.MOUSEBUTTONDOWN: 
                    self.yes_button.clicked = not self.yes_button.clicked
                    self.promoted = True
                    mechanics.promoted = True  # Promotes piece
                    UI_CLICK_SFX.play()
                    runnning = False
    
                 # If the 'no' button is selected, the piece will remain unpromoted
                if self.no_button.clicked and game.MOUSEBUTTONDOWN: 
                    self.no_button.clicked = not self.no_button.clicked
                    self.promoted = False
                    UI_CLICK_SFX.play()
                    runnning = False

            game.display.update()                        
            GAME_CLOCK.tick(FPS)  
        
        
# This class handles all the methods surrounding the game over menu
class GameOverUI:
    
    def __init__(self) -> None:
        self.y_velocity = 180
        self.y_acceleration = 1
        
        self.return_button = MenuButtonsUI(MENU_BUTTONS[18], MENU_BUTTONS[19], (296, 65),
                                    (GAME_WIDTH / 2 - 153, GAME_HEIGHT / 2 + 217),
                                    (GAME_WIDTH / 2 - 156.5, GAME_HEIGHT / 2 + 200), 37, 'large')
    
    
    def __render_game_over_title(self) -> None:
        """ This function renders the game over title text. """
        
        # Animates the title to bounce up and down
        GAME_DISPLAY.blit(WINDOW_TITLES[1], (GAME_WIDTH / 2 - 370, self.y_velocity))
        self.y_velocity += self.y_acceleration
        
        # If the y position is past a certain range it reverses the change in pixel displacement, so the image moves up or down
        if self.y_velocity > 190:
            self.y_acceleration = -1
        
        elif self.y_velocity < 180:
            self.y_acceleration = 1
            
                
    def __render_text(self, winner: str, reason: str) -> None:
        """ This function displays all the text onto the game over screen. """
        
        winner_text = GAME_FONT_1.render(str(f'{winner} WAS VICTORIOUS'), 1, LIGHT_WHITE)
        GAME_DISPLAY.blit(winner_text, (GAME_WIDTH / 2 - 280, GAME_HEIGHT / 2 - 5))
        
        reason_for_win_text = GAME_FONT_1.render(str(f'REASON: {reason}'), 1, LIGHT_WHITE)
        GAME_DISPLAY.blit(reason_for_win_text, (GAME_WIDTH / 2 - 210, GAME_HEIGHT / 2 + 70))

        # Function call to render button on window
        self.return_button.draw_button()
    
    

    def game_over_screen(self, main_menu, winner, reason) -> None:
        """ This function displays the game over screen. """
        
        runnning = True
        
        while runnning:
            
            GAME_DISPLAY.blit(TITLE_SCREENS[1], (0, 0))
            
            # Function call to render promotion window text and buttons
            self.__render_game_over_title()
            self.__render_text(winner, reason)
                                    
            for event in game.event.get():
                
                # Function call to check button input
                self.return_button.check_input()
                
                if event.type == game.QUIT:
                    game.quit()
                    sys.exit()
                
                # If the user selects the 'previous' button, they are redirected to the main menu 
                if self.return_button.clicked and game.MOUSEBUTTONDOWN:  
                    self.return_button.clicked = not self.return_button.clicked
                    UI_CLICK_SFX.play()
                    main_menu()

            game.display.update()                        
            GAME_CLOCK.tick(FPS)  

