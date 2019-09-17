#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jieba
import re
import cpca
import json
import profile


# 去除名字和逗号
def sort_name(information):

    origin_list = information.split(',', 1)
    name = origin_list[0]
    return name, origin_list[1]


# 提取出电话号码
def sort_phone(infomation):
    phonenum = " "
    for first_value in infomation:
        phone = re.compile('^0\\d{2,3}\\d{7,8}$|^1[358]\\d{9}$|^147\\d{8}')
        phonematch = phone.match(first_value)
        if phonematch:
            phonenum = phonematch.group()
            del infomation[infomation.index(first_value)]
            break
    return phonenum, infomation


# 切分并填充地址
def sortinfo(information):
    name, firstcut_list = sort_name(information)

    firstcut_list = jieba.lcut(firstcut_list)

    phone, firstcut_list = sort_phone(firstcut_list)

    # 重新合成地址
    firstsorted_address = ''
    for addr in firstcut_list:
        firstsorted_address += addr
    # 切分并填充地址
    location_str = [firstsorted_address]
    df = cpca.transform(location_str)

    newaddr = []
    secondcut_list = df.values[0]
    for addr in secondcut_list:
        newaddr.append(addr)
    # 切分街道、镇、乡
    lastaddr = newaddr.pop()
    thridcut_list = lastaddr.split('街道', 1)
    if len(thridcut_list) > 1:
        thridcut_list[0] += "街道"
    else:
        thridcut_list = lastaddr.split('镇', 1)
        if len(thridcut_list) > 1:
            thridcut_list[0] += "镇"
        else:
            thridcut_list = lastaddr.split('乡', 1)
            if len(thridcut_list) > 1:
                thridcut_list[0] += "乡"
            else:
                thridcut_list.insert(0, '')

    address = newaddr + thridcut_list
    temp = {
            "姓名": name,
            "手机": phone,
            "地址": address
        }
    return json.dumps(temp, ensure_ascii=False,  indent=4)


'''
origin_data = ["李四,福建省福州13756899511市鼓楼区鼓西街道湖滨路110号湖滨大厦一层", "张三,福建福州闽13599622362侯县上街镇福州大学10#111",
               "王五,福建省福州市鼓楼18960221533区五一北路123号福州鼓楼医院", "小美,北京市东15822153326城区交道口东大街1号北京市东城区人民法院",
               "小陈,广东省东莞市凤岗13965231525镇凤平路13号"]
new_data = ["小陈,广东省东莞市凤岗13965231525镇凤平路13号"]
sorted_info = []
for one_data in new_data:
    sorted_info.append(sort_info(one_data))
'''

origin_data = input()
print(sortinfo(origin_data))
