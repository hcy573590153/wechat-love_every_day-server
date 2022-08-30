# -*- coding: utf-8 -*-
# @Time : 2022/8/29 21:02
# @Author : hcy
# @Email : 573590153@qq.com
# @File : time_calculator.py
# @Project : wechat-love_every_day-server


import datetime


# 纪念日计算器
def commemoration_day_calculator(target_day):
    # 获取当天凌晨时间
    today = datetime.datetime.now()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    # 获取当年纪念日时间
    commemoration_day_data = [int(s) for s in target_day.split('-')]
    commemoration_day = datetime.datetime(year=today.year, month=commemoration_day_data[1],
                                          day=commemoration_day_data[2])
    # 计算时间差
    ret = (commemoration_day - today).days
    # 若纪念日早于当天时间，纪念日推后一年重新计算
    if ret < 0:
        commemoration_day = commemoration_day.replace(year=commemoration_day.year + 1)
        ret = (commemoration_day - today).days
    # print(ret)
    return ret


# 日期差计算
def day_calculator(day1, day2):
    # 解析时间
    day1_data = [int(s) for s in day1.split('-')]
    day2_data = [int(s) for s in day2.split('-')]
    # 解包计算
    return (datetime.datetime(*day1_data) - datetime.datetime(*day2_data)).days


# 获取文字形式的星期几
def get_weekday(date):
    iso_weekday = {
        1: '星期一',
        2: '星期二',
        3: '星期三',
        4: '星期四',
        5: '星期五',
        6: '星期六',
        7: '星期日',
    }
    return iso_weekday[date.isoweekday()]


def helloworld():
    print("hello world")
