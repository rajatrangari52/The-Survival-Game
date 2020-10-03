import pygame
import random
from gtts import gTTS
import csv
import matplotlib.pyplot as plt
import numpy as np

# COLORS
white = (255, 255, 255)
maroon = (204, 0, 0)
fps=60
exit_game = False
game_width = 900
game_height = 600
game_name = 'Blood Bank Game'
bloog_grp = ('O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-')

bb_A1=pygame.image.load(r"F:\The Survival Game\blood_bag - A+.png")
bb_A2=pygame.image.load(r"F:\The Survival Game\blood_bag - A-.png")
bb_B1=pygame.image.load(r"F:\The Survival Game\blood_bag - B+.png")
bb_B2=pygame.image.load(r"F:\The Survival Game\blood_bag - B-.png")
bb_AB1=pygame.image.load(r"F:\The Survival Game\blood_bag - AB+.png")
bb_AB2=pygame.image.load(r"F:\The Survival Game\blood_bag - AB-.png")
bb_O1=pygame.image.load(r"F:\The Survival Game\blood_bag - O+.png")
bb_O2=pygame.image.load(r"F:\The Survival Game\blood_bag - O-.png")
blood_bag=(bb_A1,bb_A2,bb_B1,bb_B2,bb_AB1,bb_AB2,bb_O1,bb_O2)
bb_width=55
bb_height=92
p_width=200
p_height=93

pygame.init()
gameDisp = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption(game_name)
clock = pygame.time.Clock()

bgrn = pygame.image.load(r"F:\The Survival Game\bg22.jpg") #loaded bg image
game_bg = pygame.image.load(r"F:\The Survival Game\game_bg.png")
score_bg1 = pygame.image.load(r'F:\The Survival Game\score_bg1.png')
button_press = pygame.mixer.Sound(r'F:\The Survival Game\Play_button.wav')
# Funtion to display text on the screen at a particular co-ordinates
def text_screen(text, color, font_size, x, y):
    font = pygame.font.SysFont('Chiller', font_size, False, False)
    disp_text = font.render(text, True, color)
    gameDisp.blit(disp_text, (x, y))
    pass

def player_move(x, y):
    player = pygame.image.load(r"F:\The Survival Game\ambul.png")
    gameDisp.blit(player, [x, y])

def welcome():
    intro = True
    while intro:
        gameDisp.blit(game_bg, (0, 0))
        text_screen("THE  SURVIVAL  GAME!!", white, 85, 110, 20)
        text_screen("Press SPACE BAR", maroon, 55, 560, 440)
        text_screen("to continue", maroon, 50, 620, 500)
        text_screen("DEVELOPED BY: Deeksha Nemade",maroon,18,10,540)
        text_screen("Akash Kanase",maroon,18,110,560)
        text_screen("Rajat Rangari", maroon, 18,110, 580)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    pygame.mixer.Sound.play(button_press)
                    gameloop()
            elif event.type==pygame.QUIT:
                intro = False
                pygame.quit()
                quit()

