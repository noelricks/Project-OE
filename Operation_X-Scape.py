#Imports
import pygame
import pygame, sys
from sys import exit
from pygame.locals import *
from random import randint
from button import Button

#Screen Dimensions
SCREEN = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Menu")
screen_width = 800
screen_height = 400
overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
screen = pygame.display.set_mode((800, 400))  # Screen Size
window = pygame.display.set_mode((screen_width, screen_height))

global m
m = 0

#Initial Game Properties
pygame.init()
pygame.display.set_caption('Operation_X-Scape')  # Screen name
clock = pygame.time.Clock()
test_font = pygame.font.Font('fonts/Pixeltype.ttf', 50)
small_test_font = pygame.font.Font('fonts/Pixeltype.ttf', 35)
game_active = False

#Audio
intro_music = pygame.mixer.Sound('audio/intro.wav')
options_music = pygame.mixer.Sound('audio/options.wav')
bg_music = pygame.mixer.Sound('audio/Audio3.wav')
end_music = pygame.mixer.Sound('audio/GameOver.wav')
jump_sound = pygame.mixer.Sound('audio/jump_11.wav')

#KEY FUNCTIONS
#Displays the score at top middle of screen and helps to display score at the end of the game
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000)
    score_surf = test_font.render(f'{current_time - reset_time}', False, ('White'))
    scored = current_time - reset_time
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return scored

#Steadily increases the difficulty
def display_score_1(x):
    current_time = int(pygame.time.get_ticks() / 1000)
    score = (current_time - reset_time)
    level = max(750, x - (score * 15))  # Ensure level is not too low
    return level

#Defines the movement of the obstacles
def obstacle_movement(obstacle_list):
    time = int(pygame.time.get_ticks() / 1000)
    increment = (time - reset_time)
    if obstacle_list:
        speed = 5 + (increment // 15)
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= speed

            if obstacle_rect.bottom == 345:
                screen.blit(alien_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

#Collisions
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                bg_music.stop()
                end_music.play()
                return False
    return True

#Animations
def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 345:
        player_surf = player_jump
    else:
        player_index += .1
        if player_index >= len(player_run): player_index = 0
        player_surf = player_run[int(player_index)]

# Load high score from a file
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except:
        return 0

# Save high score to a file
def save_high_score(high_score):
    try:
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))
    except Exception as e:
        print(f"Failed to save high score: {e}")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("fonts/Pixeltype.ttf", size)

