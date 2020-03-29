# coding: utf-8
import os
import re

import easygui
import pygame
import requests
from pygame.locals import *
from xpinyin import Pinyin


def renderText(font, size, text, pos, canvas, type='file', file=r'tool\fonts\FZMW.ttf'):
    if type == 'local':
        textfont = pygame.font.SysFont(font, size)
        TF = textfont.render(text, True, (255, 255, 255))
        canvas.blit(TF, pos)
    else:
        textfont = pygame.font.Font(file, size)
        TF = textfont.render(text, True, (255, 255, 255))
        canvas.blit(TF, pos)
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4083.0 Safari/537.36 Edg/82.0.458.0


def getcitypinyin(str):
    pinyin = Pinyin()
    result = pinyin.get_pinyin(str, '')
    return result


class getweater(object):

    def __init__(self):
        self.city = '西安'
        self.citypinyin = getcitypinyin(self.city)
        self.url = "https://m.tianqi.com/" + self.citypinyin + '/'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4083.0 Safari/537.36 Edg/82.0.458.0'    
        }

    def gettodatweater(self):
        repon = requests.get(self.url, headers=self.headers)
        repon.encoding = 'utf-8'
        html = repon.text
        # print(repon, html)
        regdate = '<div class="date">(.*?)</div>'
        self.date = re.findall(regdate, html)[0]
        regnow = '<dd class="now">(.*?)<i>°C</i></dd>'
        self.temp = '当前温度：' + re.findall(regnow, html)[0] + '°C'
        # print(self.now)
        regtxt = '<dd class="txt">(.*?)</dd>'
        self.wea = '今日天气：' + re.findall(regtxt, html)[0]
        # print(self.txt)
        regb1 = '<span class="b2"><i></i>(.*?)</span>'
        self.shi = re.findall(regb1, html)[0]
        # print(self.b1)
        regb2 = '<span class="b3"><i></i>(.*?)</span>'
        self.feng = re.findall(regb2, html)[0]

    def get_future_5days_weather_data(self):
        reponse = requests.get(self.url, headers=self.headers)
        reponse.encoding = 'utf-8'
        # print(self.b2)
        html = reponse.text
        '''<dt>明天</dt>
        <dd class="txt">03/29</dd>
        <dd class="txt2">小雨到中雨</dd>'''
        reg_data = '<dd class="txt">(.*?)</dd>'

        weather_data = re.findall(reg_data, html)
        # print(weather_data)
        self.date = weather_data[1:11:2]
        # print(self.date)
        self.tem = weather_data[2:12:2]
        for i in range(5):
            self.tem[i] = self.tem[i].replace('<b>', '')
            self.tem[i] = self.tem[i].replace('</b>', '')
        # print(self.tem)
        reg_date = '<dd class="txt2">(.*?)</dd>'
        self.data = re.findall(reg_date, html)
        reg_kongqi = '<dd class="txt3"><b style="background-color: .*?">(.*?)</b></dd>'
        self.kongqi = re.findall(reg_kongqi, html)[:5]
        # print(self.kongqi)
        

class GlobalVar(object):
    weather = getweater()


GlobalVar.weather.gettodatweater()
GlobalVar.weather.get_future_5days_weather_data()


def threewindow():
    GlobalVar.weather.get_future_5days_weather_data()
    pygame.init()
    bg = pygame.image.load("tool\images\weather3.jpg")
    canvas = pygame.display.set_mode((1050, 660))

    def handleEvent():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return True
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                print(mx, my)
                if 10 <= mx <= 50 and 10 <= my <= 50:
                    pygame.quit()
                    localweatherbg()
                    return True

    while True:
        canvas.blit(bg, (0, 0))
        for i in range(5):
            x = 5
            y = 84 + 95 * i
            renderText('simhei', 25, GlobalVar.weather.date[i], (x, y), canvas, "file", r'tool\fonts\PingFang Bold.ttf')
            renderText('simhei', 25, GlobalVar.weather.data[i], (x + 120, y), canvas, "file", r'tool\fonts\PingFang Bold.ttf')
            renderText('simhei', 25, GlobalVar.weather.tem[i], (x, y + 40), canvas, "file", r'tool\fonts\PingFang Bold.ttf')
            renderText('simhei', 25, '空气质量：' + GlobalVar.weather.kongqi[i], (x + 180, y + 40), canvas, "file", r'tool\fonts\PingFang Bold.ttf')

        pygame.display.update()
        if handleEvent():
            break


def localweatherbg():
    pygame.init()
    bg = pygame.image.load("tool\images\weather2.jpg")
    canvas = pygame.display.set_mode((1050, 660))

    def handleEvent():
        event = pygame.event.get()
        for i in event:
            if i.type == QUIT:
                pygame.quit()
                return True
            elif i.type == MOUSEBUTTONDOWN and i.button == 1:
                x, y = pygame.mouse.get_pos()
                print(x, y)
                if 410 <= x <= 650 and 450 <= y <= 500:
                    pygame.quit()
                    print("跳转中")
                    print("完成")
                    threewindow()
                    return True
                if 423 <= x <= 627 and 538 <= y <= 592:
                    GlobalVar.weather.city = easygui.enterbox('请输入城市名称：')
                    GlobalVar.weather.citypinyin = getcitypinyin(GlobalVar.weather.city)
                    GlobalVar.weather.url = "https://m.tianqi.com/" + GlobalVar.weather.citypinyin + '/'
                    GlobalVar.weather.gettodatweater()
                    GlobalVar.weather.get_future_5days_weather_data()
                    localweatherbg()

    while True:
        canvas.blit(bg, (0, 0))
        GlobalVar.weather.gettodatweater()
        renderText('fangsong', 30, GlobalVar.weather.date, (249, 120), canvas)
        renderText('simhei', 50, GlobalVar.weather.city, (420, 5), canvas, file=r'tool\fonts\PingFang Bold.ttf')
        renderText('simhei', 30, GlobalVar.weather.temp, (251, 158), canvas)
        renderText('simhei', 30, GlobalVar.weather.wea, (251, 192), canvas)
        renderText('simhei', 30, GlobalVar.weather.shi, (254, 230), canvas)
        renderText('simhei', 40, GlobalVar.weather.feng, (499, 220), canvas)
        pygame.display.update()
        if handleEvent():
            break


def start_bg():
    canvas = pygame.display.set_mode((1050, 660))
    pygame.display.set_caption("天气预报")
    bg = pygame.image.load("tool\images\weather1.jpg")

    def handleEvent():
        event = pygame.event.get()
        for i in event:
            if i.type == QUIT:
                pygame.quit()
                return True
            if i.type == MOUSEBUTTONDOWN and i.button == 1:
                mx, my = pygame.mouse.get_pos()
                print(mx, my)
                if 10 <= mx <= 50 and 10 <= my <= 50:
                    pygame.quit()
                    os.system("python menu.py")
                elif 550 <= my <= 610 and 760 <= mx <= 970:
                    pygame.quit()
                    print("进入天气预报中")
                    print("进入成功")
                    localweatherbg()
                    return True

    while True:
        canvas.blit(bg, (0, 0))
        pygame.display.update()
        if handleEvent():
            break


start_bg()
