# *_*coding:utf-8 *_*
import json

origin_data = input()

info ={'姓名': '刘一', '手机': '13756899511', '地址': ['福建省', '福州市', '鼓楼区', '鼓西街道', '湖滨路110号湖滨大厦一层']}

json = json.dumps(info, ensure_ascii=False,  indent=4)

print(json)