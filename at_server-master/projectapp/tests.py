# coding:utf-8
import json
tt = {'a':'中文'}

print(json.dumps(tt, encoding='utf-8', ensure_ascii=False))