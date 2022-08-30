# -*- coding: utf-8 -*-
# @Time : 2022/8/28 14:58
# @Author : hcy
# @Email : 573590153@qq.com
# @File : main.py
# @Project : wechat-love_every_day-server

import os
import random
import sys
from requests import get, post
import datetime
import time_calculator as tc
import city_server as cs
import text_server as ts


# 获取随机颜色
def get_random_color():
    return "#" + "%06x" % random.randint(0, 0xFFFFFF)


# 获取token
def get_access_token(config):
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    return access_token


# 推送
def send_message(config, access_token, region, weather, temperature, winddirection, windpower, humidity, soundbite_en,
                 soundbite_zh, chicken_soup):
    send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"

    # 获取当前时间
    today = datetime.datetime.now(tz=None)
    # 格式化时间字符串
    today_str = today.strftime("%Y-%m-%d")
    # 获取星期几
    week = tc.get_weekday(today)

    # 获取相识的日期差
    acquaint_day = str(tc.day_calculator(today_str, config["acquaint_day"]))
    print(acquaint_day)

    # 获取在一起的日期差
    love_days = str(tc.day_calculator(today_str, config["love_date"]))
    print(love_days)

    # 获取距下次在一起纪念日的时间
    love_commemoration_day = tc.commemoration_day_calculator(config["love_date"])
    print(love_commemoration_day)

    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if "birth" in k:
            birthdays[k] = v
    print(birthdays)

    # 准备发送数据
    data = {
        "touser": None,
        "template_id": config["template_id"],
        # 点击事件目标url
        # "url": "https://www.baidu.com/",
        "data": {
            "datetime": {
                "value": f"{today_str}  {week}",
                "color": get_random_color()
            },
            "region": {
                "value": region,
                "color": get_random_color()
            },
            "weather": {
                "value": weather,
                "color": get_random_color()
            },
            "temperature": {
                "value": temperature,
                "color": get_random_color()
            },
            "wind_power": {
                "value": windpower,
                "color": get_random_color()
            },
            "humidity": {
                "value": humidity,
                "color": get_random_color()
            },
            "wind_direction": {
                "value": winddirection,
                "color": get_random_color()
            },
            "acquaint_day": {
                "value": acquaint_day,
                "color": get_random_color()
            },
            "love_day": {
                "value": love_days,
                "color": get_random_color()
            },
            "love_commemoration_day": {
                "value": love_commemoration_day,
                "color": get_random_color()
            },
            "soundbite_title": {
                "value": "每日一句呦~",
                "color": get_random_color()
            },
            "soundbite_en": {
                "value": soundbite_en,
                "color": get_random_color()
            },
            "soundbite_zh": {
                "value": soundbite_zh,
                "color": get_random_color()
            },
            "chicken_soup_title": {
                "value": "鸡汤一下吧~",
                "color": get_random_color()
            },
            "chicken_soup": {
                "value": chicken_soup,
                "color": get_random_color()
            }
        }
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birthday = tc.commemoration_day_calculator(value["birthday"])
        if birthday == 0:
            birthday_data = f"今天{value['name']}生日哦，祝{value['name']}生日快乐吖~~~"
            # .format(, )
        else:
            birthday_data = f"距离{value['name']}的生日还有{birthday}天"
        # 将生日数据插入data
        data["data"][key] = {"value": birthday_data, "color": get_random_color()}
    print(data)

    # 循环发送
    for u in config["users"]:
        data["touser"] = u
        response = post(send_url, headers=config["headers"], json=data).json()
        if response["errcode"] == 40037:
            print("推送消息失败，请检查模板id是否正确")
        elif response["errcode"] == 40036:
            print("推送消息失败，请检查模板id是否为空")
        elif response["errcode"] == 40003:
            print("推送消息失败，请检查微信号是否正确")
        elif response["errcode"] == 0:
            print("推送消息成功")
        else:
            print(response)


if __name__ == '__main__':
    # 加载配置文件
    try:
        with open("conf.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("配置文件不存在")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件语法是否有误")
        os.system("pause")
        sys.exit(1)

    # 获取token
    access_token = get_access_token(config)
    print(access_token)
    # 获取发送所需要的信息
    city_code = cs.get_city_code(config["headers"], config['weather_key'], config['region'])
    print(city_code)
    city_weather = cs.get_city_weather(config["headers"], config['weather_key'], city_code)
    print(city_weather)
    chicken_soup = ts.get_chicken_soup(config["headers"])
    print(chicken_soup)
    soundbite = ts.get_soundbite(config["headers"])
    print(soundbite)

    # 打包发送内容方便管理
    send_list = list()
    # 添加所在地
    send_list.append(f"{city_weather['province']}  {city_weather['city']}")
    # 添加天气
    send_list.append(city_weather['weather'])
    # 添加温度
    send_list.append(city_weather['temperature'])
    # 添加风向
    if city_weather['winddirection'] == "无风向":
        city_weather['winddirection'] = "无持续风向"
    send_list.append(city_weather['winddirection'])
    # 添加风力
    send_list.append(city_weather['windpower'])
    # 添加湿度
    send_list.append(city_weather['humidity'])
    # 添加每日一句
    send_list.append(soundbite[1])
    send_list.append(soundbite[0])
    # 添加鸡汤一刻
    send_list.append(chicken_soup)

    # 推送消息
    send_message(config, access_token, *send_list)
