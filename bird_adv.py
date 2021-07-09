import random 
import sys
import pygame
import pygame.locals
#global variables
FPS=20
width =289
height=511
screen =pygame.display.set_mode((width,height))
ground=int(height*0.8)
objects={}
game_sounds={}
player='gallery/objects/bird.png'
bg='gallery/objects/bg_fp.png'
pipe='gallery/objects/pipe.png'
base='gallery/objects/base.png'
clock=pygame.time.Clock
def move_floor(base_x):
    screen.blit(objects['base'],(base_x+0,ground))
    screen.blit(objects['base'],(base_x+289,ground))

def welcomeScreen():
    messagex = int((width - objects['message'].get_width())/2)
    messagey = int(height*0.13)
    player_x=int(width/5)
    player_y=int((height-objects['player'].get_height())/2)
    base_x=0
    while True:
        for event in pygame.event.get():
            if event.type== pygame.QUIT or (event.type== pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN and (event.key==pygame.K_SPACE or event.key ==pygame.K_UP):
                return
            else:
                screen.blit(objects['bg'],(0,0))
                screen.blit(objects['player'],(player_x,player_y))
                screen.blit(objects['message'],(0,0))
                #screen.blit(objects['base'],(base_x,ground))
                pygame.display.update()
                clock.tick(FPS)
def check_collision(player_x,player_y,upperPipe,lowerPipe):
    if player_y>ground-25 or player_y<0:
        game_sounds['hit'].play()
        return True
    for pipe in upperPipe:
        #print(objects['pipe'](0).get_width())
        pipeHeight=(objects['pipe'][0].get_height())
        if (player_y<(pipe['y']+pipeHeight) and abs(player_x-pipe['x']-objects['player'].get_width()//2)<objects['pipe'][0].get_width()):
            game_sounds['hit'].play()
            return True
    for pipe in lowerPipe:
        #print(objects['pipe'](0).get_width())
        if (player_y+objects['player'].get_height())>pipe['y'] and  abs(player_x-pipe['x']-objects['player'].get_width()//2)<objects['pipe'][1].get_width():
            game_sounds['hit'].play()
            return True
    return False
def maingame():
    score=0
    base_x=0
    player_x=int(width/5)
    player_y=int(width/5)
    newPipe1=getRandomPipe()
    newPipe2=getRandomPipe()
    upperPipe=[
        {'x':width+200,'y':newPipe1[0]['y']},
        {'x':width+200+(width/2),'y':newPipe2[0]['y']}
    ]
    lowerPipe=[
        {'x':width+200,'y':newPipe1[1]['y']},
        {'x':width+200+(width/2),'y':newPipe2[1]['y']}
    ]
    pipvel_x=-4
    playervel_y=-9
    playerMaxvelY=10
    playerMinvelY=-8
    playerAccY=1
    
    playerFlapv=-8
    playerflapped=False
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or(event.type==pygame.KEYDOWN and event.type==pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type ==pygame.KEYDOWN and(event.key==pygame.K_SPACE or event.key==pygame.K_UP):
                if player_y> 0:
                    playervel_y=playerFlapv
                    playerflapped=True
                    game_sounds['wing'].play()
        crashtest=check_collision(player_x,player_y,upperPipe,lowerPipe)
        if crashtest:
            return
        playerMid=(player_x+objects['player'].get_width()/2)
        for pipe in upperPipe:
            pipeMidPos=pipe['x']+objects['pipe'][0].get_width()/2
            if pipeMidPos<=playerMid<pipeMidPos+4:
                score+=1
                print(f"Your Score is : {score}")
                game_sounds['point'].play()
        if playervel_y<playerMaxvelY and not playerflapped:
            playervel_y+=playerAccY
        if playerflapped:
            playerflapped=False
        playerHeight =  objects['player'].get_height()
        player_y = player_y + min(playervel_y,ground-player_y-playerHeight)
        
        for upper,lower in zip(upperPipe,lowerPipe):
            upper['x']+=pipvel_x
            lower['x']+=pipvel_x
        
        if 0<upperPipe[0]['x']<5:
            newPipe=getRandomPipe()
            upperPipe.append(newPipe[0])
            lowerPipe.append(newPipe[1])
        
        if upperPipe[0]['x']<-objects['pipe'][0].get_width():
            upperPipe.pop(0)
            lowerPipe.pop(0) 
        
        screen.blit(objects['bg'],(0,0))
        base
        for upper,lower in zip(upperPipe,lowerPipe):
            screen.blit(objects['pipe'][0],(round(upper['x']),round(upper['y'])))
            screen.blit(objects['pipe'][1],(round(lower['x']),round(lower['y'])))
        screen.blit(objects['player'],(player_x,player_y))
        base_x-=5
        if base_x<-289:
            base_x=0
        move_floor(base_x)
        #screen.blit(objects['base'],(base_x,ground))
        mydigits=[int(x) for x in list(str(score))]    
        width_num = 0
        for digit in mydigits:
            width_num+=objects['numbers'][digit].get_width()
        xoffset=(width - width_num)/2
        for digit in mydigits:
            screen.blit(objects['numbers'][digit],(round(xoffset),round(height*0.12)))
            xoffset+=objects['numbers'][digit].get_width()
        pygame.display.update()
        clock.tick(FPS)
def getRandomPipe():
    pipeHeight=objects['pipe'][0].get_height()
    offset=height/3
    y2=offset+random.randrange(0,int(height-objects['base'].get_height()-1.2*offset))
    pipeX=width+10
    y1=pipeHeight-y2+offset
    pipe=[ 
        {'x':pipeX,'y':-y1},
        {'x':pipeX,'y':y2}
    ]
    return pipe
if __name__=="__main__":
    #main function
    pygame.init()
    clock=pygame.time.Clock()
    pygame.display.set_caption("CG PROJECT")
    objects['numbers']=(
        pygame.image.load('gallery/objects/0.png').convert_alpha(),
        pygame.image.load('gallery/objects/1.png').convert_alpha(),
        pygame.image.load('gallery/objects/2.png').convert_alpha(),
        pygame.image.load('gallery/objects/3.png').convert_alpha(),
        pygame.image.load('gallery/objects/4.png').convert_alpha(),
        pygame.image.load('gallery/objects/5.png').convert_alpha(),
        pygame.image.load('gallery/objects/6.png').convert_alpha(),
        pygame.image.load('gallery/objects/7.png').convert_alpha(),
        pygame.image.load('gallery/objects/8.png').convert_alpha(),
        pygame.image.load('gallery/objects/9.png').convert_alpha()
    )
    objects['message']=pygame.transform.scale(pygame.image.load('gallery/objects/wel.png'),(width,height)).convert()
    objects['base']=pygame.image.load('gallery/objects/base.png').convert_alpha()
    objects['pipe']=(pygame.transform.rotate(pygame.image.load( pipe).convert_alpha(),180),
    pygame.image.load(pipe).convert_alpha()
    )
    game_sounds['die']=pygame.mixer.Sound('gallery/audio/die.wav')
    game_sounds['hit']=pygame.mixer.Sound('gallery/audio/die.wav')
    game_sounds['point']=pygame.mixer.Sound('gallery/audio/point.wav')
    game_sounds['swoosh']=pygame.mixer.Sound('gallery/audio/swoosh.wav')
    game_sounds['wing']=pygame.mixer.Sound('gallery/audio/wing.wav')
    objects['bg']=pygame.image.load(bg).convert()
    objects['player']=pygame.image.load(player).convert_alpha()
    while True:
        welcomeScreen()
        maingame()


