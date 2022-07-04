"""
This is the 'constants' module that holds all global variables that remain constant throughout the game loop.
"""

import os
import pygame as game

game.init()
game.font.init()
game.mixer.pre_init(44100, -16, 2, 512)

""" DISPLAY. """
GAME_WIDTH, GAME_HEIGHT = 900, 700
GAME_DISPLAY = game.display.set_mode((GAME_WIDTH, GAME_HEIGHT))


""" FRAMES COUNTER. """
GAME_CLOCK = game.time.Clock()
FPS = 15


""" RGB COLOURS. """
LIGHT_WHITE = (220, 220, 220)
GREY = (75, 75, 75)
LIGHT_GREY = (44, 47, 51)
DARK_GREY = (48, 48, 48)
GREEN = (16, 180, 110)
RED = (255, 65, 65)


""" AUDIO FILES. """
MOVE_SFX = game.mixer.Sound(os.path.join('Assets', 'SFX', 'move.wav'))
MOVE_SFX.set_volume(0.3)

CAPTURE_SFX = game.mixer.Sound(os.path.join('Assets', 'SFX', 'capture.wav'))
CAPTURE_SFX.set_volume(0.4)

KING_IN_CHECK_SFX = game.mixer.Sound(os.path.join('Assets', 'SFX', 'move_check.wav'))
KING_IN_CHECK_SFX.set_volume(0.55)

START_GAME_SFX = game.mixer.Sound(os.path.join('Assets', 'SFX', 'start_game.wav'))
START_GAME_SFX.set_volume(0.7)

LOW_TIME_SFX = game.mixer.Sound(os.path.join('Assets', 'SFX', 'low_time.wav'))
LOW_TIME_SFX.set_volume(0.5)

PERIOD_SFX = game.mixer.Sound(os.path.join('Assets', 'SFX', 'period.wav'))
PERIOD_SFX.set_volume(0.5)

GAME_OVER_SFX = game.mixer.Sound(os.path.join('Assets', 'SFX', 'game_end.wav'))
GAME_OVER_SFX.set_volume(1.0)

UI_NAVIGATION_SFX = game.mixer.Sound(os.path.join('Assets', 'SFX', 'UI_navigation.wav'))
UI_NAVIGATION_SFX.set_volume(0.3)

UI_CLICK_SFX = game.mixer.Sound(os.path.join('Assets', 'SFX', 'UI_click.wav'))
UI_CLICK_SFX.set_volume(0.5)


""" IMAGE FILES. """
BOARD_IMG = game.image.load(os.path.join('Assets', 'Board', 'game_board.png')).convert_alpha()
S_KOMA_IMG = game.image.load(os.path.join('Assets', 'Player Assets', 'Komadai', 'sente_komadai.png')).convert_alpha()
G_KOMA_IMG = game.image.load(os.path.join('Assets', 'Player Assets', 'Komadai', 'gote_komadai.png')).convert_alpha()

SENTE_IMGS = ['K1', 'G1', 'S1', 'N1', 'L1', 'R1', 'B1', 'P1']
SENTE = [game.image.load(os.path.join('Assets', 'Pieces [S]', f'{SENTE_IMG}.png')) for SENTE_IMG in SENTE_IMGS]


GOTE_IMGS = ['K2', 'G2', 'S2', 'N2', 'L2', 'R2', 'B2', 'P2']
GOTE = [game.image.load(os.path.join('Assets', 'Pieces [G]', f'{GOTE_IMG}.png')) for GOTE_IMG in GOTE_IMGS]


PROMOTED_SENTE_IMGS = ['PS1', 'PN1', 'PL1', 'PR1', 'PB1', 'PP1']
PROMOTED_SENTE = [game.image.load(os.path.join('Assets', 'Promoted Pieces [S]', f'{PROMOTED_SENTE}.png')) for PROMOTED_SENTE in PROMOTED_SENTE_IMGS]


PROMOTED_GOTE_IMGS = ['PS2', 'PN2', 'PL2', 'PR2', 'PB2', 'PP2']
PROMOTED_GOTE = [game.image.load(os.path.join('Assets', 'Promoted Pieces [G]', f'{PROMOTED_GOTE}.png')) for PROMOTED_GOTE in PROMOTED_GOTE_IMGS]


BACKGROUNDS = ['background_1', 'background_2']
TITLE_SCREENS = [game.image.load(os.path.join('Assets', 'Menu', 'Title Screens', f'{BACKGROUND}.png')) for BACKGROUND in BACKGROUNDS]


ICONS = ['sente', 'gote', 'upscaled_sente', 'upscaled_gote']
PLAYER_ICONS = [game.image.load(os.path.join('Assets', 'Player Assets', 'Icons', f'{ICON}.png')) for ICON in ICONS]


