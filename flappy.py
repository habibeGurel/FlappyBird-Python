import random  # For generating random numbers
import sys  # We will use sys.exit to exit the program
import pygame
from pygame.locals import *  # Basic pygame imports

# Global Variables for the game
FPS = 32
scr_width = 289
scr_height = 511
display_screen_window = pygame.display.set_mode((scr_width, scr_height))
play_ground = scr_height * 0.8
game_image = {}
game_audio_sound = {}
player = 'images/bird.png'
bcg_image = 'images/background.png'
pipe_image = 'images/pipe.png'

def welcome_main_screen():
    """
    Shows welcome images on the screen
    """

    p_x = int(scr_width / 5)
    p_y = int((scr_height - game_image['player'].get_height()) / 2)
    msgx = int((scr_width - game_image['message'].get_width()) / 2)
    msgy = int(scr_height * 0.13)
    b_x = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
            else:
                display_screen_window.blit(game_image['background'], (0, 0))
                display_screen_window.blit(game_image['player'], (p_x, p_y))
                display_screen_window.blit(game_image['message'], (msgx, msgy))
                display_screen_window.blit(game_image['base'], (b_x, play_ground))
                pygame.display.update()
                time_clock.tick(FPS)


def main_gameplay():
    score = 0
    hak = 3
    p_x = int(scr_width / 5)
    p_y = int(scr_width / 2)
    b_x = 0


    n_pip1 = get_Random_Pipes()
    n_pip2 = get_Random_Pipes()
    bait = get_Random_Bait()

    up_pips = [
        {'x': scr_width , 'y': n_pip1[0]['y']},
        {'x': scr_width + (scr_width / 2), 'y': n_pip2[0]['y']}
    ]

    low_pips = [
        {'x': scr_width, 'y': n_pip1[1]['y']},
        {'x': scr_width + (scr_width / 2), 'y': n_pip2[1]['y']}
    ]

    bait_position = {'x':bait['x'], 'y': bait['y']}

    pip_Vx = -4
    bait_Vx = -2

    p_vx = -9 #baslangicta ne kadar zıplasın
    p_mvy = 10 #asağı süzülme hızı
    p_accuracy = 1 # y ekseninde haraket etme (aşağı doğru)

    p_flap_accuracy = -8 # y ekseninde haraket etme (zıplama)
    p_flap = False

    randomBaitCounter = 0
    randomBait = random.randint(0,5)
    yesilElmaYediMi = False
    greenAppleCounter = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if p_y > 0:
                    p_vx = p_flap_accuracy
                    p_flap = True
                    game_audio_sound['wing'].play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if p_y > 0:
                    p_vx = p_flap_accuracy
                    p_flap = True
                    game_audio_sound['wing'].play()

        cr_tst = is_Colliding(p_x, p_y, up_pips, low_pips)
        eat_tst = is_Eating(p_x, p_y, bait_position, randomBait)

        if(yesilElmaYediMi):
            greenAppleCounter += 1
            if greenAppleCounter >= 160:
                p_vx = -8
                p_mvy = 10
                yesilElmaYediMi = False
                print("yesil elma yedi")


        if hak == 0:
            return
        if cr_tst:
            return

        if eat_tst:
            bait_position['x'] = -10
            bait_position['y'] = -10

            if randomBait == 0: # yesil elma
                yesilElmaYediMi = True
                p_vx = -4
                p_mvy = 5

            elif randomBait == 1: #kırmızı elma
                if(hak == 5):
                    score += 1
                    game_audio_sound['point'].play()
                else:
                    hak += 1

            elif randomBait == 2: #mavi elma
                score *= 2
            elif randomBait == 3: #sise
                hak -= 1
            elif randomBait == 4: #kola
                hak -= 1

        p_middle_positions = p_x + game_image['player'].get_width() / 2
        for pipe in up_pips:
            pip_middle_positions = pipe['x'] + game_image['pipe'][0].get_width() / 2
            if pip_middle_positions <= p_middle_positions < pip_middle_positions + 4:
                score += 1
                game_audio_sound['point'].play()


        if p_vx < p_mvy and not p_flap:
            p_vx += p_accuracy

        if p_flap:
            p_flap = False
        p_height = game_image['player'].get_height()
        p_y = p_y + min(p_vx, play_ground - p_y - p_height)

        for pip_upper, pip_lower in zip(up_pips, low_pips):
            pip_upper['x'] += pip_Vx
            pip_lower['x'] += pip_Vx
            bait_position['x'] += bait_Vx


        if 0 < up_pips[0]['x'] < 5:
            new_pip = get_Random_Pipes()
            up_pips.append(new_pip[0])
            low_pips.append(new_pip[1])

        if bait_position['x'] < -10:
            new_bait = get_Random_Bait()
            bait_position.update(new_bait)
            randomBait = random.randint(0,5)
            randomBaitCounter = 0

        randomBaitCounter += 1

        if up_pips[0]['x'] < -game_image['pipe'][0].get_width():
            up_pips.pop(0)
            low_pips.pop(0)


        display_screen_window.blit(game_image['background'], (0, 0))

        for pip_upper, pip_lower in zip(up_pips, low_pips):
            display_screen_window.blit(game_image['pipe'][0], (pip_upper['x'], pip_upper['y']))
            display_screen_window.blit(game_image['pipe'][1], (pip_lower['x'], pip_lower['y']))

        if randomBait == 0:
            display_screen_window.blit(game_image['greenapple'], (bait_position['x'],bait_position['y']))

        elif randomBait == 1:
            display_screen_window.blit(game_image['redapple'], (bait_position['x'],bait_position['y']))

        elif randomBait == 2:
            display_screen_window.blit(game_image['blueapple'], (bait_position['x'],bait_position['y']))

        elif randomBait == 3:
            display_screen_window.blit(game_image['sise'], (bait_position['x'],bait_position['y']))
        elif randomBait == 4:
            display_screen_window.blit(game_image['coke'], (bait_position['x'],bait_position['y']))

        display_screen_window.blit(game_image['base'], (b_x, play_ground))
        display_screen_window.blit(game_image['player'], (p_x, p_y))

        for i in range(hak):
            if hak >= 3:
                display_screen_window.blit(game_image['heart'], ((5*8*i), (0)))
            elif hak == 2:
                display_screen_window.blit(game_image['heart'], ((5), (0)))
                display_screen_window.blit(game_image['heart'], ((40), (0)))
                display_screen_window.blit(game_image['emptyheart'], ((75), (0)))
            elif hak == 1:
                display_screen_window.blit(game_image['heart'], ((5), (0)))
                display_screen_window.blit(game_image['emptyheart'], ((40), (0)))
                display_screen_window.blit(game_image['emptyheart'], ((75), (0)))

        d = [int(x) for x in list(str(score))]
        w = 0
        for digit in d:
            w += game_image['numbers'][digit].get_width()
        Xoffset = (scr_width - w) / 2

        for digit in d:
            display_screen_window.blit(game_image['numbers'][digit], (Xoffset, scr_height * 0.12))
            Xoffset += game_image['numbers'][digit].get_width()

        pygame.display.update()
        time_clock.tick(FPS)