def highscore(score,bg):
    high_sc = 0
    count = 0
    # score=(sc_O1,sc_O2,sc_A1,sc_A2,sc_B1,sc_B2,sc_AB1,sc_AB2)
    if bg == bloog_grp[0]:
        pygame.mixer.music.load(r'F:\The Survival Game\audio_O1.mp3')
        count = score[2]+score[3]+score[4]+ score[5] + score[6] + score[7]
        if count == 0:
            high_sc = score[0] + score[1]
    elif bg == bloog_grp[1]:
        pygame.mixer.music.load(r'F:\The Survival Game\audio_O2.mp3')
        count = score[0]+score[2] + score[3] + score[4] + score[5] + score[6] + score[7]
        if count == 0:
            high_sc = score[1]
    elif bg == bloog_grp[2]:
        pygame.mixer.music.load(r'F:\The Survival Game\audio_A1.mp3')
        count = score[4] + score[5] + score[6] + score[7]
        if count == 0:
            high_sc = score[0] + score[1] + score[2] + score[3]
    elif bg == bloog_grp[3]:
        pygame.mixer.music.load(r'F:\The Survival Game\audio_A2.mp3')
        count = score[0] + score[2] + score[4] + score[5] + score[6] + score[7]
        if count == 0:
            high_sc = score[1] + score[3]
    elif bg == bloog_grp[4]:
        pygame.mixer.music.load(r'F:\The Survival Game\audio_B1.mp3')
        count = score[2] + score[3] + score[6] + score[7]
        if count == 0:
            high_sc = score[0] + score[1] + score[4] + score[5]
    elif bg == bloog_grp[5]:
        pygame.mixer.music.load(r'F:\The Survival Game\audio_B2.mp3')
        count = score[0] + score[2] + score[3] + score[4] + score[6] + score[7]
        if count == 0:
            high_sc = score[1] + score[5]
    elif bg == bloog_grp[6]:
        pygame.mixer.music.load(r'F:\The Survival Game\audio_AB1.mp3')
        if count == 0:
            high_sc = score[0] + score[1] + score[2] + score[3] + score[4] + score[5] + score[6] + score[7]
    elif bg == bloog_grp[7]:
        pygame.mixer.music.load(r'F:\The Survival Game\audio_AB2.mp3')
        count = score[0] + score[2] + score[4] + score[6]
        if count == 0:
            high_sc = score[1] + score[3] + score[5] + score[7]
    if high_sc<10 and bg != bloog_grp[1]:
        high_sc = 0
    elif bg == bloog_grp[1] and high_sc<5:
        high_sc=0
    if bg == bloog_grp[6] and high_sc in range(10,25):
        high_sc = 0
    print(high_sc*10)
    return high_sc*10

