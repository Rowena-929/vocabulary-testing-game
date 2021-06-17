# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 11:51:55 2021

@author: Wuwei
"""

import requests
from lxml import etree
import json

url = "http://www.oh100.com/kaoshi/cet6/cihui/249585.html"
res = requests.get(url)
res.encoding = res.apparent_encoding
html = res.text

tree = etree.HTML(html)
#words = tree.xpath("//div[@class='article']/div[@class='content']/p/text()")
p_list = tree.xpath("/html/body/div[3]/div[1]/div[1]/div[1]/p")
p_list.pop(0)
p_list.pop(0)
for i in range(-9, 0):
    p_list.pop(i)

dic = {}
count = 0
for li in p_list:
    word = li.xpath("./text()")[0]
    word = ''.join(word.split())
    word = word.replace("*", "")
    word = word.replace("&amp；", "")
    word = word.replace("a.","adj.")
    lii = word.split('/')
    try:
        dic[lii[0]] = lii[2]
    except IndexError:
        continue

filename = "cet6_words.txt"
with open(filename, 'w', encoding = 'utf-8') as f:
    f.write(json.dumps(dic, ensure_ascii=False))








