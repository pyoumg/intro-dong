import pygame
import time
import sys, os
import random

pygame.init()
pygame.mixer.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BLUE = (125, 170, 209)
# GREEN= ( 166,195,  92)
# RED  = (204,  133,  147)

size = [800, 600]
gameDisplay = pygame.display.set_mode(size)


# image
titleImg = pygame.image.load("images/title.png")
startImg = pygame.image.load("images/starticon.png")
quitImg = pygame.image.load("images/quiticon.png")
easyImg = pygame.image.load("images/easy.png")
normalImg = pygame.image.load("images/normal.png")
hardImg = pygame.image.load("images/hard.png")
selectImg = pygame.image.load("images/select.png")
playImg = pygame.image.load("images/play.png")
okImg = pygame.image.load("images/ok.png")
noImg = pygame.image.load("images/no.png")
nextImg=pygame.image.load("images/next.png")
finishImg=pygame.image.load("images/finish.png")
mainImg=pygame.image.load("images/main.png")

# click
clickStartImg = pygame.image.load("images/clickedStartIcon.png")
clickQuitImg = pygame.image.load("images/clickedQuitIcon.png")
clickEasyImg = pygame.image.load("images/clickedEasy.png")
clickNormalImg = pygame.image.load("images/clickedNormal.png")
clickHardImg = pygame.image.load("images/clickedHard.png")
clickPlayImg = pygame.image.load("images/clickedPlay.png")
clickNextImg=pygame.image.load("images/clickedNext.png")
clickFinishImg=pygame.image.load("images/clickedFinish.png")
clickMainImg=pygame.image.load("images/clickedMain.png")



clock = pygame.time.Clock()
global level # 레벨 전역변수
# 초기값 0, 0(easy)-1-2(hard)
global score
global songFlag
global rightFlag
rightFlag=0
level=0
songFlag=False
score = 0
pygame.display.set_caption("Intro-dong")


class Button:
    def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()  # 클릭
        if x + width > mouse[0] > x and y + height > mouse[1] > y:  # 안쪽
            gameDisplay.blit(img_act, (x_act, y_act))
            if click[0] and action != None:  # 클릭
                time.sleep(1)  # 1초 지연
                action()
        else:  # 바깥
            gameDisplay.blit(img_in, (x, y))


class Button2:  # action에 args가 있는 button
    def __init__(
        self, img_in, x, y, width, height, img_act, x_act, y_act, action=None, arg=None
    ):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()  # 클릭
        if x + width > mouse[0] > x and y + height > mouse[1] > y:  # 안쪽
            gameDisplay.blit(img_act, (x_act, y_act))
            if click[0] and action != None:  # 클릭
                time.sleep(1)  # 1초 지연
                action(arg)
        else:  # 바깥
            gameDisplay.blit(img_in, (x, y))


class Text:
    def __init__(self, text, x, y, action=None, arg=None):
        largeText = pygame.font.SysFont("malgungothic", 25)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()  # 클릭
        if 750 > mouse[0] > 50 and y + 20 > mouse[1] > y - 20:  # 안쪽
            TextSurf, TextRect = text_objects(text, largeText, BLUE)
            TextRect.center = (400, y)

            gameDisplay.blit(TextSurf, TextRect)

            if click[0] and action != None:  # 클릭
                time.sleep(1)  # 1초 지연
                action(arg)
        else:  # 바깥
            TextSurf, TextRect = text_objects(text, largeText, BLACK)
            TextRect.center = (400, y)
            gameDisplay.blit(TextSurf, TextRect)


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def quitgame():
    pygame.quit()
    sys.exit()


def setLevel(num):
    global level
    level = num
    playScreen()


def getSongs():
    files = os.listdir("./songs")
    songs = list()
    for file in files:
        if ".mp3" in file:  # mp3 파일만
            songs.append(file)
    random.shuffle(songs)
    songs = songs[:40]  # 40개 무작위 뽑기
    return songs


def playSong(answer):
   
    global level
    try:
        pygame.mixer.music.load(r"./songs/" + answer)
        pygame.mixer.music.play()
        start = time.time()
        while True:
            if time.time() - start >= 3 - level:
                break
        pygame.mixer.music.stop()
    except:
        pass


def checkAns(li):
    #li[0]:누른 버튼
    #li[1]: 정답
    global score
    global rightFlag

    if rightFlag>0:
        return #이미 선택 했으면 못바꿈

    if li[0]==li[1]:
        rightFlag=5
        score+=1
    else:
        rightFlag=li[0]
    
def setInit():
    global songFlag
    global rightFlag
    songFlag=False
    rightFlag=0


def showScore():
    
    global score
    show=True

    while show:
        gameDisplay.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        stageText = Text("Score: " + str(score), 200,200)
        mainButton=Button(
            mainImg, 330, 400, 120, 55, clickMainImg, 327, 397, mainMenu
        )


        pygame.display.update()
        clock.tick(15)



def playScreen():
    gameexit = False
    songs = getSongs()
    global songFlag
    songTest = []
    songText = []
    stage = 0

    while not gameexit:
        gameDisplay.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        if songFlag is False:
            songTest = songs[stage*4 : stage*4 + 4]
            answer = random.randrange(0, 4)
            songFlag = True
            stage += 1
            songText = [None, None, None, None]

        stageText = Text("stage " + str(stage), 200, 50)
        for i in range(4):
            songText[i] = Text(
                songTest[i][: len(songTest[i]) - 4],
                50,
                i * 100 + 170,
                checkAns,[i,answer]
            )
        playButton = Button2(
            playImg, 650, 10, 130, 130, clickPlayImg, 647, 7, playSong, songTest[answer]
        )
        if rightFlag>0:
            gameDisplay.blit(okImg, (0, answer*100+150))
            if rightFlag<5:
                gameDisplay.blit(noImg, (0, rightFlag*100+150))
            if stage<10:
                nextButton=Button(nextImg,650,500,120,55,clickNextImg,647,497,setInit)
            else:
                finishButton=Button(finishImg,650,490,135,55,clickFinishImg,647,487,showScore)

        

        pygame.display.update()
        clock.tick(15)


def mainMenu():
    global score

    score = 0

    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 닫기 버튼
                quitgame()

        gameDisplay.fill(WHITE)

        titletext = gameDisplay.blit(titleImg, (220, 150))
        startButton = Button(
            startImg, 280, 400, 60, 20, clickStartImg, 277, 397, selectScreen
        )
        quitButton = Button(quitImg, 445, 400, 84, 25, clickQuitImg, 442, 397, quitgame)
        pygame.display.update()
        clock.tick(15)


def selectScreen():
    select = True
    while select:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        gameDisplay.fill(WHITE)
        gameDisplay.blit(selectImg, (200, 50))

        easySelect = Button2(
            easyImg, 350, 250, 120, 55, clickEasyImg, 347, 247, setLevel, 0
        )
        normalSelect = Button2(
            normalImg, 325, 350, 175, 55, clickNormalImg, 323, 347, setLevel, 1
        )
        hardSelect = Button2(
            hardImg, 350, 450, 120, 55, clickHardImg, 347, 447, setLevel, 2
        )

        pygame.display.update()
        clock.tick(15)


mainMenu()  # 함수 호출