GAME_TITLES = ['title', 'game_over_title', 'piece_moves_manual', 'options_Title', 'credits_Title']
WINDOW_TITLES = [game.image.load(os.path.join('Assets', 'Menu', 'Title Screens', f'{TITLE}.png')) for TITLE in GAME_TITLES]


MANUAL_PAGES = ['manual_page_1_title', 'manual_page_2_title', 'manual_page_3_title', 'manual_page_4_title']
MANUAL_TITLES = [game.image.load(os.path.join('Assets', 'Menu', 'Manual Assets', 'Page Titles', f'{TITLE}.png')) for TITLE in MANUAL_PAGES]


BUTTONS = ['start_button', 'selected_start_button', 'promote_button', 'selected_promote_button', 'unpromote_button',
           'selected_unpromote_button', 'manual_button', 'selected_manual_button', 'options_button', 'selected_options_button', 
           'credits_button', 'selected_credits_button', 'exit_button', 'selected_exit_button', 'music_button', 'selected_music_button',
           'sfx_button', 'selected_sfx_button', 'return_button', 'selected_return_button', 'engine_button', 'selected_engine_button', 
           'player_button', 'selected_player_button', 'sente_button', 'selected_sente_button', 'gote_button', 'selected_gote_button']

MENU_BUTTONS = [game.image.load(os.path.join('Assets', 'Menu', 'Buttons', f'{BUTTON}.png')) for BUTTON in BUTTONS]


POINTER_IMGS = [
    'menu_pointer', 'next_pointer', 'prev_pointer', 'selected_next_pointer', 'selected_prev_pointer', 
    'next_card_pointer', 'prev_card_pointer', 'selected_next_card_pointer', 'selected_prev_card_pointer'
    ]
POINTERS = [game.image.load(os.path.join('Assets', 'Menu', 'Pointers', f'{POINTER}.png')) for POINTER in POINTER_IMGS]


GAME_INFO = ['info_card[1]', 'info_card[2]', 'info_card[3]', 'info_card[4]', 'info_card[5]']
GAME_INFO_SLIDES = [game.image.load(os.path.join('Assets', 'Menu', 'Manual Assets', 'Game Info', f'{SLIDE}.png')).convert_alpha() for SLIDE in GAME_INFO]


BOARD_INFO = ['board_info[1]', 'board_info[2]', 'board_info[3]', 'board_info[4]', 'board_info[5]', 'board_info[6]']
BOARD_INFO_SLIDES = [game.image.load(os.path.join('Assets', 'Menu', 'Manual Assets', 'Board Info', f'{SLIDE}.png')).convert_alpha() for SLIDE in BOARD_INFO]


CARDS = ['pawn', 'lance', 'knight', 'bishop', 'rook', 'silver_general', 'gold_general', 'king']
PIECE_INFO_CARDS = [game.image.load(os.path.join('Assets', 'Menu', 'Manual Assets', 'Base Piece Cards', f'{CARD}_card.png')).convert_alpha() for CARD in CARDS]


PROMOTED_CARDS = ['promoted_pawn', 'promoted_lance', 'promoted_knight', 'promoted_silver_general', 'promoted_bishop', 'promoted_rook']
PROMOTED_PIECE_INFO_CARDS = [game.image.load(os.path.join('Assets', 'Menu', 'Manual Assets', 'Promoted Piece Cards', f'{PROMOTED_CARD}_card.png')).convert_alpha() for PROMOTED_CARD in PROMOTED_CARDS]


""" DIMENSIONS. """
BOARD_SIZE = (170, 87, 550, 550)
S_KOMA_SIZE = (799, 86, 62, 428)
G_KOMA_SIZE = (39, 216, 62, 428)

BOARD_TILE_SIZE = BOARD_SIZE[2] // 9
KOMA_TILE_SIZE = S_KOMA_SIZE[3] / 7

BOARD_X, BOARD_Y = BOARD_SIZE[0], BOARD_SIZE[1]
S_KOMA_X, S_KOMA_Y = S_KOMA_SIZE[0], S_KOMA_SIZE[1]
G_KOMA_X, G_KOMA_Y = G_KOMA_SIZE[0], G_KOMA_SIZE[1]


""" BOARD BOUNDS. """
TOP, BOTTOM = 0, 8
LEFT, RIGHT = 0, 8


""" FONTS. """
TIMER_FONT = game.font.SysFont('BaronNeue', 25)
BYOYOMI_FONT = game.font.SysFont('BaronNeue', 20)
WINNER_FONT = game.font.SysFont('Lemon Milk', 25)
WIN_REASON_FONT = game.font.SysFont('Lemon Milk', 22)

GAME_FONT_1 = game.font.SysFont('Savior1', 80)
GAME_FONT_2 = game.font.SysFont('Savior1', 50)