def is_Colliding(p_x, p_y, up_pipes, low_pipes):

    if p_y > play_ground - 25 or p_y < 0:
        game_audio_sound['hit'].play()
        return True

    for pipe in up_pipes:
        pip_h = game_image['pipe'][0].get_height()
        pip_w = game_image['pipe'][0].get_width()
        if (p_y < pip_h + pipe['y'] and abs(p_x - pipe['x']) < pip_w):
            game_audio_sound['hit'].play()
            return True

    for pipe in low_pipes:
        if (p_y + game_image['player'].get_height() > pipe['y']) and abs(p_x - pipe['x']) < \
                game_image['pipe'][0].get_width():
            game_audio_sound['hit'].play()
            return True

    return False

def is_Eating(p_x, p_y, bait_position, whichEat):

    for i in range(-10,10):
        for j in range (-10,10):
            if whichEat == 0:
                if((p_y + i) == bait_position['y']  and p_x == bait_position['x'] + j):
                    game_audio_sound['eat'].play()
                    return True
            elif whichEat == 1:
                if((p_y + i)== bait_position['y']  and p_x == bait_position['x'] + j):
                    game_audio_sound['eat'].play()
                    return True
            elif whichEat == 2:
                if((p_y + i) == bait_position['y'] and p_x == bait_position['x'] + j):
                    game_audio_sound['eat'].play()
                    return True
            elif whichEat == 3:
                if((p_y + i) == bait_position['y'] and p_x == bait_position['x'] + j):
                    game_audio_sound['eat'].play()
                    return True
            elif whichEat == 4:
                if((p_y + i) == bait_position['y'] and p_x == bait_position['x'] + j):
                    game_audio_sound['eat'].play()
                    return True
    return False

