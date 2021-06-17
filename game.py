# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 16:45:47 2021

@author: Wuwei
"""

import sys
import pygame
import time
import random
import json

dic = {}

def get_words(filename):
    """将英文单词读取到字典中"""
    with open(filename, 'r', encoding = 'utf-8')as f:
        global dic 
        dic = json.load(f)
        
def choose_word(dic):
    """将抽取到的单词以及其他的释义放入列表中，列表的第一个元素为单词及其正确含义
    的元组，其他三个元素为中文释义干扰项"""
    li = []
    t = random.randrange(len(dic))
    chosen_word = list(dic.items())[t]
    li.append(chosen_word)
    del dic[f'{chosen_word[0]}']
    lii = []
    for i in range(3):
        t = random.randrange(len(dic))
        if t not in lii:
            lii.append(t)
            li.append(list(dic.values())[t])
        else:
            i -= 1
    return li
        
def load_images(screen): 
    """将选项框及其位置储存在字典中"""
    image = pygame.image.load('D:/Wuwei/Computer_Science/Computer_Science_assignment'
                               +'/python/final_test/images/button.png')
    image_dic = {}
    image0 = pygame.transform.scale(image, (550, 70))#调整图片大小
    rect0 = image0.get_rect()
    rect_x = screen.get_rect().centerx - 1/2*rect0.width
    pygame.Rect.move_ip(rect0, rect_x, 125)
    image_dic[image0] = rect0
    
    image1 = pygame.transform.scale(image, (550, 70))
    rect1 = image1.get_rect()
    pygame.Rect.move_ip(rect1, rect_x, 275)
    image_dic[image1] = rect1
    
    image2 = pygame.transform.scale(image, (550, 70))
    rect2 = image2.get_rect()
    pygame.Rect.move_ip(rect2, rect_x, 425)
    image_dic[image2] = rect2
    
    image3 = pygame.transform.scale(image, (550, 70))
    rect3 = image3.get_rect()
    pygame.Rect.move_ip(rect3, rect_x, 575)
    image_dic[image3] = rect3
    return image_dic
    
def set_images(screen, img_dic):  
    """根据字典将选项框显示出来"""
    for key, value in img_dic.items():
        screen.blit(key, value)
        
def load_words(screen, img_dic):
    """将字体及其位置储存在列表中，列表第一个元素为单词，第二个元素为一个字典，
    储存每个单词释义及其位置"""
    wli = []
    word_dic = {}
    pygame.font.init()
    font1 = pygame.font.SysFont("AdobeDevanagari-Regular.otf", 100)
    font2 = pygame.font.Font("C:/Windows/Fonts/simsun.ttc", 30)
    wordlist = choose_word(dic)
    word = wordlist[0][0]
    wli.append(wordlist[0])
    word = font1.render(word, True, (0, 0, 0))
    wrect = word.get_rect()
    wrect.midtop = screen.get_rect().midtop#调整英文单词位置
    word_dic[word] = wrect
    meaning0 = wordlist[0][1]
    meaning1 = wordlist[1]
    meaning2 = wordlist[2]
    meaning3 = wordlist[3]
    meaning0 = font2.render(meaning0, True, (0, 0, 0))
    meaning1 = font2.render(meaning1, True, (0, 0, 0))
    meaning2 = font2.render(meaning2, True, (0, 0, 0))
    meaning3 = font2.render(meaning3, True, (0, 0, 0))
    """调整字体位置"""
    order = [0, 1, 2, 3]
    random.shuffle(order)
    img_li = list(img_dic.items())
    for i in range(4):
        if i==0:
            wm = meaning0.get_rect()
            wm.center = img_li[order[i]][1].center
            word_dic[meaning0] = wm
        elif i==1:
            wm = meaning1.get_rect()
            wm.center = img_li[order[i]][1].center
            word_dic[meaning1] = wm
        elif i==2:
            wm = meaning2.get_rect()
            wm.center = img_li[order[i]][1].center
            word_dic[meaning2] = wm
        elif i==3:
            wm = meaning3.get_rect()
            wm.center = img_li[order[i]][1].center
            word_dic[meaning3] = wm
    wli.append(word_dic)
    return wli

def set_words(screen, li):
    for key, value in li[1].items():
        screen.blit(key, value)

def run_game(screen):
    global score
    global count
    global error
    if count>=10:
        show_score(screen)
    count += 1
    mark1 = pygame.image.load("D:/Wuwei/Computer_Science/Computer_Science_assignment/"
                              +"python/final_test/images/checkmark.png")
    mark2 = pygame.image.load("D:/Wuwei/Computer_Science/Computer_Science_assignment/"
                              +"python/final_test/images/cross.png")
    mrect = mark1.get_rect()
    pygame.Rect.move_ip(mrect, 1000, 500)
    img_dic = load_images(screen)
    wli = load_words(screen, img_dic)
    bcg = set_bcg(screen)
    while True: 
        screen.blit(bcg[0], bcg[1])
        set_images(screen, img_dic)
        set_words(screen, wli)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            (x, y)= pygame.mouse.get_pos()
            rect = pygame.Rect.copy(list(wli[1].items())[1][1])
            if event.type == pygame.MOUSEBUTTONDOWN:
                if x<rect.right and x>rect.left and y>rect.top-20 and y<rect.bottom+20:
                    play_music("glass_006.ogg")
                    score += 10
                    t_end = time.time()+0.5
                    while time.time()<t_end:
                        screen.blit(mark1, mrect)
                        pygame.display.update()
                else:
                    error.append(wli[0])
                    play_music("error_004.ogg")
                    t_end = time.time()+0.5
                    while time.time()<t_end:
                        screen.blit(mark2, mrect)
                        pygame.display.update()
                run_game(screen)
        """if count>10:
            return"""
        pygame.display.update()
        
def show_score(screen):
    global score
    global count
    global error
    if score>=80:
        play_music("wow.wav")
    font1 = pygame.font.SysFont("AdobeDevanagari-Regular.otf", 100)
    text = font1.render("your score is: "+str(score), True, (100, 100, 0))
    font2 = pygame.font.Font("C:/WINDOWS/Fonts/CONSTAN.TTF",30)
    txt_rect = text.get_rect()
    txt_rect.center = (600, 200)
    #button1 = pygame.transform.scale(button, (300, 50))
    button1 = pygame.image.load("D:/Wuwei/Computer_Science/Computer_Science_assignment/"
                                "python/final_test/images/newgameB.png")
    button2 = pygame.image.load("D:/Wuwei/Computer_Science/Computer_Science_assignment/"
                                +"python/final_test/images/buttonLong_beige_pressed.png")
    button2 = pygame.transform.scale(button2, (320, 50))
    button3 = pygame.image.load("D:/Wuwei/Computer_Science/Computer_Science_assignment/"
                                +"python/final_test/images/quit.png")
    brect1 = button1.get_rect()
    brect1.centerx = 200
    brect1.centery = 500
    brect2 = button2.get_rect()
    brect2.centerx = 600
    brect2.centery = 500
    button3 = pygame.transform.scale(button3, (200, 50))
    brect3 = button3.get_rect()
    brect3.centerx = 1000
    brect3.centery = 500
    caption = font2.render("review the wrong words", True, (0, 0, 255))
    crect = caption.get_rect()
    crect.center = brect2.center
    bcg = set_bcg(screen)
    while True:
        screen.blit(bcg[0], bcg[1])
        screen.blit(text, txt_rect)
        screen.blit(button1, brect1)
        screen.blit(button2, brect2)
        screen.blit(button3, brect3)
        screen.blit(caption, crect)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                if x<brect1.right and x>brect1.left and y<brect1.bottom and y>brect1.top:
                    score = 0
                    count = 0
                    run_game(screen)
                elif x<brect3.right and x>brect3.left and y<brect3.bottom and y>brect3.top:
                    pygame.quit()
                    sys.exit()
                elif x<brect2.right and x>brect2.left and y<brect2.bottom and y>brect2.top:
                    dic = error_word()
                    brect1.y += 100
                    brect3.y += 100
                    while True:
                        screen.blit(bcg[0], bcg[1])
                        screen.blit(button1, brect1)
                        screen.blit(button3, brect3)
                        for key, value in dic.items():
                            screen.blit(key, value)
                        for event in pygame.event.get():
                            if event.type==pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type==pygame.MOUSEBUTTONDOWN:
                                (x, y) = pygame.mouse.get_pos()
                                if x<brect1.right and x>brect1.left and y<brect1.bottom and y>brect1.top:
                                    score = 0
                                    count = 0
                                    error = []
                                    run_game(screen)
                                elif x<brect3.right and x>brect3.left and y<brect3.bottom and y>brect3.top:
                                    pygame.quit()
                                    sys.exit()
                        pygame.display.update()
        pygame.display.update()
        
def set_bcg(screen):
    li = []
    bcg = pygame.image.load("D:/Wuwei/Computer_Science/Computer_Science_assignment/"
                              "python/final_test/images/background-sheet0.png")
    bcg = pygame.transform.scale(bcg, (1200, 800))
    bcgrect = bcg.get_rect()
    bcgrect.center = screen.get_rect().center
    li.append(bcg)
    li.append(bcgrect)
    return li
        
def play_music(file):
    sound = pygame.mixer.Sound(file)
    sound.play()

def show_menu(screen):
    """显示主菜单"""
    image = pygame.image.load("D:/Wuwei/Computer_Science/Computer_Science_assignment"
                              +"/python/final_test/images/buttonLong_grey.png")
    font = pygame.font.SysFont("AdobeDevanagari-Regular.otf", 100)
    img1 = pygame.transform.scale(image, (300, 200))
    img2 = pygame.transform.scale(image, (300, 200))
    caption1 = font.render("cet-4", True, (50, 50, 50))
    caption2 = font.render("cet-6", True, (50, 50, 50))
    rect1 = img1.get_rect()
    rect2 = img2.get_rect()
    rect1.centerx = 300
    rect2.centerx = 900
    rect1.centery = screen.get_rect().centery
    rect2.centery = screen.get_rect().centery
    rect3 = caption1.get_rect()
    rect4 = caption2.get_rect()
    rect3.center = rect1.center
    rect4.center = rect2.center
    bcg = set_bcg(screen)
    while True:
        screen.blit(bcg[0], bcg[1])
        screen.blit(img1, rect1)
        screen.blit(img2, rect2)
        screen.blit(caption1, rect3)
        screen.blit(caption2, rect4)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                if x>rect1.left and x<rect1.right and y<rect1.bottom and y>rect1.top:
                    play_music("glass_006.ogg")
                    return 1
                if x>rect2.left and x<rect2.right and y<rect2.bottom and y>rect2.top:
                    play_music("glass_006.ogg")
                    return 2
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        
def error_word():
    word_dic = {}#储存错误单词及其释义及其位置
    length = len(error)
    font = pygame.font.Font("C:/Windows/Fonts/simsun.ttc", 30)
    if length<=5:
        for i in range(length):
            word = font.render(error[i][0]+" "+error[i][1], True, (0, 0, 0))
            wrect = word.get_rect()
            wrect.centerx = 300
            wrect.centery = 100 * i + 100
            word_dic[word] = wrect
    else:
        for i in range(5):
            word = font.render(error[i][0]+" "+error[i][1], True, (0, 0, 0))
            wrect = word.get_rect()
            wrect.centerx = 300
            wrect.centery = 100 * i + 100
            word_dic[word] = wrect
        for i in range(5, length):
            word = font.render(error[i][0]+" "+error[i][1], True, (0, 0, 0))
            wrect = word.get_rect()
            wrect.centerx = 900
            wrect.centery = 100 * (i-5) + 100
            word_dic[word] = wrect
    return word_dic
        
count = 0
score = 0
error = []

if __name__ == '__main__':
    """设置主界面"""
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Vocabulary Testing Game")
    
    t = show_menu(screen)
    if t==1:
        get_words("D:/Wuwei/Computer_Science/Computer_Science_assignment/python/final_test/cet4_words.txt")
    elif t==2:
        get_words("D:/Wuwei/Computer_Science/Computer_Science_assignment/python/final_test/cet6_words.txt")

    run_game(screen)
    show_score(screen)
    