#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import pygame
import random
from pygame.locals import *
from itertools import cycle

SCREENWIDTH = 822
SCREENHEIGHT = 199
FPS = 30

#背景
class MyMap():
    def __init__(self, x,y):
        # self.bg = pygame.image.load("image/bg.png").convert_alpha()
        self.bg = pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\bg.png").convert_alpha()
        self.x = x
        self.y = y

    def map_rolling(self):
        if self.x < -790:
            self.x = 800
        else:
            self.x -= 5

    def map_update(self):
        SCREEN.blit(self.bg, (self.x, self.y))

#玛丽
class Marie():
    def __init__(self):
        self.rect = pygame.Rect(0,0,0,0)
        self.jumpState = False
        self.jumpHeight = 120
        self.lowest_y = 140
        self.jumpValue = 0
        
        self.marieIndex = 0
        self.marieIndexGen = cycle([0,1,2])

        # 加载小玛丽图片
        self.adventure_img = (
            pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\adventure1.png").convert_alpha(),
            pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\adventure2.png").convert_alpha(),
            pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\adventure3.png").convert_alpha(),
        )
        # self.jump_audio = pygame.mixer.Sound(r'C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\audio\\jump.wav')  # 跳音效
        self.rect.size = self.adventure_img[0].get_size()
        self.x = 50;  # 绘制小玛丽的X坐标
        self.y = self.lowest_y;  # 绘制小玛丽的Y坐标
        self.rect.topleft = (self.x, self.y)

    def jump(self):
        self.jumpState = True

    def move(self):
        if self.jumpState:  # 当起跳的时候
            if self.rect.y >= self.lowest_y:  # 如果站在地上
                self.jumpValue = -5  # 以5个像素值向上移动
            if self.rect.y <= self.lowest_y - self.jumpHeight:  # 小玛丽到达顶部回落
                self.jumpValue = 5  # 以5个像素值向下移动
            self.rect.y += self.jumpValue  # 通过循环改变玛丽的Y坐标
            if self.rect.y >= self.lowest_y:  # 如果小玛丽回到地面
                self.jumpState = False  # 关闭跳跃状态

    # 绘制小玛丽
    def draw_marie(self):
        # 匹配小玛丽动图
        marieIndex = next(self.marieIndexGen)
        # 绘制小玛丽
        SCREEN.blit(self.adventure_img[marieIndex],(self.x, self.rect.y))

#障碍物
class Obstacle():
    score = 1
    move = 5
    obstacle_y = 150

    def __init__(self):
        #初始化障碍物矩形
        self.rect = pygame.Rect(0,0,0,0)
        #加载障碍物图片
        self.missile = pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\missile.png")
        self.pipe = pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\pipe.png")

        #加载分数图片
        self.numbers = (
            pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\1.png").convert_alpha(),
            pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\2.png").convert_alpha(),
            pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\3.png").convert_alpha(),
            pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\4.png").convert_alpha(),
            pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\5.png").convert_alpha(),
            pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\6.png").convert_alpha(),
            pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\7.png").convert_alpha(),
            pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\8.png").convert_alpha(),
            pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\9.png").convert_alpha()
        )

        # self.score_audio = pygame.mixer.Sound(r'C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\audio\\score.wav')
        
        r = random.randint(0,1)
        if r == 0:
            self.image = self.missile
            self.move = 15
            self.obstacle_y = 100
        else:
            self.image = self.pipe

        self.rect.size = self.image.get_size()
        self.width, self.height = self.rect.size

        self.x = 800
        self.y = self.obstacle_y
        self.rect.center = (self.x,self.y)

    def obstacle_move(self):
        self.rect.x -= self.move


    def draw_obstacle(self):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))


    def getScore(self):
        self.score
        tem =self.score
        if tem == 1:
            # self.score_audio.play()
            pass
        self.score = 0
        return tem

    def showScore(self,score):
        self.scoreDigits = [int(x) for x in list(str(score))]
        totalWidth = 0
        for digit in self.scoreDigits:
            totalWidth += self.numbers[digit].get_width()
        Xoffset = (SCREENWIDTH- totalWidth + 30)
        for digit in self.scoreDigits:
            SCREEN.blit(self.numbers[digit], (Xoffset, SCREENHEIGHT*0.1))
            Xoffset += self.numbers[digit].get_width()


