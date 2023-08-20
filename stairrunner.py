"""
A waste of time project inspired by some
mobile game I saw someone else playing.

I claim no ownership over this idea.
"""
import pygame
from random import choice
from time import sleep, time

# GAME_MODE changes the control scheme
# 0 = L and R to move left and right
# 1 = Move and Switch Dir
# In GM 1, L -> go in the direction facing
# and R -> Change direction facing and step
GAME_MODE = 0
SCORE_TICKDOWN = True

LEFT_KEYS = pygame.K_LEFT, pygame.K_LSHIFT
RIGHT_KEYS = pygame.K_RIGHT, pygame.K_RSHIFT

_RES = 300, 600
MID_X = _RES[0] * 0.5
PREVIEW_DISTANCE: int = 50
PLATFORM_DISPLACEMENT: tuple = 40, 40

BG_COLOR = pygame.Color(150, 190, 250)
DEATH_COLOR = pygame.Color(240, 96, 96)
PLATFORM_COLOR = pygame.Color(30, 30, 30)
PLATFORM_SIZE = 60, 10

PLAYER_COLOR = pygame.Color(250, 140, 90)
PLAYER_RECT_HEAD = pygame.Rect(MID_X - 20, 470, 40, 30)
PLAYER_RECT_BODY = pygame.Rect(MID_X - 10, 500, 20, 30)
SCORE_COLOR = pygame.Color(240, 240, 240)


def process_keypress(keys) -> str | None:
    global left_cooldown, right_cooldown
    left_pressed, right_pressed = False, False
    for key in LEFT_KEYS:
        if keys[key]:
            left_pressed = True
            break
    for key in RIGHT_KEYS:
        if keys[key]:
            right_pressed = True
            break
    
    if left_pressed and not left_cooldown:
        left_cooldown = True
        return 'L'
    elif not left_pressed:
        left_cooldown = False
    if right_pressed and not right_cooldown:
        right_cooldown = True
        return 'R'
    elif not right_pressed:
        right_cooldown = False
        
    return None


def paint_scene(alive):
    window.fill(BG_COLOR if alive else DEATH_COLOR)
    
    anim_dir = 1 if facing_dir == 'R' else -1
    plat_anim_disp = (PLATFORM_DISPLACEMENT[0] * plat_anim * anim_dir,
                      PLATFORM_DISPLACEMENT[1] * plat_anim * -1)
    
    plat_x = (_RES[0] - PLATFORM_SIZE[0]) * 0.5
    platform_loc = [plat_x + plat_anim_disp[0],
                    _RES[1] - 70 + plat_anim_disp[1]]
    for item in plat_gen[:PREVIEW_DISTANCE]:
        pygame.draw.rect(window, PLATFORM_COLOR, 
                         (platform_loc, PLATFORM_SIZE), border_radius=5)
        platform_loc[0] += PLATFORM_DISPLACEMENT[0] * (1 if 'R' == item else -1)
        platform_loc[1] -= PLATFORM_DISPLACEMENT[1]
        if platform_loc[1] < 0:
            break
    
    pygame.draw.rect(window, PLAYER_COLOR, PLAYER_RECT_HEAD, border_radius=7)
    pygame.draw.rect(window, PLAYER_COLOR, PLAYER_RECT_BODY, border_radius=7)
    
    # Draw nose for pointing dir
    nose_left = PLAYER_RECT_HEAD.centerx - (PLAYER_RECT_HEAD.width if anim_dir == -1 else 0)
    pygame.draw.rect(window, PLAYER_COLOR, (nose_left, 480, 40, 10), border_radius=5)
    
    score_text = font.render(str(score), True, SCORE_COLOR)
    score_box = score_text.get_rect(center=(_RES[0] * 0.5, 50))
    window.blit(score_text, score_box)
    pygame.display.update()


def main():
    global plat_gen, plat_anim, facing_dir, score, BG_COLOR
    
    max_score = 0
    start_time = time()
    
    running = True
    while running:
        frame_events = pygame.event.get()
        keys_pressed = pygame.key.get_pressed()
        
        action_taken = process_keypress(keys_pressed)
        if action_taken is not None:
            if GAME_MODE == 0:
                if plat_gen[0] == action_taken:
                    score += 1
                    plat_anim = 1
                    facing_dir = action_taken
                    plat_gen = plat_gen[1:]
                    plat_gen.append(choice(('L', 'R')))
                else:
                    running = False
            elif GAME_MODE == 1:
                if action_taken == 'L' and plat_gen[0] == facing_dir:
                    score += 1
                    plat_anim = 1
                    plat_gen = plat_gen[1:]
                    plat_gen.append(choice(('L', 'R')))
                elif action_taken == 'R' and plat_gen[0] != facing_dir:
                    score += 1
                    plat_anim = 1
                    facing_dir = 'L' if facing_dir == 'R' else 'R'
                    plat_gen = plat_gen[1:]
                    plat_gen.append(choice(('L', 'R')))
                else:
                    running = False
        
        paint_scene(running)
        if not running:
            sleep(0.5)
        plat_anim = max(0, plat_anim - (1/5))
        clock.tick(60)
        
        current_time = time()
        if current_time - start_time >= 1 and SCORE_TICKDOWN:
            score = max(0, score - 1)
            start_time = time()
        
        max_score = max(score, max_score)
        
        for event in frame_events:
            if event.type == pygame.QUIT:
                running = False
                score = max_score
                return False
    score = max_score
    return True


replaying = True
while replaying:
    score: int = 0
    plat_gen = [choice(('L', 'R')) for _ in range(PREVIEW_DISTANCE)]
    plat_anim = 0
    facing_dir = 'L' if GAME_MODE == 0 else plat_gen[0]
    left_cooldown, right_cooldown = False, False

    pygame.init()
    pygame.display.set_caption("Stair Runner Prototype")
    clock = pygame.time.Clock()
    window = pygame.display.set_mode(_RES)
    font = pygame.font.SysFont("Roboto", 96)
    
    replaying = main()
    print("Your best score was:", score)