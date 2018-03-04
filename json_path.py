# -*- coding:utf-8 -*-
import requests,json
from jsonpath import jsonpath
from User_agent import User_Agt

url = 'http://www.lagou.com/lbs/getAllCitySearchLabels.json'
headers = User_Agt()
res = requests.get(url,headers=headers)
str_data = res.content.decode()

json_data = json.loads(str_data)

print(json_data)

# 这句意思，就是不管nana在什么位置，凡是有的都会查到
js_data = jsonpath(json_data,'$..name')

print(js_data)