def get_Pipe(lastUpPipeX, lastUpPipeY, lastLowPipeX, lastLowPipeY):
    pipe = [
        {'x': lastUpPipeX + scr_width, 'y': lastUpPipeY + scr_height},
        {'x': lastLowPipeX + scr_width, 'y': lastLowPipeY + scr_height}
    ]
    return pipe

def get_Random_Pipes():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pip_h = game_image['pipe'][0].get_height()
    off_s = scr_height / 3
    y2 = off_s + random.randrange(0, int(scr_height - game_image['base'].get_height() - 1.2 * off_s))
    pipeX = scr_width + 10
    y1 = pip_h - y2 + off_s
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper Pipe
        {'x': pipeX, 'y': y2}, # lower Pipe
    ]

    return pipe

def get_Random_Bait():
    """
    Generate bait
    """
    baitX = scr_width + 10
    y = int(scr_width / 4)
    baitY = random.randint(y, (scr_height - game_image['base'].get_height()))
    bait = {'x': baitX, 'y': baitY}

    return bait

if __name__ == "__main__":
    """
    This will be the main point from where our game will start
    """
    pygame.init()
    time_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Game')
    game_image['numbers'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha(),
    )
    game_image['coke'] = pygame.image.load('images/coke.png').convert_alpha()
    game_image['sise'] = pygame.image.load('images/copsise.png').convert_alpha()
    game_image['heart'] = pygame.image.load('images/heart.png').convert_alpha()
    game_image['emptyheart'] = pygame.image.load('images/emptyheart.png').convert_alpha()
    game_image['redapple'] = pygame.image.load('images/redapple.png').convert_alpha()
    game_image['greenapple'] = pygame.image.load('images/greenapple.png').convert_alpha()
    game_image['blueapple'] = pygame.image.load('images/blueapple.png').convert_alpha()
    game_image['message'] = pygame.image.load('images/message.png').convert_alpha()
    game_image['base'] = pygame.image.load('images/base.png').convert_alpha()
    game_image['pipe'] = (pygame.transform.rotate(pygame.image.load(pipe_image).convert_alpha(), 180),
                          pygame.image.load(pipe_image).convert_alpha()
                          )

    # Game sounds
    game_audio_sound['die'] = pygame.mixer.Sound('sounds/die.wav')
    game_audio_sound['hit'] = pygame.mixer.Sound('sounds/hit.wav')
    game_audio_sound['point'] = pygame.mixer.Sound('sounds/point.wav')
    game_audio_sound['swoosh'] = pygame.mixer.Sound('sounds/swoosh.wav')
    game_audio_sound['wing'] = pygame.mixer.Sound('sounds/wing.wav')
    game_audio_sound['eat'] = pygame.mixer.Sound('sounds/eating.mp3')
    game_image['background'] = pygame.image.load(bcg_image).convert()
    game_image['player'] = pygame.image.load(player).convert_alpha()

    while True:
        welcome_main_screen()  # Shows welcome screen to the user until he presses a button
        main_gameplay()  # This is the main game function