# Screens
def play():
    global game_active, reset_time, reset_time_speed, obstacle_rect_list, player_rect2, player_rect, player_surf, player_gravity, alien_surf, fly_surf, end_music, bg_music, intro_music, options_music, jump_sound, player_index, player_run, player_jump, high_score, score, resets, ties

    game_active = True
    reset_time = 0
    reset_time_speed = 0
    score = 0
    resets = 0
    ties = 1
    reset_time = int(pygame.time.get_ticks() / 1000)
    reset_time_speed = int(pygame.time.get_ticks())
    intro_music.stop()
    options_music.stop()
    if m == 1:
        bg_music.set_volume(0)
        jump_sound.set_volume(0)
        end_music.set_volume(0)
    else:
        bg_music.set_volume(0.3)
        end_music.set_volume(0.3)
        jump_sound.set_volume(0.3)
        bg_music.play(loops = -1)
    #Images
    #Space Background
    space_surf = pygame.image.load('images/bg.png').convert()
    space_surf = pygame.transform.scale(space_surf, (800, 400)).convert()
    i = 0

    #Invisible Ground
    ground_surf = pygame.image.load('images/ground.png')
    ground_surf = pygame.transform.scale(ground_surf, (800, 100)).convert_alpha()

    # Alien
    alien_1 = pygame.image.load('images/alien_1.png').convert_alpha()
    alien_2 = pygame.image.load('images/alien_2.png').convert_alpha()
    alien_3 = pygame.image.load('images/alien_3.png').convert_alpha()
    alien_1 = pygame.transform.scale(alien_1, (80, 80)).convert_alpha()
    alien_2 = pygame.transform.scale(alien_2, (80, 80)).convert_alpha()
    alien_3 = pygame.transform.scale(alien_3, (80, 80)).convert_alpha()
    alien_frames = [alien_1, alien_2, alien_3]
    alien_frame_index = 0
    alien_surf = alien_frames[alien_frame_index]

    # Fly
    fly_1 = pygame.image.load('images/fly1.png').convert_alpha()
    fly_2 = pygame.image.load('images/fly2.png').convert_alpha()
    fly_1 = pygame.transform.scale(fly_1, (50, 50)).convert_alpha()
    fly_2 = pygame.transform.scale(fly_2, (50, 50)).convert_alpha()
    fly_frames = [fly_1, fly_2]
    fly_frame_index = 0
    fly_surf = fly_frames[fly_frame_index]

    #Obstacle list to hold both the Aliens and the Flies
    obstacle_rect_list = []
    obstacle_rect_list.clear()

    #Player with movements
    player_1 = pygame.image.load('images/Player_1.png').convert_alpha()
    player_2 = pygame.image.load('images/Player_2.png').convert_alpha()
    player_3 = pygame.image.load('images/Player_3.png').convert_alpha()
    player_4 = pygame.image.load('images/Player_4.png').convert_alpha()
    player_jump = pygame.image.load('images/Player_jump.png').convert_alpha()
    player_run = [player_1, player_2, player_3, player_4]
    player_index = 0
    player_surf = player_run[player_index]
    player_rect = player_surf.get_rect(midbottom=(150, 345))
    player_gravity = 0

    high_score = 0
    # Intro screen
    player_stand = pygame.image.load('images/player_stand.png').convert_alpha()
    player_stand = pygame.transform.scale(player_stand, (250, 250))
    player_stand_rect = player_stand.get_rect(center=(400, 200))

    game_name = test_font.render('Operation X-Scape', False, ('White'))
    game_name_rect = game_name.get_rect(center=(400, 60))

    game_message = test_font.render('Press "R" key to Run', False, 'White')
    game_message_rect = game_message.get_rect(center=(400, 350))

    # Timers / Animations
    base = int(1500)
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, base)

    alien_animation_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(alien_animation_timer, 60)

    fly_animation_timer = pygame.USEREVENT + 3
    pygame.time.set_timer(fly_animation_timer, 60)

    # Keeps the window open
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #Gravity
            if game_active:
                keys = pygame.key.get_pressed()
                elif keys[pygame.K_SPACE] and player_rect.bottom >= 325:
                    player_gravity = -15
                    jump_sound.play()
                else:
                    player_animation()
                    screen.blit(player_surf, player_rect)
            #Reset functionalities when the player loses
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    resets = 0
                    ties = 1
                    game_active = True
                    intro_music.stop()
                    bg_music.play(loops = -1)
                    reset_time = int(pygame.time.get_ticks() / 1000)
                    reset_time_speed = int(pygame.time.get_ticks())
                    obstacle_rect_list.clear()
                    player_rect.midbottom = (200, 345)
                    player_gravity = 0
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e and score > 0.5:
                    save_high_score(0)
                    high_score = 0
                    resets = 1
                    
                    # Display "High Score Resetting..."
                    reset_message = small_test_font.render(f'High Score Resetting...', True, 'White')
                    reset_message_rect = reset_message.get_rect(center=(200, 300))
                    screen.blit(reset_message, reset_message_rect)
                    pygame.display.update()  # Force the update to show the first message
                    
                    pygame.time.delay(1500)  # Wait for 1.5 seconds

            #Summons Obstacles
            if game_active:
                if event.type == obstacle_timer:
                    choice = randint(0,2)
                    if choice == 0:
                        obstacle_rect_list.append(alien_surf.get_rect(bottomright=(randint(900, 1000), 345)))
                    elif choice == 1:
                        obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1000), 260)))
                    else:
                        obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1000), 200)))
                    # Adjust timer dynamically based on the score
                    pygame.time.set_timer(obstacle_timer, display_score_1(base))
                if event.type == fly_animation_timer:
                    fly_frame_index += 1
                    if fly_frame_index >= len(fly_frames):
                        fly_frame_index = 0
                    fly_surf = fly_frames[fly_frame_index]
                if event.type == alien_animation_timer:
                    alien_frame_index += 1
                    if alien_frame_index >= len(alien_frames):
                        alien_frame_index = 0
                    alien_surf = alien_frames[alien_frame_index]

        #Animates the background image with looping effect
        if game_active == True:
            time = int(pygame.time.get_ticks())
            increment = (time - reset_time_speed)
            speed = 2 + (increment // 28000)
            screen.blit(space_surf, (i, 0))
            screen.blit(space_surf, (screen_width + i, 0))
            if (i <= -screen_width):
                screen.blit(space_surf, (screen_width + i, 0))
                i = 0
            i -= speed
            score = display_score()

            # Player Gravity
            player_gravity += 0.58
            player_rect.y += player_gravity
            if player_rect.bottom >= 345:
                player_rect.bottom = 345
            keys = pygame.key.get_pressed()
            
            player_animation()
            screen.blit(player_surf, player_rect)

            # Obstacle Movement
            obstacle_rect_list = obstacle_movement(obstacle_rect_list)

            # Create smaller collision rectangles
            smaller_player_rect = player_rect.inflate(-50, -50)
            smaller_obstacle_rects = [obstacle.inflate(-70, -70) for obstacle in obstacle_rect_list]

            # Collision
            game_active = collisions(smaller_player_rect, smaller_obstacle_rects)

        #Start Up Screen
        else:
            bg_music.stop()
            screen.fill('Red')
            screen.blit(player_stand, player_stand_rect)
            screen.blit(game_name, game_name_rect)
            screen.blit(game_message, game_message_rect)
            player_rect.midbottom = (150, 345)
            player_gravity = 0
            obstacle_rect_list.clear()
            if score == 0:
                screen.blit(game_message, game_message_rect)

            #Tells the player to hit the "R" key to restart   
            else:
                if high_score == 0:
                    save_high_score(high_score)
                if score > high_score and resets < 1:
                    ties -= 1
                    high_score = score
                    save_high_score(high_score)
                font_color = 'White'
                def display_text(text, x, y):
                    text_surface = test_font.render(text, True, font_color)
                    text_rect = text_surface.get_rect(center=(x, y))
                    screen.blit(text_surface, text_rect)
            #Tells the player their score
                def display_scores(text, x, y):
                    text_surface = test_font.render(text, True, font_color)
                    text_rect = text_surface.get_rect(center=(x, y))
                    screen.blit(text_surface, text_rect)
                def display_high_scores(text, x, y):
                    text_surface = test_font.render(text, True, font_color)
                    text_rect = text_surface.get_rect(center=(x, y))
                    screen.blit(text_surface, text_rect)
            #Popup Screen for when the player loses
                font = pygame.font.Font(None, 74)
                BG = pygame.image.load("images/game_over.jpg").convert()
                BG = pygame.transform.scale(BG, (800, 400)).convert()
                SCREEN.blit(BG, (0, 0))
                PLAY_MOUSE_POS = pygame.mouse.get_pos()

                PLAY_BACK = Button(image=None, pos=(700, 375), text_input="BACK", font=get_font(75), base_color="Red", hovering_color="White")

                PLAY_BACK.changeColor(PLAY_MOUSE_POS)
                PLAY_BACK.update(SCREEN)
            
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                            main_menu()
                if score == high_score and resets < 1 and ties == 0: #Ensures that scores are not labeled "High Scores" if the current score ties with the high score.
                    def display_text1(text, x, y):
                            text_surface = test_font.render(text, True, 'White')
                            text_rect = text_surface.get_rect(center=(x, y))
                            screen.blit(text_surface, text_rect)
                    display_text1('New High Score!', 545, 25)
                display_text('Press the "R" key to restart.', 225, 350)
                display_text('Press the "E" key to reset high score.', 295, 385)
                display_scores(f'Your score was: {score}', 250, 60)
                display_high_scores(f'High Score: {high_score}', 545, 65)

        pygame.display.update()
        clock.tick(80)  # fps control
#Opens the options page    
def options():
    global m
    audio_muted = False  # Flag to track mute state
    intro_music.stop()
    bg_music.stop()
    options_music.set_volume(0.3)
    options_music.play(loops=-1)
    
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        BG = pygame.image.load("images/options.jpg").convert()
        BG = pygame.transform.scale(BG, (800, 400)).convert()
        SCREEN.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(75).render("OPTIONS", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 75))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_TEXT = get_font(45).render("Press the 'm' key to mute the audio.", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 200))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_TEXT = get_font(45).render("Press the 'u' key to unmute the audio.", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 240))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # Display the mute/unmute message based on the current state
        if m == 1:
            MUTE_TEXT = get_font(35).render("Audio is muted", True, "Red")
            MUTE_RECT = MUTE_TEXT.get_rect(center=(400, 300))
            SCREEN.blit(MUTE_TEXT, MUTE_RECT)
        else:
            UNMUTE_TEXT = get_font(35).render("Audio is unmuted", True, "Green")
            UNMUTE_RECT = UNMUTE_TEXT.get_rect(center=(400, 300))
            SCREEN.blit(UNMUTE_TEXT, UNMUTE_RECT)

        OPTIONS_BACK = Button(image=None, pos=(400, 350), 
                              text_input="BACK", font=get_font(75), base_color="White", hovering_color="Blue")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_m and m == 0:
                audio_muted = True
                options_music.set_volume(0)  # Mute the music
                m += 1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_u and m == 1:
                audio_muted = False
                options_music.set_volume(0.3)  # Unmute the music
                m -= 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()
#Opens the main menu page
def main_menu():
    bg_music.stop()
    options_music.stop()
    if m == 1:
        intro_music.set_volume(0)
    else:
        intro_music.set_volume(.3)
        intro_music.play(loops = -1)
    while True:
        game_active = False
        BG = pygame.image.load("images/bg.jpg").convert()
        BG = pygame.transform.scale(BG, (800, 400)).convert()
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Operation X-Scape", True, "White")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 60))

        PLAY_BUTTON = Button(image=pygame.image.load("images/button.png"), pos=(400, 150), 
                            text_input="PLAY", font=get_font(75), base_color="#b68f40", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("images/button.png"), pos=(400, 235), 
                            text_input="OPTIONS", font=get_font(75), base_color="#b68f40", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("images/button.png"), pos=(400, 320), 
                            text_input="QUIT", font=get_font(75), base_color="#b68f40", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()

high_score = load_high_score()