def draw_bar(score):
    #        score=(sc_O1,sc_O2,sc_A1,sc_A2,sc_B1,sc_B2,sc_AB1,sc_AB2)
    # Write into csv file
    fields = ['Blood Group', 'Count']
    with open(r'F:\The Survival Game\Blood_grp_data.csv', 'w+') as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(fields)
        filewriter.writerow(['A+', score[2]])
        filewriter.writerow(['A-', score[3]])
        filewriter.writerow(['B+', score[4]])
        filewriter.writerow(['B-', score[5]])
        filewriter.writerow(['AB+', score[6]])
        filewriter.writerow(['AB-', score[7]])
        filewriter.writerow(['O+', score[0]])
        filewriter.writerow(['O-', score[1]])
    bldgrp = []
    count = []
    with open(r'F:\The Survival Game\Blood_grp_data.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for col in csvreader:
            bldgrp.append(col['Blood Group'])
            count.append(int(col['Count']))

    xindex = np.arange(len(bldgrp))
    max_count = max(count)
    yindex = np.arange(max_count + 1)
    fig = plt.figure(figsize=(6, 3))
    ax = plt.subplot(111)
    ax.bar(xindex, count, label='Blood bags collected', color='maroon')
    plt.xlabel('Blood Groups', )
    plt.ylabel('Total Number of packets', fontname='Chiller', fontsize=15, color='maroon')
    plt.xticks(xindex, bldgrp, fontname='Chiller', fontsize=15, rotation=30, color='maroon')
    plt.yticks(yindex, yindex, fontname='Chiller', fontsize=10, color='maroon')
    ax.legend()
    fig.savefig(r'F:\The Survival Game\plot.png')
    csvfile.close()
    print(bldgrp)
    print(count)

def screen1():
    global exit_game
    disp_screen1 = True
    img_box = pygame.image.load(r'F:\The Survival Game\box_inactive.png')
    active = False
    bg = ''
    while disp_screen1 and not exit_game:
        #print(bg)
        gameDisp.blit(score_bg1, (0, 0))
        text_screen("THE  SURVIVAL  GAME!!", white, 85, 110,20)
        text_screen('To enter your blood group click on the box:', maroon, 50, 130, 320)
        text_screen('(Example: A+)',maroon,20,400,380)
        gameDisp.blit(img_box, (360, 410))
        text_screen(bg, maroon, 70, 400, 420)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if mx in range(360, 540) and my in range(400, 494):
                    img_box = pygame.image.load(r'F:\The Survival Game\box_active.png')
                    pygame.mixer.Sound.play(button_press)
                    active = True
                else:
                    continue
            elif active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and bg == '':
                    t = 'A'
                    bg = bg + t
                if event.key == pygame.K_b and (bg == '' or bg == 'A'):
                    t = 'B'
                    bg = bg + t
                if event.key == pygame.K_o and bg == '':
                    t = 'O'
                    bg = bg + t
                if event.key == pygame.K_KP_PLUS and (bg == 'A' or bg == 'B' or bg == 'AB' or bg == 'O'):
                    t = '+'
                    bg = bg + t
                if event.key == pygame.K_KP_MINUS and (bg == 'A' or bg == 'B' or bg == 'AB' or bg == 'O'):
                    t = '-'
                    bg = bg + t
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    disp_screen1 = False
                    break
            elif not active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(button_press)
                    disp_screen1 = False
                    break
            elif event.type == pygame.QUIT:
                disp_screen1 = False
                exit_game = True
    if bg not in bloog_grp:
        bg = random.choice(bloog_grp)
    return bg

def screen2(bg):
    global exit_game
    disp_screen2 = True
    play = pygame.image.load(r'F:\The Survival Game\play.png')
    bg_speech = bg
    if bg == bloog_grp[0] or bloog_grp[2] or bloog_grp[4] or bloog_grp[6]:
        bg_speech = bg_speech.replace('+', ' positive')
        print(bg_speech)
    if bg == bloog_grp[1] or bloog_grp[3] or bloog_grp[5] or bloog_grp[7]:
        bg_speech = bg_speech.replace('-', ' negative')
        print(bg_speech)
    script = gTTS(
        text="Hello! Your blood group is " + bg_speech + ". Collect minimum ten blood bags to survive, but make sure the blood bags match your, blood type.",
        lang='en',
        slow=False, )
    script.save("Script.mp3")
    pygame.mixer.music.load(r"F:\The Survival Game\Script.mp3")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()
    while disp_screen2 and not exit_game:
        gameDisp.blit(score_bg1, (0, 0))
        x=110
        y=180
        txt_size = 50
        text_screen("THE  SURVIVAL  GAME!!", white, 80, x,y-160)
        text_screen("Your blood group is:", maroon, txt_size, x+220, y+90)
        text_screen(bg, maroon, 80, x+320, y+135)
        text_screen("Collect minimum 10 blood bags to survive", maroon, txt_size, x+40, y+230)
        text_screen("But make sure the blood bags match your", maroon, txt_size, x+40, y+280)
        text_screen("BLOOD TYPE", maroon, txt_size, x+250, y+340)
        gameDisp.blit(play,(690,526))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()
                if mx in range(690,890) and my in range(526,590):
                    disp_screen2 = False
                    pygame.mixer.Sound.play(button_press)
                    break
                else:
                    continue
            elif event.type == pygame.QUIT:
                disp_screen2 = False
                exit_game = True

def gameloop():
    global exit_game
    game_over = False
    bg = screen1()
    screen2(bg)
    sc=pygame.image.load(r'F:\The Survival Game\score.png')
    x = y = 0
    px = 180
    py = 240
    pos = 0
    bx1 = 900
    by1 = random.randrange(10, 490)
    if bg == bloog_grp[1]:
        bb1 = random.choice(blood_bag[6:7])
    else:
        bb1 = random.choice(blood_bag)
    bx2 = 1200
    by2 = random.randrange(10, 490)
    if bg == bloog_grp[3] or bg == bloog_grp[5]:
        bb2 = random.choice(blood_bag[0:3])
    else:
        bb2 = random.choice(blood_bag)
    bx3 = 1500
    by3 = random.randrange(10, 490)
    if bg == bloog_grp[0]:
        bb3 = random.choice(blood_bag[4:7])
    else:
        bb3 = random.choice(blood_bag)
    collide = False

    bb_count=3
    sc_A1 = 0
    sc_A2 = 0
    sc_B1 = 0
    sc_B2 = 0
    sc_AB1 = 0
    sc_AB2 = 0
    sc_O1 = 0
    sc_O2 = 0
    col_sound = pygame.mixer.Sound(r'F:\The Survival Game\bag_collect.wav')
    pygame.mixer.music.load(r"F:\The Survival Game\ambsund.mp3")
    pygame.mixer.music.play(-1)
    while not exit_game and not game_over:
        gameDisp.blit(bgrn, [x, y])
        gameDisp.blit(bgrn, [x+game_width, y])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pos = -8
                elif event.key == pygame.K_DOWN:
                    pos = 8

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or pygame.K_DOWN:
                    pos = 0

        if py>0 and py<game_height-p_height:
            py += pos
        elif py<=0:
            py = 2
        else:
            py -= 8

        player_move(px, py)

        if bx1>-bb_width:
            bx1 -= 4
            if bx1 in range(px,px+p_width) and (by1 in range(py,py+p_height) or by1+bb_height in range(py,py+p_height)):
                collide = True
                pygame.mixer.Sound.play(col_sound)
            elif bx1+bb_width in range(px,px+p_width) and (by1 in range(py,py+p_height) or by1+bb_height in range(py,py+p_height)):
                collide = True
                pygame.mixer.Sound.play(col_sound)
            if not collide:
               gameDisp.blit(bb1, [bx1, by1])
            else:
                if bb1 == bb_A1:
                    sc_A1+=1
                elif bb1 == bb_A2:
                    sc_A2+=1
                elif bb1 == bb_B1:
                    sc_B1+=1
                elif bb1 == bb_B2:
                    sc_B2+=1
                elif bb1 == bb_AB1:
                    sc_AB1+=1
                elif bb1 == bb_AB2:
                    sc_AB2+=1
                elif bb1 == bb_O1:
                    sc_O1+=1
                elif bb1 == bb_O2:
                    sc_O2+=1
                bx1 = 900
                by1 = random.randrange(10, 490)
                bb1 = random.choice(blood_bag)
                bb_count+=1
                collide = False

        if bx2>-bb_width:
            bx2 -= 4
            if bx2 in range(px,px+p_width) and (by2 in range(py,py+p_height) or by2+bb_height in range(py,py+p_height)):
                collide = True
                pygame.mixer.Sound.play(col_sound)
            elif bx2+bb_width in range(px,px+p_width) and (by2 in range(py,py+p_height) or by2+bb_height in range(py,py+p_height)):
                collide = True
                pygame.mixer.Sound.play(col_sound)
            if not collide:
               gameDisp.blit(bb2, [bx2, by2])
            else:
                if bb2 == bb_A1:
                    sc_A1+=1
                elif bb2 == bb_A2:
                    sc_A2+=1
                elif bb2 == bb_B1:
                    sc_B1+=1
                elif bb2 == bb_B2:
                    sc_B2+=1
                elif bb2 == bb_AB1:
                    sc_AB1+=1
                elif bb2 == bb_AB2:
                    sc_AB2+=1
                elif bb2 == bb_O1:
                    sc_O1+=1
                elif bb2 == bb_O2:
                    sc_O2+=1
                bx2 = 900
                by2 = random.randrange(10, 490)
                bb2 = random.choice(blood_bag)
                bb_count+=1
                collide = False
                
        if bx3>-bb_width:
            bx3 -= 4
            if bx3 in range(px,px+p_width) and (by3 in range(py,py+p_height) or by3+bb_height in range(py,py+p_height)):
                collide = True
                pygame.mixer.Sound.play(col_sound)
            elif bx3+bb_width in range(px,px+p_width) and (by3 in range(py,py+p_height) or by3+bb_height in range(py,py+p_height)):
                collide = True
                pygame.mixer.Sound.play(col_sound)
            if not collide:
               gameDisp.blit(bb3, [bx3, by3])
            else:
                if bb3 == bb_A1:
                    sc_A1+=1
                elif bb3 == bb_A2:
                    sc_A2+=1
                elif bb3 == bb_B1:
                    sc_B1+=1
                elif bb3 == bb_B2:
                    sc_B2+=1
                elif bb3 == bb_AB1:
                    sc_AB1+=1
                elif bb3 == bb_AB2:
                    sc_AB2+=1
                elif bb3 == bb_O1:
                    sc_O1+=1
                elif bb3 == bb_O2:
                    sc_O2+=1
                bx3 = 900
                by3 = random.randrange(10, 490)
                bb3 = random.choice(blood_bag)
                bb_count+=1
                collide = False
                
        if bx1<=-bb_width:
            bx1 = 900
            by1 = random.randrange(10, 490)
            bb1 = random.choice(blood_bag)
            bb_count += 1
            collide=False
        if bx2<=-bb_width:
            bx2 = 1200
            by2 = random.randrange(10, 490)
            bb2 = random.choice(blood_bag)
            bb_count += 1
            collide=False
        if bx3<=-bb_width:
            bx3 = 1500
            by3 = random.randrange(10, 490)
            bb3 = random.choice(blood_bag)
            bb_count += 1
            collide=False

        if bb_count == 50:
            game_over = True
        x-=5
        if x == -game_width:
            x=0
        sum=sc_O1+sc_O2+sc_AB1+sc_AB2+sc_B1+sc_B2+sc_A1+sc_A2
        gameDisp.blit(sc,(10,10))
        text_screen(str(sum), white, 50, 65, 20)
        pygame.display.update()
        clock.tick(fps)

    if game_over and not exit_game:
        bar_screen = True
        score_screen = True
        score=(sc_O1,sc_O2,sc_A1,sc_A2,sc_B1,sc_B2,sc_AB1,sc_AB2)
        pygame.mixer.music.fadeout(2000)
        draw_bar(score)
        score_bg1 = pygame.image.load(r'F:\The Survival Game\score_bg1.png')
        plot = pygame.image.load(r'F:\The Survival Game\plot.png')
        gameDisp.blit(score_bg1, (0, 0))
        text_screen('Score Board', white, 80, 320, 20)
        gameDisp.blit(plot, (150, 230))
        pygame.display.update()
        hsc = highscore(score,bg)
        pygame.mixer.music.play()
        while bar_screen and not exit_game:
            gameDisp.blit(score_bg1, (0, 0))
            text_screen('Score Board',white,80,320,20)
            gameDisp.blit(plot, (150, 230))
            text_screen("Press SPACE BAR to see result...", maroon, 40, 450, 540)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bar_screen = False
                        pygame.mixer.Sound.play(button_press)
                        break
                    else:
                        continue
                elif event.type == pygame.QUIT:
                    bar_screen = False
                    exit_game = True
                    break
        txt_size=70
        wx=350
        lx=375
        ty=260
        while score_screen and not exit_game:
            pygame.mixer.music.stop()
            txt_size+=1
            ty-=1
            gameDisp.fill(white)
            if hsc!=0 and txt_size<200:
                wx-=2
                text_screen("SURVIVED!!",maroon,txt_size,wx,ty)
            elif hsc==0 and txt_size<200:
                lx-=1
                text_screen("DEAD!!", maroon,txt_size, lx, ty)

            if txt_size>=200:
                txt_size=70
                wx = 350
                lx = 375
                ty = 260
            gameDisp.blit(sc,(10,10))
            text_screen(str(hsc),white,50,65,20)
            text_screen("Press SPACE BAR to play again...",maroon,40,450,540)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.Sound.play(button_press)
                        return
                    else:
                        continue
                elif event.type == pygame.QUIT:
                    score_screen = False
                    exit_game = True
                    break

    if exit_game:
        pygame.quit()
        quit()

welcome()