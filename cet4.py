# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 16:31:56 2021

@author: Wuwei
"""

import json

word_dic = {}

with open("cet-4.json", 'r', encoding = 'utf-8') as f1:
    with open('cet4_words.txt', 'w', encoding = 'utf-8') as f2:
        for line in f1.readlines():
            dic = json.loads(line)
            word_dic[dic['content']] = dic['remarks'][0]
        f2.write(json.dumps(word_dic, ensure_ascii=False))