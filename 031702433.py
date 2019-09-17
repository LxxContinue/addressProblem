#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jieba
import re
import cpca
import json


def sortinfo(information):
    info = {}
    # 去除名字和逗号
    origin_list = information.split(',', 1)
    info["姓名"] = origin_list[0]
    firstcut_list = origin_list[1]
    firstcut_list = jieba.lcut(firstcut_list)
    # 提取出电话号码
    for first_value in firstcut_list:
        phone = re.compile('^0\\d{2,3}\\d{7,8}$|^1[358]\\d{9}$|^147\\d{8}')
        phonematch = phone.match(first_value)
        if phonematch:
            info["手机"] = phonematch.group()
            del firstcut_list[firstcut_list.index(first_value)]
            break
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

    info["地址"] = newaddr + thridcut_list
    return info


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
sorted_info = sortinfo(origin_data)
# print(sorted_info)

json = json.dumps(sorted_info, ensure_ascii=False,  sort_keys=True, indent=4, separators=(',', ':'))
print(json)