#音乐播放
class Music_Button():
    is_open = True
    def __init__(self):
        self.open_img = pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\btn_open.png").convert_alpha()
        self.close_img = pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\btn_close.png").convert_alpha()
        # self.bg_music = pygame.mixer.Sound(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\audio\\bg_music.wav")

    #判断鼠标是否在按钮的范围内
    def is_select(self):
        point_x, point_y = pygame.mouse.get_pos()
        w,h = self.open_img.get_size()
        in_x = point_x >20 and point_x < 20+w
        in_y = point_y >20 and point_y < 20+h
        return in_x and in_y



def game_over():
    # bump_audio = pygame.mixer.Sound(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\audio\\bump.wav")
    # bump_audio.play()

    screen_w = pygame.display.Info().current_w
    screen_h = pygame.display.Info().current_h

    over_img = pygame.image.load(r"C:\\Users\\Administrator\\Desktop\\oeasy\\data\\mine\\python\\marie_adventure\\image\\gameover.png").convert_alpha()

    SCREEN.blit(over_img, ((screen_w - over_img.get_width())/2, (screen_h - over_img.get_height())/2 ))


def mainGame():
    # 创建地图对象
    score = 0
    over = False
    global SCREEN,FPSCLOCK
    addObstacleTimer = 0
    list = []

    pygame.init()
    # pygame.mixer.init()  
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("玛利冒险")

    bg1 = MyMap(0, 0)
    bg2 = MyMap(800, 0)
    # 创建小玛丽对象
    marie = Marie()
    music_button = Music_Button()
    btn_img = music_button.open_img
    # music_button.bg_music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:  # 判断鼠标事件
                if music_button.is_select():        # 判断鼠标是否在静音按钮范围
                    if music_button.is_open:        # 判断背景音乐状态
                        btn_img = music_button.close_img # 单击后显示关闭状态的图片
                        music_button.is_open = False    # 关闭背景音乐状态
                        # music_button.bg_music.stop()    # 停止背景音乐的播放
                    else:
                        btn_img = music_button.open_img
                        music_button.is_open = True
                        # music_button.bg_music.play(-1)


            if event.type == QUIT:
                pygame.quit()
                sys.exit()


            # 单击键盘空格键，开启跳的状态
            if event.type == KEYDOWN and event.key == K_SPACE:
                if marie.rect.y >= marie.lowest_y:  # 如果小玛丽在地面上
                    # marie.jump_audio.play()  # 播放小玛丽跳跃音效
                    marie.jump()  # 开启小玛丽跳的状态

                if over == True:  # 判断游戏结束的开关是否开启
                    mainGame()  # 如果开启将调用mainGame方法重新启动游戏
        

        if over == False:
            # 绘制地图起到更新地图的作用
            bg1.map_update()
            # 地图移动
            bg1.map_rolling()
            bg2.map_update()
            bg2.map_rolling()

            # 小玛丽移动
            marie.move()
            # 绘制小玛丽
            marie.draw_marie()

            # 计算障碍物间隔时间
            if addObstacleTimer >= 800:
                r = random.randint(0, 100)
                if r > 40:
                    # 创建障碍物对象
                    obstacle = Obstacle()
                    # 将障碍物对象添加到列表中
                    list.append(obstacle)
                # 重置添加障碍物时间
                addObstacleTimer = 0

            # 循环遍历障碍物
            for i in range(len(list)):
                # 障碍物移动
                list[i].obstacle_move()
                # 绘制障碍物
                list[i].draw_obstacle()

                # 判断小玛丽与障碍物是否碰撞
                if pygame.sprite.collide_rect(marie, list[i]):
                    over = True  # 碰撞后开启结束开关
                    game_over()  # 调用游戏结束的方法
                    # music_button.bg_music.stop()
                else:
                    # 判断小玛丽是否跃过了障碍物
                    if (list[i].rect.x + list[i].rect.width) < marie.rect.x:
                        # 加分
                        score += list[i].getScore()
                # 显示分数
                list[i].showScore(score)


        addObstacleTimer += 20  # 增加障碍物时间
        SCREEN.blit(btn_img, (20, 20)) # 绘制背景音乐按钮
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    mainGame()