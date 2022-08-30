# -*- coding: utf-8 -*-
# @Time : 2022/8/29 21:10
# @Author : hcy
# @Email : 573590153@qq.com
# @File : text_server.py
# @Project : wechat-love_every_day-server


from requests import get


# 鸡汤一刻
def get_chicken_soup(headers):
    chicken_soup_url = "https://v1.hitokoto.cn/"
    response = get(chicken_soup_url, headers=headers).json()
    # 来自 格式处理
    if response["from"] and response["from_who"]:
        return response["hitokoto"] + "\n——" + response["from"] + "[{}]".format(response["from_who"])
    elif response["from"] and not response["from_who"]:
        return response["hitokoto"] + "\n——" + response["from"]
    elif not response["from"] and response["from_who"]:
        return response["hitokoto"] + "\n——" + "[{}]".format(response["from_who"])
    else:
        return response["hitokoto"]


# 每日金句
def get_soundbite(headers):
    soundbite_url = "http://open.iciba.com/dsapi/"
    response = get(soundbite_url, headers=headers).json()
    note_en = response["content"]
    note_ch = response["note"]
    return note_ch, note_en
