# -*- coding: utf-8 -*-
# @Time : 2022/8/29 21:05
# @Author : hcy
# @Email : 573590153@qq.com
# @File : city_server.py
# @Project : wechat-love_every_day-server


import os
import sys
from requests import get


# 获取城市代码
def get_city_code(headers, weather_key, address):
    city_code_url = f"https://restapi.amap.com/v3/geocode/geo?address={address}&key={weather_key}"
    response = get(city_code_url, headers=headers).json()
    if response['status'] == '1' and response['infocode'] == '10000':
        return response['geocodes'][0]['adcode']
    else:
        print("获取城市编码失败，请检查地址是否正确")
        os.system("pause")
        sys.exit(1)


# 获取城市天气
def get_city_weather(headers, weather_key, city_code):
    city_weather_url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city_code}&key={weather_key}"
    response = get(city_weather_url, headers=headers).json()
    if response['status'] == '1' and response['infocode'] == '10000':
        return response['lives'][0]
    else:
        print("获取城市天气失败")
        os.system("pause")
        sys.exit(1)
